from __future__ import annotations

import cv2
import numpy as np
from huggingface_hub import snapshot_download
from insightface.app import FaceAnalysis

snapshot_download(
    'fal/AuraFace-v1',
    local_dir='models/auraface',
)
face_app = FaceAnalysis(
    name='auraface',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
    root='.',
)

input_image = cv2.imread('test.png')

cv2_image = np.array(input_image.convert('RGB'))

cv2_image = cv2_image[:, :, ::-1]
faces = face_app.get(cv2_image)
embedding = faces[0].normed_embedding


def create_embedding(image: bytes) -> str:
    input_image = cv2.imread(image)
    cv2_image = np.array(input_image.convert('RGB'))
    cv2_image = cv2_image[:, :, ::-1]
    faces = face_app.get(cv2_image)
    embedding = faces[0].normed_embedding
    return embedding
