from discord import app_commands
from discord.ext import commands
from model import ZeroChanModel

zerochan_model = ZeroChanModel()


@commands.hybrid_group(name="제로찬")
async def zerochan(ctx: commands.Context):
    """제로찬 기능 명령어들"""
    pass


@zerochan.command(name="최신")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def s_id(ctx: commands.Context, 나만보기: bool = False):
    """제로찬 최신 작품을 불러옵니다."""
    msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
    data = await zerochan_model.s_id(ctx.author.id)
    await msg.edit(content=None, embed=data[0], view=data[1])


@zerochan.command(name="인기")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def f_id(ctx: commands.Context, 나만보기: bool = False):
    """제로찬 인기 작품을 불러옵니다."""
    msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
    data = await zerochan_model.f_id(ctx.author.id)
    await msg.edit(content=None, embed=data[0], view=data[1])
