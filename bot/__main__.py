import os
import nextcord
from translatepy.translators.yandex import YandexTranslate
from icecream import ic

TOKEN = os.environ.get("TOKEN")

assert TOKEN is not None, "You dont specified Discord bot token"

translator = YandexTranslate()

client = nextcord.Client()

registred_chanels = []


@client.event
async def on_message(message):
    ic(message)
    ic(message.content)

    if message.author.bot:
        return

    if message.content.startswith('/bot_'):
        await processing_bot_commands(message)
    else:
        await translate_message(message)


async def processing_bot_commands(message):
    cmd = message.content.split()[0].replace("/bot_", "")
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

async def generate_embed(message, text):
    embed = nextcord.Embed(color=nextcord.Color.blue(), title="", description="")
    embed.add_field(name="Translated by Yandex", value=text, inline=False)
    embed.set_author(name=message.author.name)
    embed.set_footer(text=f"from #{message.channel.name}")
    
    if len(message.attachments) > 0:
        for attach in message.attachments:
            embed.set_image(url=attach.url)

    return embed


async def translate_message(message):
    nothing_to_translate_text = "Нечего переводить, пустое сообщение / Nothing to translate, empty message "
    for channel_couple in registred_chanels:
            channe_1 = channel_couple["channel_1"]
            channe_2 = channel_couple["channel_2"]
            if channe_1 == str(message.channel.id):
                if not message.content:
                    text = nothing_to_translate_text
                else:
                    text = translator.translate(message.content, "en", "ru").result
                
                embed = await generate_embed(message, text)

                channel = client.get_channel(int(channe_2))
                await channel.send(embed=embed)
                return
            elif channe_2 == str(message.channel.id):
                if not message.content:
                    text = nothing_to_translate_text
                else:
                    text = translator.translate(message.content, "ru", "en").result

                embed = await generate_embed(message, text)

                channel = client.get_channel(int(channe_1))
                await channel.send(embed=embed)
                return


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
        registred_chanels.append(connect_channel_data)
        await message.channel.send("Каналы успешно зарегистрированы в базе!")
        ic(connect_channel_data)


async def disconnect_chanel_cmd(message):
    ...


client.run(TOKEN)
