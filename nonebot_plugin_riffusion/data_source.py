import base64
import random
import uuid
from dataclasses import dataclass

from httpx import AsyncClient
from pydantic import BaseModel, validator
from pydantic.main import ModelMetaclass

from .config import config

PRESET_PROMPTS_MAP = {
    "Upbeat": ["edm dance song, electronic female vocals"],
    "Shred": ["Rock"],
    "Groove": ["R&B"],
    "Twang": ["Country"],
    "Indie": ["Indie pop music"],
    "Surprise": [
        "edm dance song, electronic female vocals",
        "punk rock, male vocals",
        "indie country pop song",
        "upbeat country folk song, male vocals, banjo",
        "female, country folk song, pop",
        "1930's jazz singer, smooth drums",
        "edm dance song, male vocals harmonies",
        "electronic dance song, male vocals",
        "upbeat electronic vocals",
        "indie rock, male pop singer, heartfelt",
        "heartfelt ballad, acoustic guitar",
        "jazz piano, soulful female vocals",
        "bluegrass jam, male vocals, banjo",
        "heartfelt acoustic indie, guitar strumming, male vocals",
        "big band swing jazz",
        "upbeat disco with funky bassline, energetic female vocals",
        "operatic aria, soprano singer, beautiful clear vocals",
        "country pop song with catchy lyrics and singing",
        "tropical island groove, laid back vocals",
        "tropical house, dance, male vocals, energetic and upbeat",
        "death metal",
        "heartfelt piano ballad, male vocals",
        "electronic pop with catchy synth hooks, female ballad",
        "indie rock, electric guitar, female ballad",
        "angelic choir singing, harp",
        "indie pop acoustic guitar, female singing",
    ],
}
PRESET_LYRICS = [
    "You've got to pay the cheese tax, Every time you're cooking, When the cheese comes out, This puppy comes looking!",
    "If we ever broke up",
    "Sticking out your thumb for the picture",
    "I just got hit by cupid now I'm feeling lonely",
    "Girls like me don't cry",
    "Hands on yo knees shawty got sum",
    "Can't take my eyes off youuu",
    "All I want for Thanksgiving is you",
    "Bing bing bong ding ding dong I can sing sing sing anything that you want",
    "It's the most wonderful fall of the year",
    "And I wonder if you know",
    "No cap and gown I ain't go to class",
    "Life goes on",
    "I'm feeling good",
    "Beat it repeat it beat it",
    "Little bitty pretty one",
    "I knew I loved you",
    "Tell me all the things I wanna hear",
    "That boy's a liar",
    "Dance if you still want her",
    "You're my weakness",
    "That's just the way it is",
    "It's too early for christmas lights",
]
SESSION_ID = str(uuid.uuid4())


def camel_case(string: str, upper_first: bool = False) -> str:
    pfx, *rest = string.split("_")
    if upper_first:
        pfx = pfx.capitalize()
    sfx = "".join(x.capitalize() for x in rest)
    return f"{pfx}{sfx}"


class CamelAliasModelMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):  # noqa: N804
        kwargs["alias_generator"] = camel_case
        return super().__new__(mcs, name, bases, namespace, **kwargs)


@dataclass
class Base64DataUrl:
    mime: str
    data: bytes

    @property
    def ext(self) -> str:
        return self.mime.split("/")[-1] if "/" in self.mime else f"{self.mime}.bin"


def validator_decode_base64_data_url(v) -> Base64DataUrl:
    try:
        assert isinstance(v, str)
        head, b64str = v.split(",", 1)
        mime = head[head.find(":") + 1 : head.find(";")]
        data = base64.b64decode(b64str)
        return Base64DataUrl(mime, data)
    except Exception as e:
        raise ValueError("invalid base64 data url") from e


class SingleAudioOutput(BaseModel):
    audio: Base64DataUrl
    key: str
    # lyrics: {"words": [{"end": float, pronunciation: str, start: float, text: str, wav2vec2_format: Optional[Any]}]}
    seed: int

    _decode_audio = validator("audio", pre=True, allow_reuse=True)(
        validator_decode_base64_data_url,
    )


class SingleImageOutput(BaseModel):
    image: Base64DataUrl
    key: str

    _decode_image = validator("image", pre=True, allow_reuse=True)(
        validator_decode_base64_data_url,
    )


class SingleGeneratedResult(BaseModel, metaclass=CamelAliasModelMeta):
    audio_output: SingleAudioOutput
    image_output: SingleImageOutput
    title: str


def get_sound_prompt(key: str) -> str:
    prompts = PRESET_PROMPTS_MAP[key]
    return prompts[0] if len(prompts) == 1 else random.choice(prompts)


def get_random_lyrics() -> str:
    return random.choice(PRESET_LYRICS)


async def generate_single(lyrics: str, prompt: str, tag: str) -> SingleGeneratedResult:
    async with AsyncClient(proxies=config.proxy) as cli:
        resp = await cli.post(
            "https://www.riffusion.com/api/trpc/inference.singleTextToAudio",
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/119.0.0.0 "
                    "Safari/537.36"
                ),
                "Origin": "https://www.riffusion.com",
                "Referer": "https://www.riffusion.com/",
            },
            json={
                "json": {
                    "lyrics": lyrics,
                    "prompt": prompt,
                    "session_id": SESSION_ID,
                    "tag": tag,
                },
            },
            follow_redirects=True,
            timeout=config.riffusion_timeout,
        )
        resp.raise_for_status()
        return SingleGeneratedResult.parse_obj(resp.json()["result"]["data"]["json"])
