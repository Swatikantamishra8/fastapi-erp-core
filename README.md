# fastapi-erp-core

![CI](https://github.com/Swatikantamishra8/fastapi-erp-core/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A production-ready lightweight ERP REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0 async**, **Docker** & **JWT Authentication**.

## Features

- **JWT Authentication** - Secure token-based auth with bcrypt password hashing
- **Employee Management** - Full CRUD with department associations
- **Department Management** - Organizational hierarchy support
- **Attendance Tracking** - Clock-in/out with daily summaries
- **Async Database** - SQLAlchemy 2.0 with asyncpg for high performance
- **Database Migrations** - Alembic for schema versioning
- **Docker Ready** - Single command deployment with docker-compose
- **CI/CD** - GitHub Actions with linting, testing, and Docker build
- **API Docs** - Auto-generated Swagger UI & ReDoc

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI 0.110 |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 (async) |
| Auth | python-jose + passlib[bcrypt] |
| Migrations | Alembic |
| Container | Docker + docker-compose |
| Testing | pytest + pytest-asyncio |
| Linting | ruff |

## Quick Start

### With Docker (Recommended)

```bash
git clone https://github.com/Swatikantamishra8/fastapi-erp-core.git
cd fastapi-erp-core
cp .env.example .env
docker-compose up --build
```

API available at: http://localhost:8000
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

### Local Development

```bash
# Clone repository
git clone https://github.com/Swatikantamishra8/fastapi-erp-core.git
cd fastapi-erp-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/token` | Login & get JWT token |

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/employees` | List all employees |
| POST | `/api/v1/employees` | Create employee |
| GET | `/api/v1/employees/{id}` | Get employee |
| PUT | `/api/v1/employees/{id}` | Update employee |
| DELETE | `/api/v1/employees/{id}` | Delete employee |

### Departments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/departments` | List all departments |
| POST | `/api/v1/departments` | Create department |
| GET | `/api/v1/departments/{id}` | Get department |
| PUT | `/api/v1/departments/{id}` | Update department |
| DELETE | `/api/v1/departments/{id}` | Delete department |

### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/attendance/check-in` | Record check-in |
| POST | `/api/v1/attendance/check-out/{id}` | Record check-out |
| GET | `/api/v1/attendance/employee/{id}` | Get employee records |
| GET | `/api/v1/attendance/summary/{id}` | Daily summary |

## Project Structure

```
fastapi-erp-core/
├── app/
│   ├── main.py           # FastAPI app, CORS, routers
│   ├── database.py       # Async SQLAlchemy engine & session
│   ├── models.py         # SQLAlchemy ORM models
│   ├── schemas.py        # Pydantic v2 request/response schemas
│   ├── auth.py           # JWT token & password utilities
│   └── routers/
│       ├── auth.py       # Auth endpoints
│       ├── employees.py  # Employee CRUD
│       ├── departments.py # Department CRUD
│       └── attendance.py  # Attendance tracking
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Running Tests

```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.
