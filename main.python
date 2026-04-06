import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.database import init_db
from app.routers import reddit, youtube, gtrends


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="SocialPulse API",
    version="1.1.0",
    description="Unified social media data aggregation API",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reddit.router,  prefix="/reddit",  tags=["Reddit"])
app.include_router(youtube.router, prefix="/youtube", tags=["YouTube"])
app.include_router(gtrends.router, prefix="/gtrends", tags=["Google Trends"])

if os.path.isdir("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_frontend():
        return FileResponse("frontend/index.html")


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "version": "1.1.0"}