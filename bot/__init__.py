import os

TOKEN = os.environ.get("TOKEN")
assert TOKEN, "You don't specified Discord bot token"

import discord  # pycord
import asyncio
from discord.ext import commands
from loguru import logger
from translatepy.translators.yandex import YandexTranslate

from bot.models import Base, BaseModel
from bot.models.channel import Channel

from importlib import resources
import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import sessionmaker

# Initalialization SQLAlchemy connection
with resources.path("bot", "database.db") as sqlite_filepath:
    engine = sa.create_engine(f'sqlite:///{sqlite_filepath}', echo=False)

session = scoped_session(sessionmaker(bind=engine, autocommit=True))

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
BaseModel.set_session(session)

loop = asyncio.get_event_loop()


translator = YandexTranslate()
bot = commands.Bot()


@bot.event
async def on_ready():
    logger.info(f"Discord successfully started as {bot.user}!")
