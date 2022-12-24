from discord.ext import commands


# 와일드 카드 임포트
from .pixiv import pixiv
from .booru import booru

commands = [
    val
    for val in locals().values()
    if isinstance(val, commands.HybridGroup) or isinstance(val, commands.HybridCommand)
]
