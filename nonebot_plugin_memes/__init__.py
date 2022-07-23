from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import MessageSegment

require("nonebot_plugin_imageutils")

from .depends import regex
from .data_source import memes
from .utils import Meme, help_image

__plugin_meta__ = PluginMetadata(
    name="表情包制作",
    description="生成各种表情包",
    usage="触发方式：指令 + 文字 (部分表情包需要多段文字)\n发送“表情包制作”查看表情包列表",
    extra={
        "unique_name": "memes",
        "example": "鲁迅说 我没说过这句话\n举牌 aya大佬带带我",
        "author": "meetwq <meetwq@gmail.com>",
        "version": "0.3.3",
    },
)

__zx_plugin_name__ = "表情包制作"
__plugin_usage__ = """
Usage:
    触发方式：指令 + 文字 (部分表情包需要多段文字)
    发送“表情包制作”查看表情包列表
    （静态表情的参数个数如果不对将不会响应）
    例子：
        五年怎么过的.gif 我 在 哪 里
        举牌 rua
        可达鸭 左手 右手
""".strip()
__plugin_des__ = "生成各种表情包"
__plugin_type__ = ("好玩的",)
__plugin_version__ = 0.3
__plugin_cmd__ = ["表情包制作"]
__plugin_author__ = "meetwq"

__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": [],
}

help_cmd = on_command("表情包制作", block=True, priority=12)


@help_cmd.handle()
async def _():
    img = await help_image(memes)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        async def handle(
            matcher: Matcher, res: Union[str, BytesIO] = Depends(meme.func)
        ):
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=False,
            priority=12,
        ).append_handler(handler(meme))


create_matchers()
