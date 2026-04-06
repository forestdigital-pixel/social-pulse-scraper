from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import List, Optional

from app.models.post import RedditPost
from app.services.reddit_service import (
    fetch_hot_posts,
    fetch_search_posts,
    fetch_subreddit_info,
)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/hot", response_model=List[RedditPost])
@limiter.limit("30/minute")
async def get_hot_posts(
    request: Request,
    subreddit: str = Query("all", description="Subreddit name"),
    limit: int = Query(25, ge=1, le=100),
):
    """Fetch hot posts from a subreddit."""
    return await fetch_hot_posts(subreddit, limit)


@router.get("/search", response_model=List[RedditPost])
@limiter.limit("20/minute")
async def search_posts(
    request: Request,
    q: str = Query(..., description="Search query"),
    subreddit: Optional[str] = Query(None),
    limit: int = Query(25, ge=1, le=100),
    sort: str = Query("relevance", enum=["relevance", "hot", "top", "new"]),
):
    """Search Reddit posts."""
    return await fetch_search_posts(q, subreddit, limit, sort)


@router.get("/subreddit/{name}")
@limiter.limit("20/minute")
async def get_subreddit_info(request: Request, name: str):
    """Get subreddit metadata."""
    return await fetch_subreddit_info(name)