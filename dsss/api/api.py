import asyncio

from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.requests import Request

from dsss.main import get_config
from dsss.engine.engine import Engine
import dsss.api.status
import dsss.api.admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    app.state.engine = Engine(config)
    app.state.engine_task = asyncio.create_task(app.state.engine.start())
    yield


app = FastAPI(lifespan=lifespan)

api = APIRouter()

api.include_router(
    dsss.api.status.router,
    prefix="/status",
    responses={404: {"error": "invalid API route"}},
)

api.include_router(
    dsss.api.admin.router,
    prefix="/admin",
    responses={404: {"error": "invalid API route"}},
)

app.include_router(api, prefix="/api")
