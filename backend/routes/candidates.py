from typing import Optional

import sqlalchemy as sa
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from backend.database.db_session import get_session_yield
from backend.database.models import Candidate, Result
from backend.schemas.candidate import CandidateCreate, CandidateRead
from backend.utils.auth import authed_user, is_auth_user
from backend.utils.image import save_image

router = APIRouter(tags=["Candidates"])


@router.get("/candidates", status_code=status.HTTP_200_OK)
async def candidates_get_all(
    request: Request,
    session: AsyncSession = Depends(get_session_yield),
) -> list[CandidateRead]:
    query = sa.select(Candidate).order_by(Candidate.id)

    candidates = [
        CandidateRead.model_validate(candidate, from_attributes=True)
        for candidate in await session.scalars(query)
    ]

    result = await session.scalar(sa.select(Result))
    authed = await is_auth_user(request)

    if not authed and not result.is_end and not result.is_show_votes:
        for candidate in candidates:
            candidate.votes = None

    return candidates


@router.get("/candidates/{candidate_id}", status_code=status.HTTP_200_OK)
async def candidates_get_one(
    request: Request,
    candidate_id: int,
    session: AsyncSession = Depends(get_session_yield),
) -> CandidateRead:
    query = sa.select(Candidate).where(Candidate.id == candidate_id)
    candidate_db = await session.scalar(query)

    if candidate_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    candidate = CandidateRead.model_validate(candidate_db, from_attributes=True)

    result = await session.scalar(sa.select(Result))
    authed = await is_auth_user(request)
    if not authed and not result.is_end and not result.is_show_votes:
        candidate.votes = None

    return candidate


@router.post("/candidates", status_code=status.HTTP_201_CREATED)
async def candidates_create(
    candidate: CandidateCreate,
    session: AsyncSession = Depends(get_session_yield),
    user: None = Depends(authed_user),
) -> CandidateRead:
    candidate = Candidate(
        name=candidate.name,
        surname=candidate.surname,
        gender=candidate.gender,
    )
    session.add(candidate)
    await session.commit()

    return CandidateRead.model_validate(candidate, from_attributes=True)


@router.put("/candidates", status_code=status.HTTP_200_OK)
async def candidates_update(
    candidate_id: int = Form(...),
    name: Optional[str] = Form(None),
    surname: Optional[str] = Form(None),
    gender: Optional[bool] = Form(None),
    image: Optional[UploadFile] = Form(None),
    votes: Optional[int] = Form(None),
    session: AsyncSession = Depends(get_session_yield),
    user: None = Depends(authed_user),
) -> CandidateRead:
    query = sa.select(Candidate).where(Candidate.id == candidate_id)
    candidate = await session.scalar(query)

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    candidate.name = name
    candidate.surname = surname
    candidate.gender = gender
    candidate.votes = votes or 0

    if image:
        filename = save_image(image, candidate_id)
        candidate.image = filename

    await session.commit()

    return CandidateRead.model_validate(candidate, from_attributes=True)


@router.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def candidates_delete(
    candidate_id: int,
    session: AsyncSession = Depends(get_session_yield),
    user: None = Depends(authed_user),
) -> None:
    query = sa.select(Candidate).where(Candidate.id == candidate_id)
    candidate = await session.scalar(query)

    if candidate:
        await session.delete(candidate)
        await session.commit()
