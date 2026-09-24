"""Authentication + Role-Based Access Control (RBAC) — FastAPI port of the
Streamlit app's utils/auth.py.

Same three roles, same rules:
- "admin"      : full control.
- "instructor" : scoped to courses where instructor_id == their own id.
- "student"    : enrollment-gated learner.

Session is now a JWT in an httpOnly cookie instead of st.session_state.
There is still no public sign-up endpoint — only an admin (or the seed
admin created on first boot) can create accounts, matching the paid-
enrollment business model.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Cookie, Depends, Header, HTTPException, Response, status

from config import settings
from db import users_col

ROLES = ["admin", "instructor", "student"]


# --- Password helpers (identical to the Streamlit app) -----------------------

def hash_password(raw_password: str) -> bytes:
    return bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())


def verify_password(raw_password: str, hashed) -> bool:
    try:
        if isinstance(hashed, str):
            hashed = hashed.encode("utf-8")
        return bcrypt.checkpw(raw_password.encode("utf-8"), hashed)
    except (ValueError, TypeError):
        return False


# --- Seed admin on first boot (same logic as _seed_first_admin) -------------

def seed_first_admin():
    col = users_col()
    if col.find_one({"role": "admin"}):
        return
    email = settings.SEED_ADMIN_EMAIL
    password = settings.SEED_ADMIN_PASSWORD
    name = settings.SEED_ADMIN_NAME
    if not email or not password:
        return
    if col.find_one({"email": email}):
        col.update_one({"email": email}, {"$set": {"role": "admin"}})
        return
    col.insert_one(
        {
            "name": name,
            "email": email,
            "password_hash": hash_password(password),
            "role": "admin",
            "created_at": datetime.now(timezone.utc),
            "timezone": "Asia/Kolkata",
        }
    )


# --- JWT ----------------------------------------------------------------

def create_access_token(user: dict) -> str:
    payload = {
        "sub": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
        path="/",
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.COOKIE_NAME, path="/")


# --- Login / lookup -----------------------------------------------------

def authenticate(email: str, password: str) -> dict:
    email = email.strip().lower()
    user = users_col().find_one({"email": email})
    if not user or not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password.")
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }


# --- FastAPI dependencies (replace require_login / require_role) -----------

def get_current_user(
    dsiar_session: str | None = Cookie(default=None),
    authorization: str | None = Header(default=None),
) -> dict:
    # Prefer the Authorization header (what the deployed frontend sends —
    # works across different onrender.com subdomains where third-party
    # cookies get blocked). Fall back to the cookie for local dev, where
    # the Vite proxy makes frontend and backend same-origin.
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif dsiar_session:
        token = dsiar_session

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid.")

    # Re-check the user still exists / role hasn't changed since token issue.
    try:
        user = users_col().find_one({"_id": ObjectId(payload["sub"])})
    except InvalidId:
        user = None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account no longer exists.")

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
    }


def require_roles(*allowed_roles: str):
    """Usage: Depends(require_roles("admin", "instructor"))"""

    def _dependency(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to do that.",
            )
        return user

    return _dependency
