import sqlalchemy as sa
from bot.models import BaseModel


class Channel(BaseModel):
    __tablename__ = 'channels'

    channel_id = sa.Column(sa.Integer, nullable=False, index=True, primary_key=True)
    english_channel_id = sa.Column(sa.Integer, nullable=False, index=True, unique=True)
    russian_channel_id = sa.Column(sa.Integer, nullable=False, index=True, unique=True)
