from typing import Any
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from dsss.api import get_engine
from dsss.engine.engine import Engine

router = APIRouter()


def make_response(engine: Engine, **kwargs: dict[str, Any]) -> JSONResponse:  # pyright: ignore[reportExplicitAny]
    return JSONResponse(
        {
            "currentRound": engine.current_round,
            "timeToNextRound": engine.get_time_to_next_round(),
            "paused": engine.paused,
            **kwargs,
        }
    )


@router.get("/get_scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "scores": engine.get_scores(),
        },
    )


@router.get("/get_round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.get_rounds(),
        },
    )


@router.get("/get_cumulative_round_history")
async def get_cumulative_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.get_rounds_cumulative(),
        },
    )


@router.get("/get_overview")
async def get_overview(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "overview": engine.get_overview(),
        },
    )
