from __future__ import annotations

import uuid
from typing import Any
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from face_recognition_api.app.core.base import Base
if TYPE_CHECKING:
    from face_recognition_api.app.domains.faces import Faces


class UsersInfo(Base):
    __tablename__ = 'users_info'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        server_default=text('gen_random_uuid()')
    )
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    user_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)

    faces: Mapped[list[Faces]] = relationship(
        'Faces', back_populates='users_info')


class UserSimilarityResult(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    group_id: uuid.UUID
    user_metadata: dict[str, Any] | None
    similarity: float

    class Config:
        from_attributes = True
