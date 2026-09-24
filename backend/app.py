"""D'siar Tech LMS — FastAPI backend entry point.

Mirrors app.py's startup (init_session -> now JWT/seed-admin, ensure_indexes)
and exposes the same feature set as the Streamlit views, as a REST API
consumed by the React frontend.

Runs against a NEW MongoDB database (config.DB_NAME, default
"dsiar_lms_v2") in the SAME free Atlas cluster the Streamlit app uses — the
Streamlit app's own "dsiar_lms" database is never opened by this process.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from db import ensure_indexes
from security import seed_first_admin

from modules import assignments, auth, certificates, courses, enrollments, live_sessions, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_indexes()
    seed_first_admin()
    yield


app = FastAPI(title="D'siar Tech LMS API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,  # required so the httpOnly auth cookie is sent/received
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(assignments.router)
app.include_router(certificates.router)
app.include_router(live_sessions.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Serves course thumbnails, the logo, and certificate fonts straight off
# this backend's own filesystem (same "read from disk, not an external
# URL" pattern the Streamlit app switched to after its GitHub repo went
# private) — reachable at /api/static/<filename>, e.g.
# /api/static/AI Thumbnail.png
import os  # noqa: E402

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
app.mount("/api/static", StaticFiles(directory=_ASSETS_DIR), name="static")
