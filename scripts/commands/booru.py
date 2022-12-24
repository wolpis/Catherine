from discord import app_commands
from discord.ext import commands
from model import BooruModel

booru_model = BooruModel()


@commands.hybrid_group(name="단보루")
async def booru(ctx: commands.Context):
    """단보루 기능 명령어들"""
    pass


@booru.command(name="검색")
@app_commands.describe(tag="일본어 발음을 로마자로 적어 검색합니다. 띄어쓰기는 언더바(_)를 사용해주세요!", 나만보기="일러스트의 가시성을 설정합니다.")
async def post(ctx: commands.Context, tag: str, 나만보기: bool = False):
    """태그를 사용해 작품을 가져옵니다."""
    msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
    data = booru_model.search(ctx.author.id, tag)
    await msg.edit(content=None, embed=data[0], view=data[1])


@booru.command(name="최신")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def post(ctx: commands.Context, 나만보기: bool = False):
    """최근에 업데이트된 작품들을 가져옵니다."""
    msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
    data = await booru_model.post(ctx.author.id)
    await msg.edit(content=None, embed=data[0], view=data[1])
