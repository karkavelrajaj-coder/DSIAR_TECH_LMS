"""Certificate eligibility + issuance — direct port of utils/certificates.py.
Logic is 100% unchanged from the Streamlit app (it never touched Streamlit
APIs to begin with).
"""

import uuid
from datetime import datetime, timezone

from pymongo.errors import DuplicateKeyError

from db import (
    assignments_col,
    certificates_col,
    lessons_col,
    modules_col,
    progress_col,
    submissions_col,
)


def course_lessons_complete(user_id: str, course_id: str) -> bool:
    module_ids = [str(m["_id"]) for m in modules_col().find({"course_id": course_id})]
    if not module_ids:
        return False
    lesson_ids = [str(l["_id"]) for l in lessons_col().find({"module_id": {"$in": module_ids}})]
    if not lesson_ids:
        return False
    completed_count = progress_col().count_documents(
        {"user_id": user_id, "lesson_id": {"$in": lesson_ids}, "completed": True}
    )
    return completed_count >= len(lesson_ids)


def _all_assignments_approved(user_id: str, course_id: str) -> bool:
    assignment_ids = [str(a["_id"]) for a in assignments_col().find({"course_id": course_id})]
    if not assignment_ids:
        return True
    approved_count = submissions_col().count_documents(
        {"user_id": user_id, "assignment_id": {"$in": assignment_ids}, "status": "approved"}
    )
    return approved_count >= len(assignment_ids)


def is_eligible(user_id: str, course_id: str) -> bool:
    return course_lessons_complete(user_id, course_id) and _all_assignments_approved(user_id, course_id)


def ensure_certificate(user_id: str, course_id: str):
    existing = certificates_col().find_one({"user_id": user_id, "course_id": course_id})
    if existing:
        return existing

    if not is_eligible(user_id, course_id):
        return None

    for _attempt in range(5):
        cert = {
            "user_id": user_id,
            "course_id": course_id,
            "cert_id": uuid.uuid4().hex[:12].upper(),
            "issued_at": datetime.now(timezone.utc),
        }
        try:
            certificates_col().insert_one(cert)
            return cert
        except DuplicateKeyError:
            existing = certificates_col().find_one({"user_id": user_id, "course_id": course_id})
            if existing:
                return existing
            continue

    raise RuntimeError("Could not generate a unique certificate ID after 5 attempts.")
