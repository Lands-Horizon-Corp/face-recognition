from __future__ import annotations

from app.db.db import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(String, index=True)
    embedding = Column(String)
