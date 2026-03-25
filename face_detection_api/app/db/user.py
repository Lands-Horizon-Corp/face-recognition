from __future__ import annotations

from app.models.user import User
from sqlalchemy.orm import Session


def get_user_by_embedding(db: Session, embedding: str):
    return db.query(User).filter(User.embedding == embedding).first()


def create_user(db: Session, user_id: str, branch_id: str, embedding: str):
    db_user = User(user_id=user_id, branch_id=branch_id, embedding=embedding)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
