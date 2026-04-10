from __future__ import annotations

from app.api.base_routes import base_route
from app.core.config import settings
from app.core.security import limiter
from robyn import ALLOW_CORS
from robyn import Request
from robyn import Robyn

app = Robyn(__file__, openapi_file_path=settings.OPENAPI_PATH)
ALLOW_CORS(app, origins=settings.CORS_ALLOW_ORIGINS)
app.include_router(base_route)


@app.before_request()
def middleware(request: Request):
    return limiter.handle_request(app, request)


if __name__ == '__main__':
    app.start(host='0.0.0.0', port=8080)
