from typing import Optional

import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database.db_session import get_session_yield
from backend.database.models import Candidate, Result
from backend.schemas import ResultRead, ResultUpdate
from backend.utils.auth import authed_user

router = APIRouter()


@router.get("/result", status_code=status.HTTP_200_OK)
async def is_end(session: AsyncSession = Depends(get_session_yield)) -> ResultRead:
    result = await session.scalar(sa.select(Result))
    return ResultRead.model_validate(result, from_attributes=True)


@router.put("/result", status_code=status.HTTP_200_OK)
async def end_toggle(
    result_update: ResultUpdate,
    session: AsyncSession = Depends(get_session_yield),
    user: None = Depends(authed_user),
) -> ResultRead:
    result = await session.scalar(sa.select(Result))
    result.is_end = result_update.is_end
    result.is_show_votes = result_update.is_end or result_update.is_show_votes

    if result.is_end:
        candidates = await session.scalars(sa.select(Candidate))
        candidate = max(candidates, key=lambda c: c.votes)

        result.winner_name = candidate.name
        result.winner_surname = candidate.surname
        result.winner_gender = candidate.gender
    else:
        result.winner_name = None
        result.winner_surname = None
        result.winner_gender = None

    await session.commit()

    return ResultRead.model_validate(result, from_attributes=True)


@router.get("/percentage", status_code=status.HTTP_200_OK)
async def percentage(
    session: AsyncSession = Depends(get_session_yield),
) -> Optional[list[tuple[int, float]]]:
    query = sa.select(Candidate).order_by(Candidate.id)
    candidates = list(await session.scalars(query))

    result = await session.scalar(sa.select(Result))
    voted = sum(c.votes for c in candidates)

    if result.is_end or result.is_show_votes:
        return [(c.id, c.votes / voted * 100) for c in candidates] if voted else []


@router.get("/votes", status_code=status.HTTP_200_OK)
async def votes_count(
    session: AsyncSession = Depends(get_session_yield),
) -> Optional[int]:
    query = sa.select(sa.func.sum(Candidate.votes))
    return await session.scalar(query)
