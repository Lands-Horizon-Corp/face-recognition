from __future__ import annotations

from filetype import filetype
from robyn import Request


def is_image_file(file: bytes) -> bool:
    """Check if the uploaded file is an image based on its content type."""

    file_Info = filetype.guess(file)
    return file_Info is not None and file_Info.mime.startswith('image/')


def get_image(request: Request):
    files = request.files
    file_names = list(files.keys())
    first_key = file_names[0]
    if not is_image_file(files[first_key]):
        return None
    return files[first_key]
