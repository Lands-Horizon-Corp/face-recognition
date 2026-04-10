from __future__ import annotations

from app.core.config import settings
from app.core.utils import DownloadFile


async def download_models():

    download_face_detector_model = DownloadFile(
        file_url=settings.FACE_DETECTOR_DOWNLOAD_URL_ENV,
        file_path=settings.FACE_DETECTOR_MODEL_PATH,
    )
    downloads = [download_face_detector_model]

    for download in downloads:
        if not download.check_file_exists():
            await download.execute()
        else:
            print(
                f'File {download.file_path} already exists, skipping download.')
