from discord import app_commands
from discord.ext import commands
from model import KonachanModel

konachan_model = KonachanModel()


@commands.hybrid_group(name="코나찬")
async def konachan(ctx: commands.Context):
    """코나찬 기능 명령어들"""
    pass


@konachan.command(name="최신")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def s_id(ctx: commands.Context, 나만보기: bool = False):
    """코나찬 최신 작품을 불러옵니다."""
    if ctx.channel.nsfw:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = await konachan_model.post(ctx.author.id)
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=konachan_model.embed(title="해당 명령어는 연령제한채널에서만 가능합니다."), ephemeral=True
        )


@konachan.command(name="인기")
@app_commands.describe(모드="인기작품의 기준점을 설정합니다.", 나만보기="일러스트의 가시성을 설정합니다.")
@app_commands.choices(
    모드=[
        app_commands.Choice(name="지난 24시간", value="popular_recent"),
        app_commands.Choice(name="일별", value="popular_by_day"),
        app_commands.Choice(name="주별", value="popular_by_week"),
        app_commands.Choice(name="월별", value="popular_by_month"),
    ]
)
async def s_id(ctx: commands.Context, 모드: str, 나만보기: bool = False):
    """코나찬 인기 작품을 불러옵니다."""
    if ctx.channel.nsfw:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = await konachan_model.popular(ctx.author.id, 모드)
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=konachan_model.embed(title="해당 명령어는 연령제한채널에서만 가능합니다."), ephemeral=True
        )
