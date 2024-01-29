from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CandidateCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, gt=0)
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    patronymic: str = Field(max_length=32)
    image: str = Field(max_length=32)
    votes: Optional[int] = Field(default=0)


class CandidateUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(gt=0)
    name: Optional[str] = Field(max_length=32)
    surname: Optional[str] = Field(max_length=32)
    patronymic: Optional[str] = Field(max_length=32)
    image: Optional[str] = Field(max_length=32)
    votes: Optional[int]
