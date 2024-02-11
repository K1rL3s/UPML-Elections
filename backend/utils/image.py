from pathlib import Path

from fastapi import UploadFile

IMAGES_DIR = (Path(__file__).parent.parent / "images").resolve()


def save_image(image: UploadFile, candidate_id: int) -> str:
    filename = f"{candidate_id}.{image.filename.split('.')[-1]}"

    with open(IMAGES_DIR / filename, "wb") as file_object:
        file_object.write(image.file.read())

    return filename
