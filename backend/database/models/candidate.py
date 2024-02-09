from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base import AlchemyBaseModel


class Candidate(AlchemyBaseModel):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    surname: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    gender: Mapped[Optional[bool]] = mapped_column(
        Boolean(),
        nullable=True,
        default=True,
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
        default="candidate.png",
    )
    votes: Mapped[Optional[int]] = mapped_column(Integer, nullable=False, default=0)
