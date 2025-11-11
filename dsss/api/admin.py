from collections.abc import Awaitable
import uuid

from fastapi import APIRouter, Request, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dsss.api import get_engine, get_sessions

router = APIRouter()


class Login(BaseModel):
    username: str
    password: str


@FastAPI().middleware("")
async def authentication(
    request: Request, call_next: Awaitable[JSONResponse]
) -> JSONResponse:
    sessions = get_sessions(request)
    session = request.headers.get("session")

    if session is None:
        return JSONResponse(
            {"success": False, "message": "authentication is required"},
            status_code=401,
        )

    if session not in sessions:
        return JSONResponse(
            {"success": False, "message": "invalid authentication token"},
            status_code=401,
        )

    return await call_next


@router.post("/login")
async def login(request: Request, login: Login):
    engine = get_engine(request)
    sessions = get_sessions(request)

    if (
        engine.config.admin_username == login.username
        and engine.config.admin_password == login.password
    ):
        session = str(uuid.uuid4())
        sessions.append(session)

        return {
            "success": True,
            "session": session,
        }

    return JSONResponse(
        {
            "success": False,
            "message": "invalid credentials",
            "status_code": 401,
        }
    )
