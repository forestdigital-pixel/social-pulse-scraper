from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List

from app.models.post import TrendResult
from app.services.gtrends_service import fetch_interest_over_time, fetch_related

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/interest")
@limiter.limit("10/minute")
async def get_interest(
    request: Request,
    keywords: List[str] = Query(..., description="Up to 5 keywords"),
    timeframe: str = Query("today 3-m", description="e.g. 'today 3-m', 'today 12-m'"),
    geo: str = Query("", description="Country code e.g. US, GB"),
):
    """Get Google Trends interest over time."""
    return await fetch_interest_over_time(keywords[:5], timeframe, geo)


@router.get("/related")
@limiter.limit("10/minute")
async def get_related(
    request: Request,
    keyword: str = Query(...),
    timeframe: str = Query("today 3-m"),
    geo: str = Query(""),
):
    """Get related queries and topics for a keyword."""
    return await fetch_related(keyword, timeframe, geo)