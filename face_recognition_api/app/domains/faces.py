from __future__ import annotations

import enum

from app.core.db import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy import UUID
from sqlalchemy.orm import relationship


class Directions(enum.Enum):
    FRONT = 'front'
    LEFT = 'left'
    RIGHT = 'right'


class Faces(Base):
    __tablename__ = 'faces'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                server_default=text('gen_random_uuid()'))
    users_info_id = Column(UUID(as_uuid=True), ForeignKey('users_info.id'))
    direction = Column(Enum(Directions))
    embeddings = Column(Vector(512))

    users_info = relationship('UsersInfo', back_populates='faces')
