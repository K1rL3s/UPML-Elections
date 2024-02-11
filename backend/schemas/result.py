from typing import Optional

from pydantic import Field

from backend.schemas.base import BaseSchema


class ResultRead(BaseSchema):
    is_end: bool = Field(default=False)
    is_show_votes: bool = Field(default=False)
    winner_name: Optional[str] = Field(default=None, max_length=32)
    winner_surname: Optional[str] = Field(default=None, max_length=32)
    winner_gender: Optional[bool] = Field(default=True)


class ResultUpdate(BaseSchema):
    is_end: bool = Field()
    is_show_votes: bool = Field()
