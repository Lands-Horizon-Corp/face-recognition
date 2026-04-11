from __future__ import annotations

import os

import gdown
import requests  # type: ignore


class DownloadFile:
    def __init__(self, file_url: str, file_path: str):
        self.file_url = file_url
        self.file_path = file_path

    async def execute(self):

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if 'drive.google.com' in self.file_url:
            gdown.download(self.file_url, self.file_path, quiet=False)
        else:
            await download_file(self.file_url, self.file_path)

    def check_file_exists(self) -> bool:
        return os.path.isfile(self.file_path)


async def download_file(file_url: str, file_path: str):
    print(f'Downloading file {file_url} to {file_path}...')
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f'Model downloaded successfully to {file_path}')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading model: {e}')
