from __future__ import annotations

import io

import numpy as np
from huggingface_hub import snapshot_download
from insightface.app import FaceAnalysis
from PIL import Image
snapshot_download(
    'fal/AuraFace-v1',
    local_dir='models/auraface',
)
face_app = FaceAnalysis(
    name='auraface',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider'],
    root='.',
)

face_app.prepare(ctx_id=0, det_size=(640, 640))


def create_embedding(image: Image) -> np.ndarray:
    cv2_image = np.array(image.convert('RGB'))
    cv2_image = cv2_image[:, :, ::-1]
    faces = face_app.get(cv2_image)
    embedding = faces[0].normed_embedding
    return embedding


if __name__ == '__main__':
    with open('./src/face_recognition/test_image.jpg', 'rb') as f:
        img_bytes = f.read()
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    embedding = create_embedding(img)
    print(embedding)
