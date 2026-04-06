# ⚡ SocialPulse

> Unified social media data aggregation API — Reddit · YouTube · Google Trends  
> Built with **FastAPI** · Deployed on **Railway** · Powered by **Supabase**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat&logo=railway&logoColor=white)
![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Caching](#-caching)
- [Frontend Dashboard](#-frontend-dashboard)
- [Deploying to Railway](#-deploying-to-railway)
- [Supabase Setup](#-supabase-setup)
- [License](#-license)

---

## 🌐 Overview

SocialPulse is a **REST API** that aggregates real-time data from multiple social media platforms into a single unified interface. It features built-in **response caching** via Supabase, **JWT authentication**, and **rate limiting** out of the box.

---

## ✨ Features

- 🟠 **Reddit** — Fetch hot posts, search posts, subreddit metadata
- 🔴 **YouTube** — Search videos, trending videos, individual video details
- 📈 **Google Trends** — Interest over time, related queries & topics
- 🗄️ **Supabase caching** — All API responses cached with configurable TTL
- 🔐 **JWT Auth** — Secure endpoints with Bearer token authentication
- 🚦 **Rate limiting** — Per-IP rate limits via SlowAPI
- 📊 **Swagger UI** — Auto-generated interactive API docs at `/docs`
- 🌍 **CORS** — Configurable allowed origins
- 🖥️ **Frontend dashboard** — Built-in HTML UI served at `/`

---

## 📁 Project Structure

```
socialpulse/
├── main.py                        # FastAPI app entrypoint
├── requirements.txt               # Python dependencies
├── railway.toml                   # Railway deployment config
├── Procfile                       # Fallback start command
├── .env.example                   # Environment variable template
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── config.py                  # Pydantic settings
│   ├── database.py                # Supabase client
│   ├── auth.py                    # JWT auth helpers
│   ├── cache.py                   # Supabase-backed cache layer
│   ├── models/
│   │   ├── post.py                # RedditPost, YouTubeVideo, TrendResult
│   │   └── user.py                # User, Token models
│   ├── routers/
│   │   ├── reddit.py              # /reddit/* endpoints
│   │   ├── youtube.py             # /youtube/* endpoints
│   │   └── gtrends.py             # /gtrends/* endpoints
│   └── services/
│       ├── reddit_service.py      # PRAW logic
│       ├── youtube_service.py     # YouTube Data API v3 logic
│       └── gtrends_service.py     # Pytrends logic
├── db/
│   └── schema.sql                 # Supabase table definitions
└── frontend/
    └── index.html                 # Built-in dashboard UI
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.11+**
- A [Supabase](https://supabase.com) project
- A [Reddit](https://www.reddit.com/prefs/apps) app (for API credentials)
- A [Google Cloud](https://console.cloud.google.com) project with YouTube Data API v3 enabled

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/socialpulse.git
cd socialpulse
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
# Fill in all values in .env
```

### 5. Set up Supabase tables

Go to your **Supabase project → SQL Editor** and run the contents of `db/schema.sql`.

### 6. Run locally

```bash
uvicorn main:app --reload
```

Visit:
- **Dashboard** → http://localhost:8000
- **Swagger UI** → http://localhost:8000/docs
- **Health check** → http://localhost:8000/health

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description | Required |
|---|---|---|
| `SUPABASE_URL` | Your Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase service role key | ✅ |
| `REDDIT_CLIENT_ID` | Reddit app client ID | ✅ |
| `REDDIT_CLIENT_SECRET` | Reddit app client secret | ✅ |
| `REDDIT_USER_AGENT` | Reddit API user agent string | ✅ |
| `YOUTUBE_API_KEY` | Google Cloud YouTube Data API v3 key | ✅ |
| `SECRET_KEY` | Random secret for JWT signing | ✅ |
| `ALGORITHM` | JWT algorithm (default: `HS256`) | ➖ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiry in minutes (default: `30`) | ➖ |
| `CORS_ORIGINS` | Comma-separated list of allowed origins | ➖ |

---

## 📡 API Reference

### System

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc UI |

### 🟠 Reddit — `/reddit`

| Method | Endpoint | Description | Rate Limit |
|---|---|---|---|
| `GET` | `/reddit/hot` | Hot posts from a subreddit | 30/min |
| `GET` | `/reddit/search` | Search posts | 20/min |
| `GET` | `/reddit/subreddit/{name}` | Subreddit metadata | 20/min |

**Example:**
```
GET /reddit/hot?subreddit=technology&limit=10
GET /reddit/search?q=AI&sort=top&limit=5
GET /reddit/subreddit/programming
```

### 🔴 YouTube — `/youtube`

| Method | Endpoint | Description | Rate Limit |
|---|---|---|---|
| `GET` | `/youtube/search` | Search videos | 20/min |
| `GET` | `/youtube/trending` | Trending videos by region | 10/min |
| `GET` | `/youtube/video/{video_id}` | Single video details | 30/min |

**Example:**
```
GET /youtube/search?q=machine+learning&max_results=10&order=viewCount
GET /youtube/trending?region_code=US&max_results=5
GET /youtube/video/dQw4w9WgXcQ
```

### 📈 Google Trends — `/gtrends`

| Method | Endpoint | Description | Rate Limit |
|---|---|---|---|
| `GET` | `/gtrends/interest` | Interest over time for keywords | 10/min |
| `GET` | `/gtrends/related` | Related queries & topics | 10/min |

**Example:**
```
GET /gtrends/interest?keywords=AI&keywords=ChatGPT&timeframe=today 3-m&geo=US
GET /gtrends/related?keyword=Python&timeframe=today 12-m
```

---

## 🗄️ Caching

All API responses are cached in Supabase's `api_cache` table using an MD5-hashed key derived from the request parameters.

| Source | Default TTL |
|---|---|
| Reddit hot / search | 15 minutes |
| Reddit subreddit info | 60 minutes |
| YouTube search | 15 minutes |
| YouTube trending | 30 minutes |
| YouTube video details | 60 minutes |
| Google Trends | 60 minutes |

Stale entries are automatically deleted on the next cache miss.

---

## 🖥️ Frontend Dashboard

A lightweight built-in dashboard is served at `/` when the `frontend/` directory is present. It lets you interactively query all three data sources directly from the browser — no setup required.

---

## 🚂 Deploying to Railway

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/socialpulse.git
git push -u origin main
```

### 2. Create a Railway project

1. Go to [railway.app](https://railway.app) → **New Project**
2. Select **Deploy from GitHub repo**
3. Choose your `socialpulse` repository

### 3. Add environment variables

In Railway → your service → **Variables**, add all keys from `.env.example`.

### 4. Deploy

Railway auto-detects `railway.toml` and deploys automatically on every push to `main`. ✅

### 5. Verify

```
https://your-app.up.railway.app/health   →  {"status": "ok", "version": "1.1.0"}
https://your-app.up.railway.app/docs     →  Swagger UI
https://your-app.up.railway.app/         →  Frontend Dashboard
```

---

## 🗃️ Supabase Setup

1. Create a free project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run `db/schema.sql`
3. Copy your **Project URL** and **service_role key** from **Settings → API**
4. Paste them into your `.env` (or Railway Variables)

> ⚠️ Use the **service_role** key (not the anon key) so the API can read/write the cache table without RLS restrictions, or configure RLS policies accordingly.

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute it freely.

---

<p align="center">
  Built with ❤️ using FastAPI · Supabase · Railway
</p>