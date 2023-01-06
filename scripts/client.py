from commands import commands as cds
from config import CatherineConfig
from discord import Embed, Interaction, Message, Object, SelectOption
from discord.ext import commands
from discord.ui import Select, View

bot = commands.Bot(
    command_prefix=CatherineConfig.prefix, intents=CatherineConfig.intents()
)


@bot.event
async def on_ready():
    for command in cds:
        bot.add_command(command)
    if CatherineConfig.public:
        await bot.tree.sync()
    else:
        bot.tree.copy_global_to(guild=Object(CatherineConfig.guild_id))
        await bot.tree.sync(guild=Object(CatherineConfig.guild_id))


@bot.hybrid_command("도움말")
async def help_command(ctx: commands.Context):
    """도움말 문서입니다."""
    p = bot.get_emoji(1056203497428762654)
    z = bot.get_emoji(1056205292586668083)
    k = bot.get_emoji(1056204151639519282)
    b = bot.get_emoji(1056203760730390608)
    embed = Embed(
        title="캐서린 사용설명서",
        description="제작자 : `Neru#4379`\n접두사 : `?` | 모든 명령어 빗금명령어(/) 지원",
        color=0xF18EA3,
    )
    embed.add_field(
        name="지원서버목록", value=f">>> {p} 픽시브\n \n{b} 단보루\n \n{k} 코나찬\n \n{z} 제로찬"
    )
    options = [
        SelectOption(emoji=p, label="픽시브", value="픽시브"),
        SelectOption(emoji=b, label="단보루", value="단보루"),
        SelectOption(emoji=k, label="코나찬", value="코나찬"),
        SelectOption(emoji=z, label="제로찬", value="제로찬"),
    ]
    select = Select(
        options=options, placeholder="도움말을 선택해주세요!", min_values=1, max_values=1
    )

    async def callback(inter: Interaction):
        if select.values[0] == "픽시브":
            text = """</픽시브 검색:1056029686662189108> : 일러스트 아이디(품번)으로 작품을 가져옵니다.
            
            </픽시브 랜덤:1056029686662189108> : 랜덤으로 일러스트를 가져옵니다. (약후방)

            </픽시브 r18:1056029686662189108> : 랜덤으로 일러스트를 가져옵니다. (후방)

            </픽시브 랭킹:1056029686662189108> : 픽시브 랭킹 일러스트를 가져옵니다.

            </픽시브 태그:1056029686662189108> : 태그에 맞는 일러스트를 가져옵니다.
            """
            embed = Embed(title="픽시브 사용설명서", description=text, color=0x0096FA)
            await inter.response.edit_message(embed=embed)
        elif select.values[0] == "단보루":
            text = """</단보루 검색:1056065100504649728> : 일본어 발음을 로마자로 적어 검색합니다.

            </단보루 최신:1056065100504649728> : 단보루 최신 일러스트들을 가져옵니다.
            """
            embed = Embed(title="단보루 사용설명서", description=text, color=0xFFE08C)
            await inter.response.edit_message(embed=embed)

        elif select.values[0] == "코나찬":
            text = """</코나찬 최신:1056153768531599381> : 코나찬 최신 작품을 불러옵니다.

            </코나찬 인기:1056153768531599381> : 코나찬 인기 작품을 불러옵니다.
            """
            embed = Embed(title="코나찬 사용설명서", description=text, color=0xFF007F)
            await inter.response.edit_message(embed=embed)

        elif select.values[0] == "제로찬":
            text = """</제로찬 최신:1056136844586254387> : 제로찬 최신 작품을 불러옵니다.

            </제로찬 인기:1056136844586254387> : 제로찬 인기 작품을 불러옵니다.
            """
            embed = Embed(title="제로찬 사용설명서", description=text, color=0xABF200)
            await inter.response.edit_message(embed=embed)

    select.callback = callback
    view = View()
    view.add_item(select)
    await ctx.reply(embed=embed, view=view)


@bot.tree.context_menu(name="그림삭제")
async def change_image(inter: Interaction, msg: Message):
    await inter.response.send_message("처리중..")
    try:
        msg.embeds[0].set_footer(text=f"{inter.user.name}님에 의하여 검열처리")
        msg.embeds[0].set_image(
            url="https://media.discordapp.net/attachments/1052260588660719678/1055895525616013372/-angry.gif"
        )
        await msg.edit(embed=msg.embeds[0])
        await inter.delete_original_response()
    except:
        await inter.edit_original_response(content="지원하지 않는 메세지입니다.")


bot.run(CatherineConfig.token)
