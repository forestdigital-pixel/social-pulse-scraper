from supabase import create_client, Client
from app.config import settings

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client


def init_db():
    """Verify Supabase connection on startup."""
    client = get_client()
    # Simple ping — will raise if credentials are wrong
    client.table("reddit_posts").select("id").limit(1).execute()
    print("✅ Supabase connection verified.")