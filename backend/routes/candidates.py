from fastapi import APIRouter, Depends, HTTPException
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database.db_session import get_session
from backend.database.models import Candidate
from backend.schemas.candidate import (
    CandidateCreate,
    CandidateUpdateSchema,
)


router = APIRouter(tags=["Candidates"])


@router.get("/candidates/{candidate_id}", status_code=status.HTTP_200_OK)
async def candidates_get_one(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
) -> CandidateCreate:
    query = sa.select(Candidate).where(Candidate.id == candidate_id)
    candidate = await session.scalar(query)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    return CandidateCreate.model_validate(candidate)


@router.get("/candidates", status_code=status.HTTP_200_OK)
async def candidates_get_all(
    session: AsyncSession = Depends(get_session),
) -> list[CandidateCreate]:
    query = sa.select(Candidate)
    candidates = await session.scalars(query)

    return [
        CandidateCreate.model_validate(candidate, from_attributes=True)
        for candidate in candidates
    ]


@router.post("/candidates", status_code=status.HTTP_201_CREATED)
async def candidates_create(
    candidate: CandidateCreate,
    session: AsyncSession = Depends(get_session),
) -> CandidateCreate:
    query = sa.select(Candidate).where(
        Candidate.name == candidate.name,
        Candidate.surname == candidate.surname,
        Candidate.patronymic == candidate.patronymic,
    )
    if await session.scalar(query):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This candidate is already exists",
        )

    candidate = Candidate(
        name=candidate.name,
        surname=candidate.surname,
        patronymic=candidate.patronymic,
    )
    session.add(candidate)
    await session.commit()

    return CandidateCreate.model_validate(candidate, from_attributes=True)


@router.put("/candidates", status_code=status.HTTP_200_OK)
async def candidates_update(
    candidate: CandidateUpdateSchema,
    session: AsyncSession = Depends(get_session),
) -> CandidateUpdateSchema:
    candidate_dump = candidate.model_dump()
    del candidate_dump["id"]

    query = sa.select(Candidate)
    if candidate.id is not None:
        query = query.where(Candidate.id == candidate.id)
    else:
        query = query.where(
            Candidate.name == candidate.name,
            Candidate.surname == candidate.surname,
            Candidate.patronymic == candidate.patronymic,
        )

    candidate = await session.scalar(query)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found"
        )

    for k, v in candidate_dump.items():
        setattr(candidate, k, v)
    await session.commit()

    return CandidateUpdateSchema.model_validate(candidate, from_attributes=True)


@router.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def candidates_delete(
    candidate_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    query = sa.select(Candidate).where(Candidate.id == candidate_id)
    candidate = await session.scalar(query)

    if candidate:
        await session.delete(candidate)
        await session.commit()
