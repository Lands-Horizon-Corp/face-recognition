from __future__ import annotations

import numpy as np
from app.domains.faces import Faces
from app.domains.user import UsersInfo
from PIL.ImageCms import Direction
from sqlalchemy import text
from sqlalchemy.orm import Session


def create_user(db: Session,
                user_id: str,
                group_id: str,
                embeddings: dict[Direction, str]) -> UsersInfo:
    db_user = UsersInfo(user_id=user_id, group_id=group_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    for direction, embedding in embeddings.items():
        db_face = Faces(users_info_id=db_user.id,
                        direction=direction.value,
                        embeddings=embedding)
        db.add(db_face)
        db.commit()
        db.refresh(db_face)

    return db_user


def get_user_by_embedding(db: Session, embeddings: np.ndarray, group_id: str | None = None) -> UsersInfo | None:  # noqa: E501

    query = """SELECT
            users_info.id,
            users_info.user_id,
            users_info.group_id,
            users_info.user_metadata,
            1 - (faces.embeddings <=> CAST(:embeddings AS vector)) AS similarity
        FROM faces
        JOIN users_info ON faces.users_info_id = users_info.id
    """
    if group_id is not None:
        query += ' WHERE group_id = :group_id;'
    else:
        query += ';'
    return db.execute(text(query), {'embeddings': embeddings.tolist(), 'group_id': group_id}).fetchone()  # noqa: E501
