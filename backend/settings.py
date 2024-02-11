import os

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
        port=int(os.getenv("BACKEND_PORT", 8000)),
        db_path="./db/database.sqlite",
        login=os.getenv("LOGIN", "login"),
        password=os.getenv("PASSWORD", "password"),
    )
