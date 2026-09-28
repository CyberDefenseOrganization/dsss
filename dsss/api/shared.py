from typing import cast

from fastapi import Request
from fastapi.responses import JSONResponse

from dsss.engine.engine import Engine


def get_engine(request: Request) -> Engine:
    return cast(Engine, request.app.state.engine)


def get_sessions(request: Request) -> list[str]:
    return cast(list[str], request.app.state.sessions)


def make_response(engine: Engine, **kwargs: object) -> JSONResponse:
    return JSONResponse(
        {
            "currentRound": engine.current_round,
            "timeToNextRound": engine.get_time_to_next_round(),
            "paused": engine.paused,
            **kwargs,
        }
    )
