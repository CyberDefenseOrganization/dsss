from fastapi import Request
from dsss.engine.engine import Engine


def get_engine(request: Request) -> Engine:
    return request.app.state.engine  # pyright: ignore[reportAny]
