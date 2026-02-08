from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.modules.heroes.router import heroes_router
from app.modules.players.router import player_router

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    title=settings.APP_NAME,
    version=settings.VERSION,
)


app.include_router(
    router=heroes_router,
    prefix="/api",
)

app.include_router(
    router=player_router,
    prefix="/api",
)


@app.get("/scalar")
def scalar_doc():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
