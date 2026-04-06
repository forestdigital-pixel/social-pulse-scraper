import praw
from datetime import datetime
from typing import List, Optional

from app.config import settings
from app.cache import get_cache, set_cache
from app.models.post import RedditPost

_reddit: praw.Reddit | None = None


def _get_reddit() -> praw.Reddit:
    global _reddit
    if _reddit is None:
        _reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )
    return _reddit


def _submission_to_post(sub) -> RedditPost:
    return RedditPost(
        id=sub.id,
        title=sub.title,
        subreddit=str(sub.subreddit),
        author=str(sub.author) if sub.author else "[deleted]",
        score=sub.score,
        num_comments=sub.num_comments,
        url=sub.url,
        selftext=sub.selftext[:500] if sub.selftext else "",
        created_utc=datetime.utcfromtimestamp(sub.created_utc),
        permalink=f"https://reddit.com{sub.permalink}",
    )


async def fetch_hot_posts(subreddit: str, limit: int) -> List[RedditPost]:
    params = {"subreddit": subreddit, "limit": limit}
    cached = get_cache("reddit:hot", params)
    if cached:
        return [RedditPost(**p) for p in cached]

    reddit = _get_reddit()
    posts = [_submission_to_post(s) for s in reddit.subreddit(subreddit).hot(limit=limit)]
    set_cache("reddit:hot", params, [p.dict() for p in posts])
    return posts


async def fetch_search_posts(
    query: str, subreddit: Optional[str], limit: int, sort: str
) -> List[RedditPost]:
    params = {"q": query, "subreddit": subreddit, "limit": limit, "sort": sort}
    cached = get_cache("reddit:search", params)
    if cached:
        return [RedditPost(**p) for p in cached]

    reddit = _get_reddit()
    target = reddit.subreddit(subreddit) if subreddit else reddit.subreddit("all")
    posts = [_submission_to_post(s) for s in target.search(query, sort=sort, limit=limit)]
    set_cache("reddit:search", params, [p.dict() for p in posts])
    return posts


async def fetch_subreddit_info(name: str) -> dict:
    params = {"name": name}
    cached = get_cache("reddit:sub_info", params)
    if cached:
        return cached

    reddit = _get_reddit()
    sub = reddit.subreddit(name)
    data = {
        "name": sub.display_name,
        "title": sub.title,
        "description": sub.public_description,
        "subscribers": sub.subscribers,
        "created_utc": datetime.utcfromtimestamp(sub.created_utc).isoformat(),
        "over18": sub.over18,
        "url": f"https://reddit.com{sub.url}",
    }
    set_cache("reddit:sub_info", params, data, ttl_minutes=60)
    return data