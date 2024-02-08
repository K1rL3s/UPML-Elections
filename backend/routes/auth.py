from uuid import uuid4

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.database import get_session_return, get_session_yield
from backend.database.models import AuthToken
from backend.schemas import AuthSchema
from backend.settings import get_settings


router = APIRouter()


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(
    auth: AuthSchema,
    session: AsyncSession = Depends(get_session_yield)
) -> JSONResponse:
    settings = get_settings()
    if auth.login != settings.login or auth.password != settings.password:
        raise HTTPException(status_code=401, detail="Who are you?..")

    token = str(uuid4())
    auth_token = AuthToken(token=token)
    session.add(auth_token)
    await session.commit()

    return JSONResponse(content={"session_id": token})


async def is_auth_user(request: Request) -> None:
    session = await get_session_return()
    session_id = request.headers.get("Session-Id")
    auth_token = await session.scalar(
        sa.select(AuthToken).where(AuthToken.token == session_id)
    )
    if auth_token is None:
        raise HTTPException(status_code=401, detail="Who are you?..")
