import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional

from app.database import get_client


CACHE_TABLE = "api_cache"
DEFAULT_TTL_MINUTES = 15


def _make_key(prefix: str, params: dict) -> str:
    raw = json.dumps(params, sort_keys=True)
    digest = hashlib.md5(raw.encode()).hexdigest()
    return f"{prefix}:{digest}"


def get_cache(prefix: str, params: dict) -> Optional[Any]:
    client = get_client()
    key = _make_key(prefix, params)
    result = (
        client.table(CACHE_TABLE)
        .select("data, expires_at")
        .eq("cache_key", key)
        .single()
        .execute()
    )
    if not result.data:
        return None
    expires_at = datetime.fromisoformat(result.data["expires_at"])
    if datetime.utcnow() > expires_at:
        client.table(CACHE_TABLE).delete().eq("cache_key", key).execute()
        return None
    return result.data["data"]


def set_cache(prefix: str, params: dict, data: Any, ttl_minutes: int = DEFAULT_TTL_MINUTES):
    client = get_client()
    key = _make_key(prefix, params)
    expires_at = (datetime.utcnow() + timedelta(minutes=ttl_minutes)).isoformat()
    client.table(CACHE_TABLE).upsert(
        {"cache_key": key, "data": data, "expires_at": expires_at}
    ).execute()