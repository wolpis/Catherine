from discord import app_commands
from discord.ext import commands
from model import PixivModel

pixiv_model = PixivModel()


@commands.hybrid_group(name="픽시브")
async def pixiv(ctx: commands.Context):
    """픽시브 기능 명령어들"""
    pass


@pixiv.command(name="검색")
@app_commands.describe(illust_id="작품의 아이디를 입력해주세요!", 나만보기="일러스트의 가시성을 설정합니다.")
async def pixiv_search(ctx: commands.Context, illust_id: str, 나만보기: bool = False):
    """픽시브 검색(ID)를 진행합니다."""
    if illust_id.isdigit():
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = pixiv_model.request(f"/ajax/illust/{illust_id}")
        data = pixiv_model.image_embed(data=data)
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="ID 항목은 숫자만 입력해주세요!!"), ephemeral=True
        )


@pixiv.command(name="랜덤")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def pixiv_search(ctx: commands.Context, 나만보기: bool = False):
    """픽시브 랜덤작품을 가져옵니다. (약후방 조심)"""
    if ctx.channel.nsfw:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = pixiv_model.random_embed()
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="해당 명령어는 연령제한채널에서만 가능합니다."), ephemeral=True
        )


@pixiv.command(name="r18")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def pixiv_search(ctx: commands.Context, 나만보기: bool = False):
    """픽시브 랜덤작품을 가져옵니다. (후방 조심)"""
    if ctx.channel.nsfw:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = pixiv_model.r18_embed()
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="해당 명령어는 연령제한채널에서만 가능합니다."), ephemeral=True
        )


@pixiv.command(name="태그")
@app_commands.describe(나만보기="일러스트의 가시성을 설정합니다.")
async def pixiv_search(
    ctx: commands.Context, tag: str, r18: bool = False, 나만보기: bool = False
):
    """픽시브 태그작품을 검색합니다. (후방 조심)"""
    if ctx.channel.nsfw:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        data = pixiv_model.tag_embed(tag, r18)
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="해당 명령어는 연령제한채널에서만 가능합니다."), ephemeral=True
        )


@pixiv.command(name="랭킹")
@app_commands.describe(모드="일일 / 주간 / 월간 중에서 선택하실 수 있습니다.")
@app_commands.choices(
    모드=[
        app_commands.Choice(name="일일", value="일일"),
        app_commands.Choice(name="주간", value="주간"),
        app_commands.Choice(name="월간", value="월간"),
    ]
)
async def pixiv_search(ctx: commands.Context, 모드: str, 나만보기: bool = False):
    """픽시브 순위 작품을 가져옵니다."""
    if 모드 in ["일일", "주간", "월간"]:
        msg = await ctx.reply("작품을 불러오는 중입니다.", ephemeral=나만보기)
        tag_dict = {"일일": "daily", "주간": "weekly", "월간": "monthly"}
        data = pixiv_model.request(
            f"/ranking.php?mode={tag_dict[모드]}&content=illust&format=json"
        )
        data = pixiv_model.ranking_embed(ctx.author.id, data)
        await msg.edit(content=None, embed=data[0], view=data[1])
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="올바른 모드 설정이 아닙니다."), ephemeral=True
        )
