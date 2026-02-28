# Hiring Application Backend

Enterprise-grade FastAPI backend for managing job postings, users, and applications.

## Architecture

- **Controller Layer**: HTTP request handling
- **Service Layer**: Business logic and validation
- **Repository Layer**: Database operations
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic validation schemas

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

3. Initialize Alembic:
```bash
alembic init alembic
```

4. Generate migration:
```bash
alembic revision --autogenerate -m "initial schema"
```

5. Apply migration:
```bash
alembic upgrade head
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Users
- POST /users - Create user
- GET /users/{user_id} - Get user
- GET /users?skip=0&limit=10 - List users (paginated)
- PUT /users/{user_id} - Update user
- DELETE /users/{user_id} - Delete user

### Jobs
- POST /jobs - Create job
- GET /jobs/{job_id} - Get job
- GET /jobs?skip=0&limit=10 - List jobs (paginated)
- PUT /jobs/{job_id} - Update job
- DELETE /jobs/{job_id} - Delete job

### Applications
- POST /applications - Apply for job
- GET /applications/{id} - Get application
- GET /applications/users/{user_id}/applications - Get user applications
- PATCH /applications/{id}/status - Update application status

## Database Schema

### Users
- id, name, email (unique), role, hashed_password

### Jobs
- id, title, description, salary, company_id

### Applications
- id, user_id (FK), job_id (FK), status
