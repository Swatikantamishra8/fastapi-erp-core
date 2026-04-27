from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, employees, departments, attendance
from app.database import init_db

app = FastAPI(
    title="FastAPI ERP Core",
    description="Production-ready ERP REST API with JWT auth, Employee, Department & Attendance management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(departments.router, prefix="/departments", tags=["Departments"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])

@app.get("/", tags=["Health"])
async def root():
    return {"message": "FastAPI ERP Core is running", "docs": "/docs", "version": "1.0.0"}
