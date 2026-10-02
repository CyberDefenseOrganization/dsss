from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse

from dsss.api.shared import get_engine, make_response

router = APIRouter()


@router.get("/info")
async def get_info(request: Request):
    engine = get_engine(request)

    return make_response(
        engine,
        event_name_long=engine.config.event_name_long,
        event_name_short=engine.config.event_name_short,
        organization_name_long=engine.config.organization_name_long,
        organization_name_short=engine.config.organization_name_short,
        logo_url="/api/status/logo" if engine.config.logo_path else None,
    )


@router.get("/logo")
async def get_logo(request: Request):
    logo_path = get_engine(request).config.logo_path

    if not logo_path or not Path(logo_path).is_file():
        raise HTTPException(status_code=404, detail="No logo image configured")

    return FileResponse(logo_path)


@router.get("/scores")
async def get_scores(request: Request):
    engine = get_engine(request)

    return make_response(engine, scores=engine.current_scores)


@router.get("/round_history")
async def get_round_history(request: Request):
    engine = get_engine(request)

    return make_response(engine, rounds=engine.current_round_history)


@router.get("/cumulative_round_history")
async def get_cumulative_round_history(request: Request):
    """
    Return scores at various rounds in history.

    This endpoint handles sub-samples history automatically to prevent very large JSON 
    blobs being sent over the network.
    """
    engine = get_engine(request)

    history = engine.current_score_history
    num_rounds = max((len(scores) for scores in history.values()), default=0)
    
    # fuckass formula
    interval = 1 if num_rounds <= 1000 else ((num_rounds + 9999) // 10000) * 10
    round_numbers = list(range(interval, num_rounds + 1, interval))
    
    # always include last round
    if num_rounds and (not round_numbers or round_numbers[-1] != num_rounds):
        round_numbers.append(num_rounds)

    return make_response(
        engine,
        roundNumbers=round_numbers,
        rounds={
            team: [
                scores[round_id - 1] if round_id <= len(scores) else None
                for round_id in round_numbers
            ]
            for team, scores in history.items()
        },
    )


@router.get("/overview")
async def get_overview(request: Request):
    engine = get_engine(request)

    return make_response(engine, overview=engine.current_overview)
