from fastapi import APIRouter, Request

from dsss.api.shared import get_engine, make_response

router = APIRouter()


@router.get("/scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "scores": engine.get_scores(),
        },
    )


@router.get("/round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.get_rounds(),
        },
    )


@router.get("/cumulative_round_history")
async def get_cumulative_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.get_rounds_cumulative(),
        },
    )


@router.get("/overview")
async def get_overview(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "overview": engine.get_overview(),
        },
    )
