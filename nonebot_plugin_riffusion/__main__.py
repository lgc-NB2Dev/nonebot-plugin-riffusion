import asyncio
import re
from typing import Optional

from arclet.alconna import (
    Alconna,
    Arg,
    Args,
    Arparma,
    ArparmaBehavior,
    CommandMeta,
    Option,
    store_true,
)
from arclet.alconna.exceptions import OutBoundsBehave, SpecialOptionTriggered
from nonebot import logger
from nonebot_plugin_alconna import AlconnaMatcher, CommandResult, on_alconna
from nonebot_plugin_alconna.uniseg import Receipt, UniMessage

from .config import config
from .data_source import (
    PRESET_PROMPTS_MAP,
    generate_single,
    get_random_lyrics,
    get_sound_prompt,
)

ENGLISH_REGEX = re.compile(r"^[a-zA-Z0-9,.?!:;'\" ]+$")
DEFAULT_PRESET_KEY = "Surprise"


def break_url(url: str) -> str:
    return (
        url.replace("http://", "")
        .replace("https://", "")
        .replace(".", ". ")
        .replace("/", "/ ")
    )


class RecallManager:
    def __init__(self, receipt: Receipt) -> None:
        self.receipt = receipt

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async def do():
            try:
                await self.receipt.recall()
            except Exception as e:
                logger.warning(f"Recall failed: {type(e).__name__}: {e}")
                logger.opt(exception=e).debug("Stack trace:")

        asyncio.create_task(do())


class RiffusionBehavior(ArparmaBehavior):
    def operate(self, interface: Arparma):
        style: Optional[str] = interface["style"]
        prompt: Optional[str] = interface["prompt"]
        random_lyrics: bool = interface["random-lyrics"].value
        lyrics: Optional[str] = interface["lyrics"]

        if style:
            if prompt:
                raise OutBoundsBehave("不能同时指定 预设风格 Prompt 和 自定义 Prompt")
            if style not in PRESET_PROMPTS_MAP:
                raise OutBoundsBehave("预设风格不存在")

        if lyrics:
            if random_lyrics:
                raise OutBoundsBehave("不能同时 使用随机歌词 和 指定歌词")
            if not ENGLISH_REGEX.match(lyrics):
                raise OutBoundsBehave("歌词仅支持英文")
            if len(lyrics.split()) > 25:
                raise OutBoundsBehave("请将歌词限制在 25 词以内")
        elif not random_lyrics:  # and not lyrics
            raise OutBoundsBehave("请指定歌词，或使用随机歌词")


cmd_riffusion = on_alconna(
    Alconna(
        "riffusion",
        Option(
            "--style",
            Args["style", str],
            alias=("-s",),
            default=None,
            help_text=(
                f"使用指定预设风格 Prompt，默认为 {DEFAULT_PRESET_KEY}，"
                f"可选值：{'；'.join(PRESET_PROMPTS_MAP)}"
            ),
        ),
        Option(
            "--prompt",
            Args["prompt", str],
            alias=("-p",),
            default=None,
            help_text="使用指定 Prompt",
        ),
        Option(
            "--random-lyrics",
            alias=("-R",),
            default=False,
            action=store_true,
            help_text="使用随机预置歌词",
        ),
        Args(
            Arg(
                "lyrics?",
                value=str,
                notice="歌词（仅支持英文）",
            ),
        ),
        meta=CommandMeta(
            description="你给歌词，AI 作曲\n给出一段歌词，AI 将会根据你的歌词生成一段 12 秒的音频",
            example='riffusion -R\nriffusion -s Upbeat "If we ever broke up"',
        ),
        behaviors=[RiffusionBehavior()],
    ),
    aliases={"riff"},
    skip_for_unmatch=False,
    use_cmd_start=True,
)


@cmd_riffusion.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `riffusion -h` 查看帮助")


@cmd_riffusion.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    style: Optional[str] = parma["style"]
    custom_prompt: Optional[str] = parma["prompt"]
    use_random_lyrics: bool = parma["random-lyrics"].value

    lyrics: str = get_random_lyrics() if use_random_lyrics else parma["lyrics"]
    prompt: str = (
        custom_prompt
        if custom_prompt
        else get_sound_prompt(style or DEFAULT_PRESET_KEY)
    )
    tag = f"/,{style if style else 'Surprise'}"

    async with RecallManager(
        await UniMessage("生成中，请稍候~").send(reply_to=True),
    ):
        try:
            resp = await generate_single(lyrics, prompt, tag)
        except Exception:
            logger.exception("Failed to fetch response")
            await matcher.finish("生成失败，请检查后台输出")

    audio_key = resp.audio_output.key
    audio = resp.audio_output.audio
    receipt = await UniMessage.audio(
        raw=audio.data,
        mimetype=audio.mime,
        name=f"{audio_key}.{audio.ext}",
    ).send()  # reply_to=True

    url = f"https://www.riffusion.com/riffs/{audio_key}"
    if config.riffusion_break_url:
        url = break_url(url)
    image_key = resp.image_output.key
    image = resp.image_output.image
    image_caption = f"Title: {resp.title}\n"
    if use_random_lyrics:
        image_caption += f"Lyrics: {lyrics}\n"
    if not custom_prompt:
        image_caption += f"Prompt: {prompt}\n"
    image_caption += f"{url}"
    await receipt.reply(
        UniMessage.image(
            raw=image.data,
            mimetype=image.mime,
            name=f"{image_key}.{image.ext}",
        ).text(image_caption),
    )
