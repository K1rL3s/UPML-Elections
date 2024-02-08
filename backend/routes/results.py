import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from backend.database.db_session import get_session_yield
from backend.database.models import Candidate, Result
from backend.schemas import ResultRead
from backend.routes.auth import is_auth_user


router = APIRouter()


@router.get("/end/", status_code=status.HTTP_200_OK)
async def is_end(session: AsyncSession = Depends(get_session_yield)) -> ResultRead:
    result = await session.scalar(sa.select(Result))
    return ResultRead.model_validate(result, from_attributes=True)


@router.post("/end/", status_code=status.HTTP_200_OK)
async def end_toggle(
    session: AsyncSession = Depends(get_session_yield),
    user: None = Depends(is_auth_user),
) -> ResultRead:
    result = await session.scalar(sa.select(Result))
    result.is_end = not result.is_end

    if result.is_end:
        candidates = await session.scalars(sa.select(Candidate))
        candidate = max(candidates, key=lambda c: c.votes)

        result.winner_name = candidate.name
        result.winner_surname = candidate.surname
        result.winner_patronymic = candidate.patronymic
        result.winner_gender = candidate.gender
    else:
        result.winner_name = None
        result.winner_surname = None
        result.winner_patronymic = None
        result.winner_gender = None

    await session.commit()

    return ResultRead.model_validate(result, from_attributes=True)
