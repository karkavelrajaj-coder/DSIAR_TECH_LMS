"""MongoDB connection layer — direct port of the Streamlit app's utils/db.py,
minus the st.cache_resource (replaced with a plain module-level singleton,
since FastAPI has no equivalent decorator; the client is created once at
import time and reused for the life of the process, same effect).
"""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError, OperationFailure
from pymongo.server_api import ServerApi

from config import settings

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI, server_api=ServerApi("1"))
    return _client


def get_db() -> Database:
    return get_client()[settings.DB_NAME]


# --- Convenience collection accessors (same names as the Streamlit app) -----

def users_col():
    return get_db()["users"]


def courses_col():
    return get_db()["courses"]


def modules_col():
    return get_db()["modules"]


def lessons_col():
    return get_db()["lessons"]


def assignments_col():
    return get_db()["assignments"]


def submissions_col():
    return get_db()["submissions"]


def progress_col():
    return get_db()["progress"]


def enrollments_col():
    return get_db()["enrollments"]


def certificates_col():
    return get_db()["certificates"]


def live_sessions_col():
    return get_db()["live_sessions"]


def ensure_indexes():
    """Same resilience pattern as the Streamlit app: wrapped in try/except so
    a leftover duplicate can't crash startup."""
    index_specs = [
        (users_col, "email", {"unique": True}),
        (modules_col, "course_id", {}),
        (lessons_col, "module_id", {}),
        (enrollments_col, [("user_id", 1), ("course_id", 1)], {"unique": True}),
        (progress_col, [("user_id", 1), ("lesson_id", 1)], {"unique": True}),
        (submissions_col, [("assignment_id", 1), ("user_id", 1)], {}),
        (certificates_col, [("user_id", 1), ("course_id", 1)], {"unique": True}),
        (certificates_col, "cert_id", {"unique": True}),
        (live_sessions_col, "course_id", {}),
        (live_sessions_col, "room_name", {"unique": True}),
    ]
    for col_fn, keys, kwargs in index_specs:
        try:
            col_fn().create_index(keys, **kwargs)
        except (DuplicateKeyError, OperationFailure):
            pass
