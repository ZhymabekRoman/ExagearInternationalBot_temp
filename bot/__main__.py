import discord
from discord import option
from icecream import ic
from loguru import logger

from sqlalchemy.exc import IntegrityError

from bot import bot, translator, TOKEN
from bot.models.channel import Channel

# Error: discord.errors.NotFound: 404 Not Found (error code: 10062): Unknown interaction
# Explanation: If your processing takes more than 3 seconds the interaction expires unless you defer


@bot.slash_command(name="connect-channel", description="Connect channels to translators/ Подключить каналы к переводчику")
@option("russian_channel", discord.TextChannel, description="Select a Russian-language channel / Выберите русскоязычный канал")
@option("english_channel", discord.TextChannel, description="Select a English-language channel / Выберите англоязычный канал")
async def connect_chanel_cmd(ctx: discord.ApplicationContext, russian_channel: discord.TextChannel, english_channel: discord.TextChannel):
    ic(ctx)
    if russian_channel.id == english_channel.id:
        message_text = ["Ошибка! Вы пытаетесь зарегистрировать два одинаковых канала!"]
    else:
      try:
        channel = Channel.create(server_id=ctx.interaction.guild.id, russian_channel_id=russian_channel.id, english_channel_id=english_channel.id)
      except IntegrityError as ex:
        ic(ex)
        message_text = [
            "Ошибка! Один из каналов уже зарегистрирован в базе"
        ]
      except Exception as ex:
        message_text = [
            f"Ошибка! {ex}"
        ]
      else:
        message_text = [
            f"Каналы '{russian_channel.mention}' и '{english_channel.mention}' успешно заригестрированы в базе переводчика",
        ]
    await ctx.respond("\n".join(message_text))


@bot.slash_command(name="settings-translate", description="Settings / Настройки")
async def option_list(ctx):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.respond("You don't have admin permission")
        return

    await ctx.respond("Default translate service", view=SettingsView())


class SettingsView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Please select translate service",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Yandex",
                description="Accurate translate service",
                default=True
            ),
            discord.SelectOption(
                label="DeepL",
                description="Very accurate translate service, but has a lot limmitation by usage"
            ),
            discord.SelectOption(
                label="Google",
                description="Good old translate service"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

async def generate_embed(message, text):
    embed = discord.Embed(color=discord.Color.blue(), title="", description="")
    embed.add_field(name="Translated by Yandex", value=text, inline=False)
    embed.set_author(name=message.author.name)
    embed.set_footer(text=f"from #{message.channel.name}")

    if len(message.attachments) > 0:
        for attach in message.attachments:
            embed.set_image(url=attach.url)

    return embed


# async def translate_message(message):
@bot.event
async def on_message(message):
    ic(message)
    registred_chanels = Channel.where(server_id=message.guild.id).all()

    if not registred_chanels or message.author.bot:
        return

    nothing_to_translate_text = "Нечего переводить, пустое сообщение / Nothing to translate, empty message "
    for channel_couple in registred_chanels:
        ic(str(channel_couple))
        channe_1 = channel_couple.russian_channel_id
        channe_2 = channel_couple.english_channel_id
        if channe_1 == message.channel.id:
            ic(111111)
            if not message.content:
                text = nothing_to_translate_text
            else:
                text = translator.translate(message.content, "en", "ru").result

            embed = await generate_embed(message, text)

            channel = bot.get_channel(channe_2)
            await channel.send(embed=embed)
            return
        elif channe_2 == message.channel.id:
            ic(2222222222222)
            if not message.content:
                text = nothing_to_translate_text
            else:
                text = translator.translate(message.content, "ru", "en").result

            embed = await generate_embed(message, text)

            channel = bot.get_channel(channe_1)
            await channel.send(embed=embed)
            return


bot.run(TOKEN)
