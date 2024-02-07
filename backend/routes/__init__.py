from fastapi import FastAPI

from .candidates import router as candidates_router
from .results import router as results_router


def include_routers(app: FastAPI) -> None:
    for router in (
        candidates_router,
        results_router,
    ):
        app.include_router(router)
