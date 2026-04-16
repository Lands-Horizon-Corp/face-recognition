from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from app.core.base import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.domains.user import UsersInfo


class Directions(enum.Enum):
    FRONT = 'front'
    LEFT = 'left'
    RIGHT = 'right'


class Faces(Base):
    __tablename__ = 'faces'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text('gen_random_uuid()')
    )

    users_info_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users_info.id')
    )

    direction: Mapped[Directions] = mapped_column(
        Enum(Directions, values_callable=lambda obj: [e.value for e in obj]))

    embeddings: Mapped[str] = mapped_column(Vector(512))

    users_info: Mapped[UsersInfo] = relationship(back_populates='faces')
