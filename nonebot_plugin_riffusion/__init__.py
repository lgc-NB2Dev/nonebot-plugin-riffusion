from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.2"
__plugin_meta__ = PluginMetadata(
    name="Riffusion",
    description="你给歌词，AI 作曲",
    usage="使用指令 riffusion -h 查看帮助",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-riffusion",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "student_2333"},
)
