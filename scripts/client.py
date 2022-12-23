from discord import Object, Interaction, Message
from discord.ext import commands

from config import CatherineConfig
from commands import commands as cds

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


@bot.tree.context_menu(name="그림삭제")
async def change_image(inter: Interaction, msg: Message):
    await inter.response.send_message("처리중..")
    msg.embeds[0].set_footer(text=f"{inter.user.name}님에 의하여 검열처리")
    msg.embeds[0].set_image(
        url="https://media.discordapp.net/attachments/1052260588660719678/1055895525616013372/-angry.gif"
    )
    await msg.edit(embed=msg.embeds[0])
    await inter.delete_original_response()


bot.run(CatherineConfig.token)
