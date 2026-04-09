from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    USER_NOT_FOUND = 'ERR_USER_NOT_FOUND'
    INVALID_IMAGE = 'ERR_INVALID_IMAGE'
    MISSING_USER_OR_BRANCH_ID = 'ERR_MISSING_USER_OR_BRANCH_ID'


class HTTPStatusCode(int, Enum):
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    OK = 200
