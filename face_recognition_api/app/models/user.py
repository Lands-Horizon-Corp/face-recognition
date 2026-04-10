from __future__ import annotations

from app.core.db import Base
from sqlalchemy import Column
from sqlalchemy import String


class User(Base):
    __tablename__ = 'user_faces'

    user_id = Column(String)
    branch_id = Column(String)
    embedding = Column(String)
