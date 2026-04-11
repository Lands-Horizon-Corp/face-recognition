from __future__ import annotations

from app.core.db import Base
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'user_faces'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True,
                server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True))
    branch_id = Column(UUID(as_uuid=True))
    embeddings = Column(Vector(512))
