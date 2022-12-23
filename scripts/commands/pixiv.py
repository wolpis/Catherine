from discord import app_commands
from discord.ext import commands
from model import PixivModel

pixiv_model = PixivModel()


@commands.hybrid_command(name="픽시브검색")
@app_commands.describe(illust_id="작품의 아이디를 입력해주세요!", 나만보기="일러스트의 가시성을 설정합니다.")
async def pixiv_search(ctx: commands.Context, illust_id: str, 나만보기: bool = False):
    """픽시브 검색(ID)를 진행합니다."""
    if illust_id.isdigit():
        data = pixiv_model.request(f"/ajax/illust/{illust_id}")
        data = pixiv_model.image_embed(data=data)
        msg = await ctx.send(embed=data[0], view=data[1], ephemeral=나만보기)
        await msg.add_reaction("👎")
    else:
        await ctx.send(
            embed=pixiv_model.embed(title="ID 항목은 숫자만 입력해주세요!!"), ephemeral=True
        )
