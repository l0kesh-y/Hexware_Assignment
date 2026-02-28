# Hiring Microservices - Day 4

A complete microservices architecture for a hiring platform built with FastAPI and Docker.

## Services

### 1. Auth Service (Port 8000)
- User authentication and authorization
- JWT token generation
- Swagger UI: http://localhost:8000/docs

### 2. Job Service (Port 8001)
- Job posting management
- CRUD operations for jobs
- Filter jobs by company
- Swagger UI: http://localhost:8001/docs

### 3. User Service (Port 8002)
- User management
- User registration and login
- Profile management
- Swagger UI: http://localhost:8002/docs

### 4. Company Service (Port 8003)
- Company profile management
- CRUD operations for companies
- Swagger UI: http://localhost:8003/docs

### 5. Application Service (Port 8004)
- Job application management
- Track application status
- Filter by job or candidate
- Swagger UI: http://localhost:8004/docs

## Architecture

Each microservice follows a clean architecture pattern:
- **Models**: Database models (SQLAlchemy)
- **Schemas**: Pydantic models for validation
- **Repositories**: Data access layer
- **Services**: Business logic layer
- **Routers**: API endpoints

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Running All Services

Each service can be started independently:

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

### Building Docker Images

```bash
# Build all images
docker build -t auth-service:latest ./hiring_microservice/auth_service
docker build -t job-service:latest ./hiring_microservice/job_service
docker build -t user-service:latest ./hiring_microservice/user_service
docker build -t company-service:latest ./hiring_microservice/company_service
docker build -t application-service:latest ./hiring_microservice/application_service
```

### Stopping Services

```bash
# Stop specific service
cd hiring_microservice/<service_name>
docker-compose down

# Stop all containers
docker stop $(docker ps -aq)
```

## API Documentation

Each service provides interactive API documentation via Swagger UI:
- Auth Service: http://localhost:8000/docs
- Job Service: http://localhost:8001/docs
- User Service: http://localhost:8002/docs
- Company Service: http://localhost:8003/docs
- Application Service: http://localhost:8004/docs

## Database Ports

- Auth DB: 5432
- Job DB: 5436
- User DB: 5434
- Company DB: 5435
- Application DB: 5437

## Environment Variables

Each service uses environment variables for configuration. Example `.env` file:

```env
DATABASE_URL=postgresql://postgres:root@localhost:5432/dbname
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Note**: `.env` files are excluded from git for security.

## Project Structure

```
hiring_microservice/
├── auth_service/
│   ├── app/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── job_service/
├── user_service/
├── company_service/
└── application_service/
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Environment variables for sensitive data
- `.env` files excluded from version control

## License

MIT
