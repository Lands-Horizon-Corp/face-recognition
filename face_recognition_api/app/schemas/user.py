from __future__ import annotations

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    group_id: str
