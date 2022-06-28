import discord
from discord import option
from icecream import ic
from loguru import logger

from sqlalchemy.exc import IntegrityError

from bot import bot, TOKEN
from bot.models.channel import Channel

# Error: discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction
# Explanation: If your processing takes more than 3 seconds the interaction expires unless you defer



@bot.slash_command(name="connect_channel", description="Connect channels to translators/ Подключить каналы к переводчику")
@option("russian_channel", discord.TextChannel, description="Select a Russian-language channel / Выберите русскоязычный канал")
@option("english_channel", discord.TextChannel, description="Select a English-language channel / Выберите англоязычный канал")
async def connect_chanel_cmd(ctx: discord.ApplicationContext, russian_channel: discord.TextChannel, english_channel: discord.TextChannel):
    try:
        channel = Channel.create(channel_id=ctx.interaction.channel_id, russian_channel_id=russian_channel.id, english_channel_id=english_channel.id)
    except IntegrityError:
        ic(1)
        message_text = [
            "Ошибка! Один из каналов уже зарегистрирован в базе"
        ]
    except Exception as ex:
        ic(2)
        message_text = [
            f"Ошибка! {ex}"
        ]
    else:
        ic(3)
        message_text = [
            f"Каналы '{russian_channel.mention}' и '{english_channel.mention}' успешно заригестрированы в базе переводчика",
        ]
    ic(ctx.interaction)
    ic(ctx.command)
    ic(english_channel.__repr__)
    await ctx.respond("\n".join(message_text))



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


bot.run(TOKEN)
