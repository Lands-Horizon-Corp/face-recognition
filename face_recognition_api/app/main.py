from __future__ import annotations

from app.api.base_routes import base_route
from app.core import startup
from app.core.config import settings
from app.core.db import engine
from app.core.security import limiter
from app.domains import Base
from robyn import Request
from robyn import Response
from robyn import Robyn

from face_recognition_api.app.core.middleware import resolve_origin
Base.metadata.create_all(bind=engine)

ALLOWED_HEADERS = (
    'Content-Type, Accept, Authorization, Location, '
    'X-Organization-Id, X-User-Agent, X-Device-Type, X-CSRF-Token'
)
ALLOWED_METHODS = 'GET, POST, OPTIONS'

app = Robyn(__file__, openapi_file_path=settings.OPENAPI_PATH)

app.include_router(base_route)


@app.before_request()
def intercept_and_limit(req: Request):

    print(f'Incoming request: {req.method} {req}')

    req_origin = req.headers.get('origin') or ''
    matched_origin = resolve_origin(req_origin)
    print(f"Matched origin: '{matched_origin}'",
          f" for request origin: '{req_origin}'")

    if req.method == 'OPTIONS':
        return Response(
            status_code=204,
            description='',
            headers={
                'Access-Control-Allow-Origin': matched_origin,
                'Access-Control-Allow-Headers': ALLOWED_HEADERS,
                'Access-Control-Allow-Methods': ALLOWED_METHODS,
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '86400',
            },
        )
    return limiter.handle_request(app, req)


@app.startup_handler
async def run_on_startup():
    print('Running startup tasks...')
    await startup.download_models()


if __name__ == '__main__':
    app.start(host='0.0.0.0', port=8080)
