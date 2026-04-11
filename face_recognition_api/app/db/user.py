from __future__ import annotations

from app.domains.faces import Faces
from app.domains.user import UsersInfo
from sqlalchemy.orm import Session


def create_user(db: Session,
                user_id: str,
                group_id: str,
                embeddings: dict[str, str]) -> UsersInfo:
    db_user = UsersInfo(user_id=user_id, group_id=group_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    for direction, embedding in embeddings.items():
        db_face = Faces(users_info_id=db_user.id,
                        direction=direction,
                        embeddings=embedding)
        db.add(db_face)
        db.commit()
        db.refresh(db_face)

    return db_user


def get_user_by_embedding(db: Session, embeddings: str, group_id: str | None = None) -> UsersInfo | None:  # noqa: E501
    query = """
    SELECT 1 - (embeddings <=> :embeddings) AS similarity
    FROM faces
    JOIN users_info ON faces.users_info_id = users_info.id;

    """
    if group_id is not None:
        query += ' WHERE group_id = :group_id'
    return db.execute(query, {'embeddings': embeddings, 'group_id': group_id}).fetchone()
