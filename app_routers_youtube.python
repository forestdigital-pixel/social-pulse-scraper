from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List

from app.models.post import YouTubeVideo
from app.services.youtube_service import (
    fetch_search_videos,
    fetch_video_details,
    fetch_trending_videos,
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/search", response_model=List[YouTubeVideo])
@limiter.limit("20/minute")
async def search_videos(
    request: Request,
    q: str = Query(..., description="Search query"),
    max_results: int = Query(10, ge=1, le=50),
    order: str = Query("relevance", enum=["relevance", "date", "viewCount", "rating"]),
):
    """Search YouTube videos."""
    return await fetch_search_videos(q, max_results, order)


@router.get("/trending", response_model=List[YouTubeVideo])
@limiter.limit("10/minute")
async def get_trending(
    request: Request,
    region_code: str = Query("US"),
    max_results: int = Query(10, ge=1, le=50),
):
    """Fetch trending YouTube videos."""
    return await fetch_trending_videos(region_code, max_results)


@router.get("/video/{video_id}", response_model=YouTubeVideo)
@limiter.limit("30/minute")
async def get_video_details(request: Request, video_id: str):
    """Get details for a specific video."""
    return await fetch_video_details(video_id)