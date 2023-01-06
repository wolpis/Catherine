from discord.ext import commands

from .booru import booru
from .konachan import konachan
# 와일드 카드 임포트
from .pixiv import pixiv
from .zerochan import zerochan

commands = [
    val
    for val in locals().values()
    if isinstance(val, commands.HybridGroup) or isinstance(val, commands.HybridCommand)
]
