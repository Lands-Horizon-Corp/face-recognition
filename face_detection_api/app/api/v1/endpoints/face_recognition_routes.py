from __future__ import annotations

from filetype import filetype
from robyn import Request
from robyn import Response
from robyn import SubRouter


router = SubRouter(__file__, prefix='/api/v1/face')


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


@router.post('/add')
async def add_face(request: Request, response: Response):
    image = get_image(request)
    if not image:
        response.status_code = 400
        return {'error': 'ERR_INVALID_IMAGE_FILE'}

    form = request.form_data
    user_id: str = form.get('user_id', [None])[0]
    branch_id: str = form.get('branch_id', [None])[0]
    if not user_id or not branch_id:
        response.status_code = 400
        return {'error': 'ERR_MISSING_USER_OR_BRANCH_ID'}


@router.post('/identify')
async def identify_face(request: Request, response: Response):
    image = get_image(request)
    if not image:
        response.status_code = 400
        return {'error': 'ERR_INVALID_IMAGE_FILE'}
