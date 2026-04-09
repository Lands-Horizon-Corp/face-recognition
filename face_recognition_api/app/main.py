from __future__ import annotations

from app.api.base_routes import base_route
from app.core.config import settings
from robyn import Robyn
app = Robyn(__file__, openapi_file_path=settings.OPENAPI_PATH)

app.include_router(base_route)

if __name__ == '__main__':
    app.start(host='0.0.0.0', port=8001)
