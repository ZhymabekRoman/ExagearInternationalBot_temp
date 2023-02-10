from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType
import sqlalchemy as sa
import uuid


Base = declarative_base()


class BaseModel(Base, AllFeaturesMixin, TimestampsMixin):
    id = sa.Column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4
    )

    __abstract__ = True
