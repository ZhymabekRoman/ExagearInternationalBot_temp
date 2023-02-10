import sqlalchemy as sa
from bot.models import BaseModel


class Channel(BaseModel):
    __tablename__ = 'channels'

    server_id = sa.Column(sa.Integer, nullable=False, index=True)
    english_channel_id = sa.Column(sa.Integer, nullable=False, index=True, unique=True)
    russian_channel_id = sa.Column(sa.Integer, nullable=False, index=True, unique=True)
