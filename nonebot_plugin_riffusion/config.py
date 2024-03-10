from typing import Optional

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    proxy: Optional[str] = None

    riffusion_timeout: float = 30
    riffusion_break_url: bool = False


config = get_plugin_config(ConfigModel)
