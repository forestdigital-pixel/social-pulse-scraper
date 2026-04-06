from pytrends.request import TrendReq
from typing import List

from app.cache import get_cache, set_cache


def _get_pytrends() -> TrendReq:
    return TrendReq(hl="en-US", tz=360)


async def fetch_interest_over_time(
    keywords: List[str], timeframe: str, geo: str
) -> dict:
    params = {"keywords": keywords, "timeframe": timeframe, "geo": geo}
    cached = get_cache("gtrends:interest", params)
    if cached:
        return cached

    pt = _get_pytrends()
    pt.build_payload(keywords, timeframe=timeframe, geo=geo)
    df = pt.interest_over_time()

    if df.empty:
        data = {"keywords": keywords, "interest_over_time": {}}
    else:
        df = df.drop(columns=["isPartial"], errors="ignore")
        data = {
            "keywords": keywords,
            "interest_over_time": df.to_dict(),
        }

    set_cache("gtrends:interest", params, data, ttl_minutes=60)
    return data


async def fetch_related(keyword: str, timeframe: str, geo: str) -> dict:
    params = {"keyword": keyword, "timeframe": timeframe, "geo": geo}
    cached = get_cache("gtrends:related", params)
    if cached:
        return cached

    pt = _get_pytrends()
    pt.build_payload([keyword], timeframe=timeframe, geo=geo)

    related_queries = pt.related_queries()
    related_topics = pt.related_topics()

    def safe_df(d, key):
        try:
            df = d.get(keyword, {}).get(key)
            return df.to_dict("records") if df is not None else []
        except Exception:
            return []

    data = {
        "keyword": keyword,
        "related_queries": {
            "top": safe_df(related_queries, "top"),
            "rising": safe_df(related_queries, "rising"),
        },
        "related_topics": {
            "top": safe_df(related_topics, "top"),
            "rising": safe_df(related_topics, "rising"),
        },
    }

    set_cache("gtrends:related", params, data, ttl_minutes=60)
    return data