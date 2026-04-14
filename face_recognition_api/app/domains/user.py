from __future__ import annotations

from app.core.db import Base
from sqlalchemy import Column
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UsersInfo(Base):
    __tablename__ = 'users_info'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True))
    group_id = Column(UUID(as_uuid=True))

    faces = relationship('Faces', back_populates='users_info')
