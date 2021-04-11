import discord
import json
from googletrans import Translator
from discord import Embed
from icecream import ic
# from discord.ext import commands

TOKEN = "ODMwNTAzMTE5MzEzNjk4ODc2.YHHoTQ.sJF_g6jWPX_vOMYWRc0xlMIKXc4"
translator = Translator()

# bot = commands.Bot(command_prefix=('/'))

client = discord.Client()

global_registred_chanels = []


@client.event
async def on_message(message):
    ic(message)
    ic(message.content)

    if message.content.startswith('/'):
        await processing_bot_commands(message)
    elif message.author.bot:
        pass
    else:
        await translate_message(message)


async def processing_bot_commands(message):
    cmd = message.content.split()[0].replace("/", "")
    if len(message.content.split()) > 1:
        parameters = message.content.split()[1:]
    else:
        parameters = None

    if cmd == "connect_channel":
        await connect_chanel_cmd(message, parameters)
    elif cmd == "disconnect_channel":
        await disconnect_chanel_cmd(message)
    else:
        await message.channel.send("Я такой команды не знаю 😕")


@client.event
async def on_ready():
    print("Дискорд бот успешно запущен!")


async def translate_message(message):
    for channel_couple in global_registred_chanels:
            channe_1 = channel_couple["channel_1"]
            channe_2 = channel_couple["channel_2"]
            ic(channe_1)
            ic(message.channel.id)
            if channe_1 == str(message.channel.id):
                if not message.content:
                    text = "Нечего переводить, пустое сообщение / Nothing to translate, empty message "
                else:
                    text = translator.translate(message.content, dest="en").text

                author = message.author
                embed = discord.Embed(color=discord.Color.blue(), title="", description="")
                embed.add_field(name="Translated by Google", value=text, inline=False)
                embed.set_author(name=author.name, icon_url=str(author.avatar_url))
                embed.set_footer(text=f"via #{message.channel.name}")
                channel = client.get_channel(int(channe_2))
                await channel.send(embed=embed)
            elif channe_2 == str(message.channel.id):
                if not message.content:
                    text = "Нечего переводить, пустое сообщение / Nothing to translate, empty message "
                else:
                    text = translator.translate(message.content, dest="ru").text

                author = message.author
                embed = discord.Embed(color=discord.Color.blue(), title="", description="")
                embed.add_field(name="Translated by Google", value=text, inline=False)
                embed.set_author(name=author.name, icon_url=str(author.avatar_url))
                embed.set_footer(text=f"via #{message.channel.name}")

                if len(message.attachments) > 0:
                    for attach in message.attachments:
                        embed.set_image(url=attach.url)

                channel = client.get_channel(int(channe_1))
                await channel.send(embed=embed)


async def connect_chanel_cmd(message, parameters):
    if not parameters or len(parameters) != 2:
        await message.channel.send("Укажите пожалуйста параметры команды по синтаксису: connect_channel <1_канал> <2_канал>")
    elif len(parameters) == 2:
        normalized_parametrs = []

        for parameter in parameters:
            norm_params = parameter.replace("#", "")
            norm_params = norm_params.replace("<", "")
            norm_params = norm_params.replace(">", "")
            normalized_parametrs.append(norm_params)

        connect_channel_data = {"channel_1": normalized_parametrs[0], "channel_2": normalized_parametrs[1]}
        global_registred_chanels.append(connect_channel_data)
        await message.channel.send("Каналы успешно зарегистрированы в базе!")
        ic(connect_channel_data)


async def disconnect_chanel_cmd(message):
    pass


"""
@bot.command()
async def test1(ctx):
    embed = discord.Embed(
        title="Привет всем!",
    )
    await ctx.send(embed=embed)

@bot.command()
async def lolzsait(ctx):
    embed = discord.Embed(
        title="Тык для перехода",
        description="Ссылка для перехода на lolz",
        url='https://lolz.guru',
    )
    await ctx.send(embed=embed)

"""
client.run(TOKEN)
# bot.run(TOKEN)
