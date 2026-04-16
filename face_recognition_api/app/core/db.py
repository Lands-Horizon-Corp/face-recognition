from __future__ import annotations

from app.core.env import POSTGRES_DB
from app.core.env import POSTGRES_PASSWORD
from app.core.env import POSTGRES_PORT
from app.core.env import POSTGRES_USERNAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@postgres:{POSTGRES_PORT}/{POSTGRES_DB}'  # noqa: E501


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
