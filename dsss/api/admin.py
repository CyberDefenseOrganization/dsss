import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dsss.api import get_engine, get_sessions

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


@router.post("/logout")
async def logout(
    request: Request, response: Response, session_token: str = Depends(authentication)
):
    sessions = get_sessions(request)
    sessions.remove(session_token)

    response.delete_cookie("session_token")

    return {
        "success": True,
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
