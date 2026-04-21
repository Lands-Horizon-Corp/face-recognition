from __future__ import annotations

import json
import uuid

from app.core.contants import ErrorCode
from app.core.contants import HTTPStatusCode
from app.core.db import SessionLocal
from app.core.middleware import header_builder
from app.core.middleware import resolve_origin
from app.db.user import create_user
from app.db.user import get_user_by_embedding
from app.services.detect_face_service import face_detector
from app.utils.image_handling import get_image
from app.utils.image_handling import open_image
from face_recognition.aura_face import create_embedding
from robyn import Request
from robyn import Response
from robyn import SubRouter
from robyn.robyn import QueryParams
from robyn.types import FormData


router = SubRouter(__file__, prefix='/api/v1/face')


def parse_robyn_files(uploaded_files: dict, expected_keys: list) -> dict:
    result = {}
    for expected in expected_keys:
        match = next((k for k in uploaded_files.keys()
                     if expected in k.lower()), None)
        if match:
            result[expected] = uploaded_files[match]
    return result


@router.get('/health')
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    Returns a simple JSON response indicating the status of the API.
     - status: A string indicating the health status of the API (e.g., "ok").
    """
    return Response(
        status_code=HTTPStatusCode.OK.value,
        description=json.dumps({'status': 'ok'})
    )


@router.post('/add')
async def add_face(request: Request, form_data: FormData):
    """
    Add a new face embedding to the database. Expects an image file, user_id,
    and group_id in the form data.
     - user_id: A unique identifier for the user.
     - group_id: An identifier for the group associated with the user.
     - metadata: Additional json metadata about the user (optional).
     - image: An image file containing the face to be added.
     - direction: The direction of the face in the image (e.g., front, left, right).
    Returns the unique identifier of the newly created user or an error if the
     - id: The unique identifier for the newly created user.
    """
    origin = request.headers.get('origin')
    cors_req = request.headers.get('access-control-request-method')
    allowed_origin = resolve_origin(origin)
    headers = header_builder(allowed_origin, cors_req)
    user_id: str = form_data.get('user_id', None)
    group_id: str = form_data.get('group_id', None)
    direction: str = form_data.get('direction', None)
    metadata: str = form_data.get('metadata', None)

    if metadata:
        try:
            metadata = json.loads(metadata)
        except json.JSONDecodeError:
            return Response(
                headers=headers,
                status_code=HTTPStatusCode.BAD_REQUEST.value,
                description=json.dumps(
                    {'error': ErrorCode.INVALID_METADATA_FORMAT.value})
            )
    print(f"user_id: {user_id}",
          f"group_id: {group_id}")
    print('Files received:', request.files.keys())
    print('Form data received:', form_data.keys())
    if not user_id or not group_id:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps(
                {'error': ErrorCode.MISSING_USER_OR_GROUP_ID.value})
        )

    image = get_image(request)
    if not image:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps({'error': ErrorCode.INVALID_IMAGE.value})
        )

    img = open_image(image)
    faces = face_detector.find_faces(img)

    if not faces:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps(
                {'error': ErrorCode.NO_FACE.value})
        )

    if len(faces) > 1:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps(
                {'error': ErrorCode.MULTIPLE_FACES.value})
        )

    face = faces[0]
    left, top, right, bottom = face['bbox']
    face_image = img.crop((left, top, right, bottom))
    embeddings = create_embedding(face_image)

    with SessionLocal() as db:
        new_user = create_user(db, user_id, group_id,
                               direction, embeddings, metadata)

        if new_user is None:
            return Response(
                headers=headers,
                status_code=HTTPStatusCode.INTERNAL_SERVER_ERROR.value,
                description=json.dumps(
                    {'error': ErrorCode.FAILED_TO_CREATE_USER.value})
            )
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.OK.value,
            description=json.dumps({'id': str(new_user.id)})
        )


@router.post('/identify')
async def identify_face(request: Request, query_params: QueryParams):
    """
    Identify a face from the uploaded image. Expects an image file in the request.
     - image: An image file containing the face to be identified.
    Returns the user_id and group_id associated with the identified face,
    or an error if the face is not found or the image is invalid.
     - user_id: The unique identifier for the user associated with the identified face.
     - group_id: The identifier for the group associated with the identified face.
    """
    origin = request.headers.get('origin')
    cors_req = request.headers.get('access-control-request-method')
    allowed_origin = resolve_origin(origin)
    headers = header_builder(allowed_origin, cors_req)
    group_id = query_params.get('group_id', default=None)

    parsed_group_id = None
    if group_id:
        try:
            parsed_group_id = uuid.UUID(group_id)
        except ValueError:
            return Response(
                headers=headers,
                status_code=HTTPStatusCode.BAD_REQUEST.value,
                description=json.dumps({'error': 'Invalid group_id format'})
            )

    image = get_image(request)
    if not image:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps({'error': ErrorCode.INVALID_IMAGE.value})
        )
    image = open_image(image)
    faces = face_detector.find_faces(image)
    if not faces:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps({'error': ErrorCode.NO_FACE.value})
        )

    if len(faces) > 1:
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.BAD_REQUEST.value,
            description=json.dumps({'error': ErrorCode.MULTIPLE_FACES.value})
        )

    face = faces[0]
    left, top, right, bottom = face['bbox']
    face_image = image.crop((left, top, right, bottom))

    embeddings = create_embedding(face_image)
    with SessionLocal() as db:
        user = get_user_by_embedding(db, embeddings, parsed_group_id)
        if user is None:
            return Response(
                headers=headers,
                status_code=HTTPStatusCode.NOT_FOUND.value,
                description=json.dumps(
                    {'error': ErrorCode.USER_NOT_FOUND.value})
            )
        return Response(
            headers=headers,
            status_code=HTTPStatusCode.OK.value,
            description=json.dumps(
                {
                    'id': user.id,
                    'user_id': user.user_id,
                    'group_id': user.group_id,
                    'metadata': user.user_metadata
                }
            ))
