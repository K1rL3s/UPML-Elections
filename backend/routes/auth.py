from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from backend.database import get_session
from backend.database.models import AuthToken
from backend.schemas import AuthSchema
from backend.settings import get_settings
from backend.utils.auth import authed_user

router = APIRouter()


@router.get("/login", status_code=status.HTTP_200_OK)
async def login_check(request: Request) -> None:
    await authed_user(request)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    auth: AuthSchema, session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    settings = get_settings()
    if auth.login != settings.login or auth.password != settings.password:
        raise HTTPException(status_code=401, detail="Who are you?..")

    token = str(uuid4())
    auth_token = AuthToken(token=token)
    session.add(auth_token)
    await session.commit()

    return JSONResponse(content={"session_id": token})
