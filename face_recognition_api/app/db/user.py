from __future__ import annotations

from app.models.user import User
from sqlalchemy.orm import Session


def create_user(db: Session, user_id: str, branch_id: str, embedding: str):
    db_user = User(user_id=user_id, branch_id=branch_id, embedding=embedding)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_user_by_embedding(db: Session, embedding: str):
    query = """
    SELECT 1 - (embedding <=> :embedding) AS similarity
    FROM items;
    """
    db.execute(query, {'embedding': embedding}).fetchone()
