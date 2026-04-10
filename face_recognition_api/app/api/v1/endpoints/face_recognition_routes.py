from __future__ import annotations

from app.core.contants import ErrorCode
from app.core.contants import HTTPStatusCode
from app.core.db import SessionLocal
from app.db.user import create_user
from app.db.user import get_user_by_embedding
from app.services.detect_face_service import face_detector
from app.utils.image_handling import get_image
from face_recognition.aura_face import create_embedding
from robyn import Headers
from robyn import Request
from robyn import Response
from robyn import SubRouter
from robyn.types import FormData


router = SubRouter(__file__, prefix='/api/v1/face')


@router.post('/add')
async def add_face(request: Request, headers: Headers, form_data: FormData):
    """
    Add a new face embedding to the database. Expects an image file, user_id,
    and branch_id in the form data.
     - user_id: A unique identifier for the user.
     - branch_id: An identifier for the branch or location associated with the user.
     - image: An image file containing the face to be added.
    """
    response = Response(
        headers=headers,
        status_code=HTTPStatusCode.OK.value
    )

    image = get_image(request)
    if not image:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.INVALID_IMAGE.value}

    user_id: str = form_data.get('user_id', [None])[0]
    branch_id: str = form_data.get('branch_id', [None])[0]
    if not user_id or not branch_id:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.MISSING_USER_OR_BRANCH_ID.value}

    faces = face_detector.find_faces(image)

    if not faces:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.NO_FACE.value}

    if len(faces) > 1:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.MULTIPLE_FACES.value}

    face = faces[0]
    left, top, right, bottom = face['bbox']
    face_image = image.crop((left, top, right, bottom))

    embedding = create_embedding(face_image)
    with SessionLocal() as db:
        new_user = create_user(db, user_id, branch_id, embedding)

    if new_user is None:
        response.status_code = HTTPStatusCode.INTERNAL_SERVER_ERROR.value
        return {'error': 'Failed to create user'}


@router.post('/identify')
async def identify_face(request: Request, headers: Headers):
    """
    Identify a face from the uploaded image. Expects an image file in the request.
     - image: An image file containing the face to be identified.
    Returns the user_id and branch_id associated with the identified face,
    or an error if the face is not found or the image is invalid.
     - user_id: The unique identifier for the user associated with the identified face.
     - branch_id: The identifier for the branch or location associated
    """
    response = Response(
        headers=headers,
        status_code=HTTPStatusCode.OK.value
    )
    image = get_image(request)
    if not image:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.INVALID_IMAGE.value}

    faces = face_detector.find_faces(image)
    if not faces:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.NO_FACE.value}

    if len(faces) > 1:
        response.status_code = HTTPStatusCode.BAD_REQUEST.value
        return {'error': ErrorCode.MULTIPLE_FACES.value}

    face = faces[0]
    left, top, right, bottom = face['bbox']
    face_image = image.crop((left, top, right, bottom))

    embedding = create_embedding(face_image)
    with SessionLocal() as db:
        user = get_user_by_embedding(db, embedding)
    if user is None:
        return {'message': ErrorCode.USER_NOT_FOUND.value}
    return {'user_id': user.user_id, 'branch_id': user.branch_id}
