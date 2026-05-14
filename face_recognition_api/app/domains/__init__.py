# Import the Base
from __future__ import annotations

from face_recognition_api.app.core.base import Base
from face_recognition_api.app.domains.faces import Faces
from face_recognition_api.app.domains.user import UsersInfo
# Import all your models

# Expose them so other parts of the app can import them cleanly from 'app.domains'
__all__ = ['Base', 'Faces', 'UsersInfo']
