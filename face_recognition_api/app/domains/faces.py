from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy import text
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from face_recognition_api.app.core.base import Base

if TYPE_CHECKING:
    from face_recognition_api.app.domains.user import UsersInfo


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

    direction: Mapped[str] = mapped_column()

    embeddings: Mapped[str] = mapped_column(Vector(512))
    # test: Mapped[str] = mapped_column()

    users_info: Mapped[UsersInfo] = relationship(back_populates='faces')
