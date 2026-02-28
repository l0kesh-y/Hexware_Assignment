# Hexware Assignment

This repository contains FastAPI projects built following Clean Architecture principles.

## Projects

### Day 4: Hiring Microservices Platform
A complete microservices architecture for a hiring platform built with FastAPI and Docker.

**Location**: `hiring_microservice/`

**Services**:
1. **Auth Service** (Port 8000) - Authentication & JWT tokens
2. **Job Service** (Port 8001) - Job posting management
3. **User Service** (Port 8002) - User management
4. **Company Service** (Port 8003) - Company profiles
5. **Application Service** (Port 8004) - Job applications

**Technology Stack**:
- FastAPI, PostgreSQL, SQLAlchemy 2.0
- JWT Authentication, bcrypt
- Docker & Docker Compose

[View Day 4 Documentation](#day-4-hiring-microservices)

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

---

## Day 4: Hiring Microservices

### Architecture

Each microservice follows a clean architecture pattern:
- **Models**: Database models (SQLAlchemy)
- **Schemas**: Pydantic models for validation
- **Repositories**: Data access layer
- **Services**: Business logic layer
- **Routers**: API endpoints

### Getting Started

#### Prerequisites
- Docker
- Docker Compose

#### Running All Services

```bash
# Auth Service
cd hiring_microservice/auth_service
docker-compose up -d

# Job Service
cd hiring_microservice/job_service
docker-compose up -d

# User Service
cd hiring_microservice/user_service
docker-compose up -d

# Company Service
cd hiring_microservice/company_service
docker-compose up -d

# Application Service
cd hiring_microservice/application_service
docker-compose up -d
```

#### Building Docker Images

```bash
docker build -t auth-service:latest ./hiring_microservice/auth_service
docker build -t job-service:latest ./hiring_microservice/job_service
docker build -t user-service:latest ./hiring_microservice/user_service
docker build -t company-service:latest ./hiring_microservice/company_service
docker build -t application-service:latest ./hiring_microservice/application_service
```

### API Documentation

Each service provides interactive API documentation via Swagger UI:
- Auth Service: http://localhost:8000/docs
- Job Service: http://localhost:8001/docs
- User Service: http://localhost:8002/docs
- Company Service: http://localhost:8003/docs
- Application Service: http://localhost:8004/docs

### Database Ports

- Auth DB: 5432
- Job DB: 5436
- User DB: 5434
- Company DB: 5435
- Application DB: 5437

---

## Common Architecture

All projects follow Clean Architecture with:
- **Controller Layer**: HTTP endpoints
- **Service Layer**: Business logic
- **Repository Layer**: Data access
- **Schema Layer**: Request/response validation
- **Model Layer**: Database entities

## Technology Stack

- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL / SQLite
- Uvicorn
- Docker

## Author

Lokesh Y
