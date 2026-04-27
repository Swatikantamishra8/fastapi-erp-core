from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Attendance, Employee
from app.schemas import AttendanceCreate, AttendanceUpdate, AttendanceOut
from app.auth import get_current_user
from app.models import User

router = APIRouter()


@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    att_data: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mark attendance for an employee."""
    # Verify employee exists
    emp_result = await db.execute(select(Employee).where(Employee.id == att_data.employee_id))
    if not emp_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Employee not found")
    
    attendance = Attendance(**att_data.model_dump())
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance


@router.get("/", response_model=List[AttendanceOut])
async def list_attendance(
    employee_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List attendance records, optionally filtered by employee."""
    query = select(Attendance)
    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/employee/{employee_id}/today", response_model=List[AttendanceOut])
async def get_today_attendance(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get today's attendance for a specific employee."""
    today = datetime.utcnow().date()
    result = await db.execute(
        select(Attendance)
        .where(Attendance.employee_id == employee_id)
        .where(Attendance.date >= datetime.combine(today, datetime.min.time()))
    )
    return result.scalars().all()


@router.patch("/{attendance_id}", response_model=AttendanceOut)
async def update_attendance(
    attendance_id: int,
    att_data: AttendanceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update attendance record (e.g., add check-out time)."""
    result = await db.execute(select(Attendance).where(Attendance.id == attendance_id))
    attendance = result.scalar_one_or_none()
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    update_data = att_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(attendance, key, value)
    await db.commit()
    await db.refresh(attendance)
    return attendance


@router.get("/report/summary", response_model=List[AttendanceOut])
async def get_attendance_report(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    employee_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 500,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get attendance report with optional date range filter."""
    query = select(Attendance)
    if employee_id:
        query = query.where(Attendance.employee_id == employee_id)
    if start_date:
        query = query.where(Attendance.date >= start_date)
    if end_date:
        query = query.where(Attendance.date <= end_date)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
