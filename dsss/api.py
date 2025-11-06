import asyncio
from asyncio import Task
from typing import Any

from contextlib import asynccontextmanager
from dataclasses import dataclass
from fastapi import FastAPI
from fastapi.requests import Request
from starlette.datastructures import State

from dsss.engine.engine import Engine
from dsss.main import get_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = get_config()
    app.state.engine = Engine(config)
    app.state.engine_task = asyncio.create_task(app.state.engine.start())
    yield


app = FastAPI(lifespan=lifespan)


def get_engine(request: Request) -> Engine:
    return request.app.state.engine  # pyright: ignore[reportAny]


@app.get("/api/get_scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return {
        "scores": engine.get_scores(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@app.get("/api/get_round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return {
        "rounds": engine.get_rounds(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@app.get("/api/time_to_next_round")
async def get_time_to_next_round(request: Request):
    return {
        "timeToNextRound": get_engine(request).get_time_to_next_round(),
    }
