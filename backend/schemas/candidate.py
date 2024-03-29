from typing import Optional

from pydantic import Field

from backend.schemas.base import BaseSchema


class CandidateCreate(BaseSchema):
    name: Optional[str] = Field(default=None, max_length=32)
    surname: Optional[str] = Field(default=None, max_length=32)
    gender: Optional[bool] = Field(default=True)
    image: Optional[str] = Field(default=None, max_length=64)
    votes: Optional[int] = Field(default=0)


class CandidateRead(BaseSchema):
    id: int = Field(gt=0)
    name: Optional[str] = Field(max_length=32)
    surname: Optional[str] = Field(max_length=32)
    gender: Optional[bool] = Field(default=True)
    image: Optional[str] = Field(max_length=64)
    votes: Optional[int] = Field(default=0)
