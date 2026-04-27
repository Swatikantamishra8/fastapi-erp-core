from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from app.auth import get_current_user
from app.models import User

router = APIRouter()


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
async def create_employee(
    emp_data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new employee."""
    result = await db.execute(select(Employee).where(Employee.email == emp_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Employee with this email already exists")
    employee = Employee(**emp_data.model_dump())
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    return employee


@router.get("/", response_model=List[EmployeeOut])
async def list_employees(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all employees with pagination."""
    result = await db.execute(select(Employee).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{employee_id}", response_model=EmployeeOut)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single employee by ID."""
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeOut)
async def update_employee(
    employee_id: int,
    emp_data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an employee's details."""
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    update_data = emp_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(employee, key, value)
    await db.commit()
    await db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete (deactivate) an employee."""
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.is_active = False
    await db.commit()
