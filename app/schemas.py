from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


# ── Auth Schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# ── Department Schemas ────────────────────────────────────────
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None


class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Employee Schemas ──────────────────────────────────────────
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    designation: Optional[str] = Field(None, max_length=100)
    department_id: Optional[int] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    designation: Optional[str] = None
    department_id: Optional[int] = None
    is_active: Optional[bool] = None


class EmployeeOut(EmployeeBase):
    id: int
    is_active: bool
    joined_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Attendance Schemas ────────────────────────────────────────
class AttendanceBase(BaseModel):
    employee_id: int
    status: str = Field(default="present", pattern="^(present|absent|half_day|leave)$")
    notes: Optional[str] = Field(None, max_length=255)


class AttendanceCreate(AttendanceBase):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None


class AttendanceUpdate(BaseModel):
    check_out: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AttendanceOut(AttendanceBase):
    id: int
    date: datetime
    check_in: Optional[datetime]
    check_out: Optional[datetime]

    model_config = {"from_attributes": True}
