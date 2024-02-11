import sqlalchemy as sa
from fastapi import HTTPException
from starlette.requests import Request

from backend.database import get_session_return
from backend.database.models import AuthToken


async def authed_user(request: Request) -> None:
    session = await get_session_return()

    try:
        session_id = request.headers.get("Session-Id")
        auth_token = await session.scalar(
            sa.select(AuthToken).where(AuthToken.token == session_id)
        )
        if auth_token is None:
            raise HTTPException(status_code=401, detail="Who are you?..")
    finally:
        await session.close()


async def is_auth_user(request: Request) -> bool:
    try:
        await authed_user(request)
        return True
    except HTTPException:
        return False
