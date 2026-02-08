from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from dsss.engine.engine import Engine


def get_engine(request: Request) -> Engine:
    return request.app.state.engine  # pyright: ignore[reportAny]


def get_sessions(request: Request) -> list[str]:
    return request.app.state.sessions  # pyright: ignore[reportAny]


def make_response(engine: Engine, **kwargs: Any) -> JSONResponse:  # pyright: ignore[reportExplicitAny]
    return JSONResponse(
        {
            "currentRound": engine.current_round,
            "timeToNextRound": engine.get_time_to_next_round(),
            "paused": engine.paused,
            **kwargs,
        }
    )
