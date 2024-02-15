from typing import Optional

import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database.db_session import get_session
from backend.database.models import Candidate, Result
from backend.schemas import ResultRead, ResultUpdate
from backend.settings import get_settings
from backend.utils.auth import authed_user
from backend.utils.percent import round_percents

router = APIRouter()


@router.get("/result", status_code=status.HTTP_200_OK)
async def is_end(session: AsyncSession = Depends(get_session)) -> ResultRead:
    result = await session.scalar(sa.select(Result))
    return ResultRead.model_validate(result, from_attributes=True)


@router.put("/result", status_code=status.HTTP_200_OK)
async def end_toggle(
    result_update: ResultUpdate,
    session: AsyncSession = Depends(get_session),
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
    session: AsyncSession = Depends(get_session),
) -> Optional[list[tuple[int, float]]]:
    query = sa.select(Candidate).order_by(Candidate.id)
    candidates = list(await session.scalars(query))

    result = await session.scalar(sa.select(Result))
    voted = sum(c.votes for c in candidates)

    if result.is_end or result.is_show_votes:
        if not voted:
            return []
        percents = [c.votes / voted * 100 for c in candidates]
        rounded_percents = round_percents(percents)
        return [(c.id, rounded_percents[i]) for i, c in enumerate(candidates)]


# Возвращает
# (процент проголосовавших, проголосовавшие)
# (100% - процент проголосовавших, все голоса минус проголосовавшие)
@router.get("/votes", status_code=status.HTTP_200_OK)
async def votes_count(
    session: AsyncSession = Depends(get_session),
) -> tuple[tuple[float, int], tuple[float, int]]:
    voted = await session.scalar(sa.select(sa.func.sum(Candidate.votes))) or 0
    all_votes = get_settings().all_votes
    voted_percent = voted / all_votes * 100
    unvoted_percent = 100 - voted_percent

    voted_percent, unvoted_percent = round_percents([voted_percent, unvoted_percent])

    return (voted_percent, voted), (unvoted_percent, all_votes - voted)
