from fastapi import APIRouter, Request

from dsss.api.shared import get_engine, make_response

router = APIRouter()

@router.get("/info")
async def get_info(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "event_name_long": engine.config.event_name_long,
            "event_name_short": engine.config.event_name_short,
            "organization_name_long": engine.config.organization_name_long,
            "organization_name_short": engine.config.organization_name_short,
        },
    )

@router.get("/scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "scores": engine.current_scores,
        },
    )


@router.get("/round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.current_round_history,
        },
    )


@router.get("/cumulative_round_history")
async def get_cumulative_round_history(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "rounds": engine.current_score_history,
        },
    )


@router.get("/overview")
async def get_overview(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        **{
            "overview": engine.current_overview,
        },
    )
