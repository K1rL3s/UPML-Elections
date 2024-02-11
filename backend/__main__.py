from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.database import database_init, init_result, manager_get_session
from backend.routes import include_routers
from backend.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await database_init(settings)

    async with manager_get_session() as session:
        await init_result(session)

    yield


app = FastAPI(lifespan=lifespan)
app.mount("/images", StaticFiles(directory="backend/images"), name="images")
include_routers(app)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    settings = get_settings()
    uvicorn.run(app=app, host="0.0.0.0", port=settings.port)


if __name__ == "__main__":
    main()
