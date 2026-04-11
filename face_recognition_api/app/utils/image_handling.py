from __future__ import annotations

import io

from filetype import filetype
from PIL import Image
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


def open_image(upload_file: bytes) -> Image:
    try:
        image = Image.open(io.BytesIO(upload_file)).convert('RGB')
        # Save the image for debugging purposes
        # image.save('./spoofing_detection_api/debug_image.jpg')
    except Exception as e:
        raise ValueError(
            f"Invalid image file, file type detected:"
            f" {type(upload_file)}") from e
    return image
