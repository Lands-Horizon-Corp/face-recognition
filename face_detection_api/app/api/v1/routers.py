from __future__ import annotations

from app.api.v1.endpoints import face_recognition_routes
from robyn import SubRouter

v1_router = SubRouter(__file__, prefix='/api/v1')

# URL becomes /api/v1/face/detect
v1_router.include_router(face_recognition_routes.router)


@v1_router.get('/ping')
async def ping():
    return {'ping': 'pong'}
