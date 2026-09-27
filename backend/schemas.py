"""Pydantic request/response models for every endpoint."""

from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- Auth ---------------------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role: str
    timezone: Optional[str] = None


# --- Users (admin) --------------------------------------------------------

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "student"


class UpdateRoleRequest(BaseModel):
    role: str


class SetTimezoneRequest(BaseModel):
    timezone: str


# --- Admin settings (Digital Samba credentials, session length) -----------

class SettingsOut(BaseModel):
    digitalsamba_developer_key: Optional[str] = None
    digitalsamba_developer_key_set: bool = False
    digitalsamba_developer_key_source: str = "env"
    digitalsamba_team_id: Optional[str] = None
    digitalsamba_team_id_set: bool = False
    digitalsamba_team_id_source: str = "env"
    jwt_expire_minutes: int
    jwt_expire_minutes_source: str = "env"


class SettingsUpdate(BaseModel):
    # Any field left out of the request body is left untouched. Sending an
    # empty string clears that override and falls back to the Render env
    # var again (see runtime_settings.py).
    digitalsamba_developer_key: Optional[str] = None
    digitalsamba_team_id: Optional[str] = None
    jwt_expire_minutes: Optional[int] = Field(default=None, ge=5, le=43200)


# --- Courses --------------------------------------------------------------

class CreateCourseRequest(BaseModel):
    title: str
    category: str = ""
    description: str = ""
    thumbnail_url: str = ""
    is_free: bool = True
    instructor_id: Optional[str] = None


class UpdateCourseRequest(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_free: Optional[bool] = None
    instructor_id: Optional[str] = None


# --- Modules / Lessons -----------------------------------------------------

class CreateModuleRequest(BaseModel):
    title: str


class UpdateModuleRequest(BaseModel):
    title: str


class CreateLessonRequest(BaseModel):
    title: str
    youtube_id: str = ""
    ppt_link: str = ""
    colab_link: str = ""
    dataset_link: str = ""


class UpdateLessonRequest(BaseModel):
    title: Optional[str] = None
    youtube_id: Optional[str] = None
    ppt_link: Optional[str] = None
    colab_link: Optional[str] = None
    dataset_link: Optional[str] = None


# --- Enrollments ------------------------------------------------------------

class CreateEnrollmentRequest(BaseModel):
    user_id: str
    course_id: str


# --- Assignments / Submissions ---------------------------------------------

class CreateAssignmentRequest(BaseModel):
    course_id: str
    title: str
    description: str = ""
    due_date: Optional[str] = None


class UpdateAssignmentRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None


class SubmitAssignmentRequest(BaseModel):
    link_or_text: str


class GradeSubmissionRequest(BaseModel):
    grade: int = Field(ge=0, le=100)
    status: str  # pending | approved | rejected
    feedback: str = ""


# --- Live sessions ----------------------------------------------------------

class CreateLiveSessionRequest(BaseModel):
    course_id: str
    title: str
    description: str = ""
    date: date
    time: time
    timezone: str
    duration_minutes: int = Field(default=60, ge=15, le=300)


class UpdateLiveSessionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    timezone: Optional[str] = None
    duration_minutes: Optional[int] = Field(default=None, ge=15, le=300)
