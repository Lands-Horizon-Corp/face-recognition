from __future__ import annotations

import numpy as np
from app.domains.faces import Faces
from app.domains.user import UserSimilarityResult
from app.domains.user import UsersInfo
from sqlalchemy import text
from sqlalchemy.orm import Session


def create_user(db: Session,
                user_id: str,
                group_id: str,
                direction: str,
                embeddings: np.ndarray,
                metadata: dict | None) -> UsersInfo:

    db_user = db.query(UsersInfo).filter(UsersInfo.user_id == user_id).first()
    if not db_user:
        db_user = UsersInfo(
            user_id=user_id, group_id=group_id, user_metadata=metadata)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    db_face = Faces(users_info_id=db_user.id,
                    direction=direction,
                    embeddings=embeddings.tolist())
    db.add(db_face)
    db.commit()
    db.refresh(db_face)

    return db_user


def get_user_by_embedding(db: Session,
                          embeddings: np.ndarray,
                          group_id: str | None = None) -> UserSimilarityResult | None:  # noqa: E501

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

    query += """
        ORDER BY similarity DESC
        LIMIT 5;
    """
    result = db.execute(text(query), {'embeddings': embeddings.tolist(), 'group_id': group_id}).fetchone()  # noqa: E501
    if result:
        return UserSimilarityResult.model_validate(result, from_attributes=True)
    return None
