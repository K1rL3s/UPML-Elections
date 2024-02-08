import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    port: int
    db_path: str
    login: str
    password: str


def get_settings() -> Settings:
    return Settings(
        port=int(os.environ["BACKEND_PORT"]),
        db_path=os.environ["DB_PATH"],
        login=os.getenv("LOGIN", "login"),
        password=os.getenv("PASSWORD", "password")
    )
