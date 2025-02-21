from fastapi import APIRouter, Response, Query
from app.services.race_analysis_service import generate_gear_shift_plot

router = APIRouter(prefix="/lap-analysis", tags=["Lap Analysis"])

@router.get("/fastest-lap-gear-shifts-plot")
def gear_shift_plot(
    year: int = Query(..., description="Year of the race"),
    round_no: str = Query(..., description="Round number"),
    session_type: str = Query(..., description="Session type (FP1, FP2, FP3, Q, R)")
):
    return generate_gear_shift_plot(year, round_no, session_type)
