import uuid
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dsss.api.shared import get_engine, get_sessions, make_response

router = APIRouter()


async def authentication(request: Request) -> str:
    sessions = get_sessions(request)
    session = request.cookies.get("session_token")

    if session is None:
        raise HTTPException(
            401, {"success": False, "message": "authentication is required"}
        )

    if session not in sessions:
        raise HTTPException(
            401,
            {"success": False, "message": "invalid authentication token"},
        )

    return session


class Login(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(request: Request, response: Response, login: Login):
    engine = get_engine(request)
    sessions = get_sessions(request)

    if (
        engine.config.admin_username == login.username
        and engine.config.admin_password == login.password
    ):
        session = str(uuid.uuid4())
        sessions.append(session)

        response.set_cookie(
            "session_token",
            value=session,
            httponly=True,
            samesite="strict",
            max_age=3600,
        )

        response.set_cookie(
            "session_token_timestamp",
            value=str(time.time()),
            samesite="strict",
            max_age=3600,
        )

        return {
            "success": True,
        }

    return JSONResponse(
        {
            "success": False,
            "message": "invalid credentials",
        },
        status_code=401,
    )


@router.get("/get_status")
async def get_status(request: Request, session: str = Depends(authentication)):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "success": True,
        },
    )


@router.post("/logout")
async def logout(request: Request, response: Response):
    sessions = get_sessions(request)
    session_token = request.cookies.get("session_token")

    if session_token is not None:
        sessions.remove(session_token)

    response.delete_cookie("session_token")
    response.delete_cookie("session_token_timestamp")

    return {
        "success": True,
        "message": "session not found" if session_token is not None else None,
    }


@router.post("/pause")
async def pause(request: Request, _: str = Depends(authentication)):
    engine = get_engine(request)

    if engine.paused:
        return {"success": False, "message": "engine already paused"}

    engine.paused = True
    return {
        "success": True,
    }


@router.post("/resume")
async def resume(request: Request, _: str = Depends(authentication)):
    engine = get_engine(request)

    if not engine.paused:
        return {"success": False, "message": "engine already running"}

    engine.paused = False
    return {
        "success": True,
    }
