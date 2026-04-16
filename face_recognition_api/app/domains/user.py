from __future__ import annotations

import uuid
from typing import Any
from typing import TYPE_CHECKING

from app.core.base import Base
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.domains.faces import Faces


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
