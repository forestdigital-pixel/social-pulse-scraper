from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RedditPost(BaseModel):
    id: str
    title: str
    subreddit: str
    author: str
    score: int
    num_comments: int
    url: str
    selftext: Optional[str] = ""
    created_utc: datetime
    permalink: str


class YouTubeVideo(BaseModel):
    video_id: str
    title: str
    channel_title: str
    description: Optional[str] = ""
    published_at: datetime
    view_count: Optional[int] = 0
    like_count: Optional[int] = 0
    comment_count: Optional[int] = 0
    thumbnail_url: Optional[str] = ""


class TrendResult(BaseModel):
    keyword: str
    interest_over_time: dict
    related_queries: Optional[dict] = {}
    related_topics: Optional[dict] = {}