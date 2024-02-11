from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

IMAGES_DIR = (Path(__file__).parent.parent / "images").resolve()


def save_image(image: UploadFile) -> str:
    filename = f"{str(uuid4())}.{image.filename.split('.')[-1]}"

    with open(IMAGES_DIR / filename, "wb") as file_object:
        file_object.write(image.file.read())

    return filename
