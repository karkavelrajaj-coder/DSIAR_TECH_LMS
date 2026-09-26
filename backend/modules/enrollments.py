"""Port of the enrollment half of views/admin_users.py + the
admin/instructor self-enroll-preview button in views/catalog.py.

No public sign-up, no self-enroll for students — matches the paid-
enrollment business model: only an admin enrolls a student in a course.
"""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from db import courses_col, enrollments_col, users_col
from schemas import CreateEnrollmentRequest
from security import get_current_user, require_roles
from serializers import enrollment_out

router = APIRouter(prefix="/api/enrollments", tags=["enrollments"])


@router.get("")
def list_enrollments(user: dict = Depends(get_current_user)):
    if user["role"] == "admin":
        docs = list(enrollments_col().find())
    else:
        docs = list(enrollments_col().find({"user_id": user["id"]}))
    out = []
    for e in docs:
        item = enrollment_out(e)
        student = users_col().find_one({"_id": ObjectId(e["user_id"])})
        course = courses_col().find_one({"_id": ObjectId(e["course_id"])})
        item["student_name"] = student["name"] if student else "Unknown"
        item["student_email"] = student["email"] if student else "—"
        item["course_title"] = course["title"] if course else "Unknown"
        out.append(item)
    return out


@router.post("")
def create_enrollment(body: CreateEnrollmentRequest, user: dict = Depends(require_roles("admin"))):
    existing = enrollments_col().find_one({"user_id": body.user_id, "course_id": body.course_id})
    if existing:
        raise HTTPException(status_code=409, detail="This student is already enrolled in that course.")
    doc = {
        "user_id": body.user_id,
        "course_id": body.course_id,
        "enrolled_at": datetime.now(timezone.utc),
    }
    result = enrollments_col().insert_one(doc)
    doc["_id"] = result.inserted_id
    return enrollment_out(doc)


@router.post("/preview/{course_id}")
def self_enroll_preview(course_id: str, user: dict = Depends(require_roles("admin", "instructor"))):
    """Admins can self-enroll to preview ANY course's content, same as the
    'Enroll (preview)' button in the old catalog.py. Instructors are NOT
    admins, though: they may only preview courses assigned to them (which
    they already have automatic access to via course_detail's
    _has_course_access — this endpoint mainly exists for admin's benefit
    now, but stays open to instructors for their own courses too)."""
    if user["role"] == "instructor":
        course = courses_col().find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found.")
        if course.get("instructor_id") != user["id"]:
            raise HTTPException(status_code=403, detail="You can only access courses assigned to you.")

    existing = enrollments_col().find_one({"user_id": user["id"], "course_id": course_id})
    if existing:
        return enrollment_out(existing)
    doc = {
        "user_id": user["id"],
        "course_id": course_id,
        "enrolled_at": datetime.now(timezone.utc),
    }
    result = enrollments_col().insert_one(doc)
    doc["_id"] = result.inserted_id
    return enrollment_out(doc)


@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: str, user: dict = Depends(require_roles("admin"))):
    result = enrollments_col().delete_one({"_id": ObjectId(enrollment_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found.")
    return {"ok": True}
