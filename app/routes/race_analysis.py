from fastapi import APIRouter, Response, Query
from app.services.gear_shift_analysis_service import generate_gear_shift_plot
from app.services.team_pace_comparison_service import generate_team_pace_comparison_plot
from app.services.tyre_strategy_comparison_service import generate_tyre_strategy_plot
from app.services.laptime_tyrecompound_distribution_service import generate_laptime_distribution_plot
from app.services.position_changes_comparison_service import generate_position_changes_plot

router = APIRouter(prefix="/race-analysis", tags=["Race Analysis"])

@router.get("/fastest-lap-gear-shifts-plot")
def gear_shift_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_gear_shift_plot(year, round_no, session_type)


@router.get("/team-pace-comparison")
def team_pace_comparison_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_team_pace_comparison_plot(year, round_no, session_type)

@router.get("/tyre-strategies")
def tyre_strategy_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_tyre_strategy_plot(year, round_no, session_type)

@router.get("/driver-laptimes-distribution--tyrecompound")
def laptime_distribution_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_laptime_distribution_plot(year, round_no, session_type)

@router.get("/position-changes-during-race")
def position_changes_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_position_changes_plot(year, round_no, session_type)