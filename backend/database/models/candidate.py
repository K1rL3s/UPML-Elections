from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base import AlchemyBaseModel


class Candidate(AlchemyBaseModel):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    surname: Mapped[str] = mapped_column(String(32), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(32), nullable=False)
    image: Mapped[str] = mapped_column(
        String(32), nullable=False, default="notfound.png"
    )
    votes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
