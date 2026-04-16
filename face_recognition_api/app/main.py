from __future__ import annotations

from app.api.base_routes import base_route
from app.core import startup
from app.core.config import settings
from app.core.db import engine
from app.core.security import limiter
from app.domains import Base
from robyn import ALLOW_CORS
from robyn import Request
from robyn import Robyn
Base.metadata.create_all(bind=engine)

app = Robyn(__file__, openapi_file_path=settings.OPENAPI_PATH)
ALLOW_CORS(app, origins=settings.CORS_ALLOW_ORIGINS)
app.include_router(base_route)


@app.before_request()
def middleware(request: Request):
    return limiter.handle_request(app, request)


@app.startup_handler
async def run_on_startup():
    print('Running startup tasks...')
    await startup.download_models()


if __name__ == '__main__':
    app.start(host='0.0.0.0', port=8080)
