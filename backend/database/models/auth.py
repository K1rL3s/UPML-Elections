from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base import AlchemyBaseModel


class AuthToken(AlchemyBaseModel):
    __tablename__ = "auth_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    token: Mapped[str] = mapped_column(String(36), nullable=False)
