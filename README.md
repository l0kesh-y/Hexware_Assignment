# Hexware Assignment - FastAPI Clean Architecture Projects

This repository contains two FastAPI projects built following Clean Architecture principles.

## Projects

### 1. Learning Management System (LMS)
A course enrollment platform for managing students, courses, and enrollments.

**Location**: `lms_app/`

**Features**:
- Course management
- Student registration
- Course enrollment with duplicate prevention
- REST APIs with Swagger documentation

[View LMS Documentation](./lms_app/README.md)

### 2. Loan Application & Approval Management System
A fintech loan processing system with automated eligibility validation.

**Location**: `loan_app/`

**Features**:
- Loan application submission
- Automatic eligibility validation
- Approve/Reject workflow
- Business rule enforcement

[View Loan System Documentation](./loan_app/README.md)

## Architecture

Both projects follow Clean Architecture with:
- **Controller Layer**: HTTP endpoints
- **Service Layer**: Business logic
- **Repository Layer**: Data access
- **Schema Layer**: Request/response validation
- **Model Layer**: Database entities

## Technology Stack

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## Quick Start

### LMS Application
```bash
cd lms_app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

### Loan Application
```bash
cd loan_app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

## Author

Lokesh Y
