from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from backend.settings import get_settings
from backend.database.db_session import database_init
from backend.routes import candidates


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await database_init(settings)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(candidates.router, tags=["Candidates"])


def main():
    settings = get_settings()
    uvicorn.run(app=app, host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    main()
