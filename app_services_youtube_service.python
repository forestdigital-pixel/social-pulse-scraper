from datetime import datetime
from typing import List

from googleapiclient.discovery import build

from app.config import settings
from app.cache import get_cache, set_cache
from app.models.post import YouTubeVideo

_youtube = None


def _get_youtube():
    global _youtube
    if _youtube is None:
        _youtube = build("youtube", "v3", developerKey=settings.youtube_api_key)
    return _youtube


def _item_to_video(item: dict) -> YouTubeVideo:
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    vid_id = item.get("id", {})
    if isinstance(vid_id, dict):
        vid_id = vid_id.get("videoId", "")

    return YouTubeVideo(
        video_id=vid_id,
        title=snippet.get("title", ""),
        channel_title=snippet.get("channelTitle", ""),
        description=snippet.get("description", "")[:300],
        published_at=datetime.fromisoformat(
            snippet.get("publishedAt", "2000-01-01T00:00:00Z").replace("Z", "+00:00")
        ),
        view_count=int(stats.get("viewCount", 0)),
        like_count=int(stats.get("likeCount", 0)),
        comment_count=int(stats.get("commentCount", 0)),
        thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
    )


async def fetch_search_videos(query: str, max_results: int, order: str) -> List[YouTubeVideo]:
    params = {"q": query, "max_results": max_results, "order": order}
    cached = get_cache("youtube:search", params)
    if cached:
        return [YouTubeVideo(**v) for v in cached]

    yt = _get_youtube()
    search_resp = (
        yt.search()
        .list(part="snippet", q=query, maxResults=max_results, order=order, type="video")
        .execute()
    )
    video_ids = [i["id"]["videoId"] for i in search_resp.get("items", [])]
    if not video_ids:
        return []

    details_resp = (
        yt.videos().list(part="snippet,statistics", id=",".join(video_ids)).execute()
    )
    videos = [_item_to_video(i) for i in details_resp.get("items", [])]
    set_cache("youtube:search", params, [v.dict() for v in videos])
    return videos


async def fetch_trending_videos(region_code: str, max_results: int) -> List[YouTubeVideo]:
    params = {"region_code": region_code, "max_results": max_results}
    cached = get_cache("youtube:trending", params)
    if cached:
        return [YouTubeVideo(**v) for v in cached]

    yt = _get_youtube()
    resp = (
        yt.videos()
        .list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results,
        )
        .execute()
    )
    videos = [_item_to_video(i) for i in resp.get("items", [])]
    set_cache("youtube:trending", params, [v.dict() for v in videos], ttl_minutes=30)
    return videos


async def fetch_video_details(video_id: str) -> YouTubeVideo:
    params = {"video_id": video_id}
    cached = get_cache("youtube:details", params)
    if cached:
        return YouTubeVideo(**cached)

    yt = _get_youtube()
    resp = yt.videos().list(part="snippet,statistics", id=video_id).execute()
    items = resp.get("items", [])
    if not items:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Video not found")
    video = _item_to_video(items[0])
    set_cache("youtube:details", params, video.dict(), ttl_minutes=60)
    return video