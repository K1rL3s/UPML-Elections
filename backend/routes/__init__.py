from fastapi import FastAPI

from .auth import router as auth_router
from .candidates import router as candidates_router
from .results import router as results_router


def include_routers(app: FastAPI) -> None:
    for router in (
        auth_router,
        candidates_router,
        results_router,
    ):
        app.include_router(router)
