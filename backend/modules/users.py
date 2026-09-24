"""Port of views/admin_users.py (account creation, role changes) plus the
per-user timezone preference from utils/timezones.py."""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from db import users_col
from schemas import CreateUserRequest, SetTimezoneRequest, UpdateRoleRequest
from security import ROLES, get_current_user, hash_password, require_roles
from serializers import user_out
from utils.timezones import set_user_timezone, timezone_options

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/users")
def list_users(user: dict = Depends(require_roles("admin"))):
    return [user_out(u) for u in users_col().find().sort("created_at", 1)]


@router.get("/users/instructors")
def list_instructors(user: dict = Depends(require_roles("admin"))):
    """For the 'assign to instructor' dropdown when creating/editing a course."""
    return [user_out(u) for u in users_col().find({"role": "instructor"})]


@router.post("/users")
def create_user(body: CreateUserRequest, user: dict = Depends(require_roles("admin"))):
    email = body.email.strip().lower()
    if body.role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role.")
    if users_col().find_one({"email": email}):
        raise HTTPException(status_code=409, detail="A user with this email already exists.")
    doc = {
        "name": body.name.strip(),
        "email": email,
        "password_hash": hash_password(body.password),
        "role": body.role,
        "created_at": datetime.now(timezone.utc),
        "timezone": "Asia/Kolkata",
    }
    result = users_col().insert_one(doc)
    doc["_id"] = result.inserted_id
    return user_out(doc)


@router.patch("/users/{user_id}/role")
def update_role(user_id: str, body: UpdateRoleRequest, user: dict = Depends(require_roles("admin"))):
    if body.role not in ROLES:
        raise HTTPException(status_code=400, detail="Invalid role.")
    if user_id == user["id"] and body.role != "admin":
        raise HTTPException(status_code=400, detail="You can't demote your own account.")
    result = users_col().update_one({"_id": ObjectId(user_id)}, {"$set": {"role": body.role}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"ok": True}


@router.get("/timezones")
def get_timezone_options(user: dict = Depends(get_current_user)):
    return {"options": timezone_options()}


@router.patch("/users/me/timezone")
def update_my_timezone(body: SetTimezoneRequest, user: dict = Depends(get_current_user)):
    set_user_timezone(user["id"], body.timezone)
    return {"ok": True, "timezone": body.timezone}
