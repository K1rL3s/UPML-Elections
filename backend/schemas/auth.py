from backend.schemas.base import BaseSchema


class AuthSchema(BaseSchema):
    login: str
    password: str
