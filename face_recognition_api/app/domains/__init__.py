# Import the Base
from __future__ import annotations

from app.core.base import Base
from app.domains.faces import Faces
from app.domains.user import UsersInfo
# Import all your models

# Expose them so other parts of the app can import them cleanly from 'app.domains'
__all__ = ['Base', 'Faces', 'UsersInfo']
