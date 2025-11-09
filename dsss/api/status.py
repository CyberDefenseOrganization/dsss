from fastapi import APIRouter, Request

from dsss.api import get_engine

router = APIRouter()


@router.get("/get_scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return {
        "scores": engine.get_scores(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@router.get("/get_round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return {
        "rounds": engine.get_rounds(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@router.get("/get_cumulative_round_history")
async def get_cumulative_round_history(request: Request):
    engine = get_engine(request)

    return {
        "rounds": engine.get_rounds_cumulative(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@router.get("/get_overview")
async def get_overview(request: Request):
    engine = get_engine(request)

    return {
        "overview": engine.get_overview(),
        "currentRound": engine.current_round,
        "timeToNextRound": engine.get_time_to_next_round(),
    }


@router.get("/time_to_next_round")
async def get_time_to_next_round(request: Request):
    return {
        "timeToNextRound": get_engine(request).get_time_to_next_round(),
    }
