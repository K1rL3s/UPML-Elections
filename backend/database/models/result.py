from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base import AlchemyBaseModel


class Result(AlchemyBaseModel):
    __tablename__ = "result"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )

    is_end: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    winner_name: Mapped[Optional[str]] = mapped_column(
        String(32),
        default=None,
        nullable=True,
    )
    winner_surname: Mapped[Optional[str]] = mapped_column(
        String(32),
        default=None,
        nullable=True,
    )
    winner_patronymic: Mapped[Optional[str]] = mapped_column(
        String(32),
        default=None,
        nullable=True,
    )
    winner_gender: Mapped[Optional[bool]] = mapped_column(
        String(32),
        default=None,
        nullable=True,
    )
