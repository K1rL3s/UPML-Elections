import os

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    port: int
    db_path: str


def get_settings() -> Settings:
    load_dotenv()
    return Settings(
        port=os.environ["BACKEND_PORT"],
        db_path=os.environ["db_path"],
    )
