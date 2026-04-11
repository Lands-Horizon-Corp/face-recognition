from __future__ import annotations

from app.models.user import User
from sqlalchemy.orm import Session


def create_user(db: Session, user_id: str, group_id: str, embeddings: str):
    db_user = User(user_id=user_id, group_id=group_id, embeddings=embeddings)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_embedding(db: Session, embeddings: str):
    query = """
    SELECT 1 - (embeddings <=> :embeddings) AS similarity
    FROM items;

    """
    # WHERE GROUP_ID = GROUP_ID
    return db.execute(query, {'embeddings': embeddings}).fetchone()
