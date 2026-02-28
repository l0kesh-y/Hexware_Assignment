# Learning Management System (LMS) - Course Enrollment Platform

A scalable backend system built with FastAPI following Clean Architecture principles.

## Features

- Course Management (Create, View, List)
- Student Management (Register, View Profile)
- Enrollment Management (Enroll, View Enrollments)
- Prevents duplicate enrollments
- REST API with automatic Swagger documentation

## Architecture

The project follows Clean Architecture with clear separation of concerns:

```
Controller → Service → Repository → Database
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
cd lms_app
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Interactive API documentation (Swagger UI): http://localhost:8000/docs

## API Endpoints

### Courses
- POST /courses - Create a course
- GET /courses - List all courses
- GET /courses/{course_id} - Get course by ID

### Students
- POST /students - Register a student
- GET /students/{student_id} - Get student by ID

### Enrollments
- POST /enrollments - Enroll student in course
- GET /enrollments - Get all enrollments
- GET /enrollments/students/{student_id}/enrollments - Get student's enrollments

## Example Usage

### Create a Course
```bash
curl -X POST "http://localhost:8000/courses" \
  -H "Content-Type: application/json" \
  -d '{"title": "Python for Beginners", "duration": 40}'
```

### Register a Student
```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{"name": "Anita Sharma", "email": "anita@gmail.com"}'
```

### Enroll Student
```bash
curl -X POST "http://localhost:8000/enrollments" \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1, "course_id": 1}'
```

## Project Structure

```
lms_app/
├── app/
│   ├── main.py                    # Application entry point
│   ├── core/                      # Configuration
│   │   └── db.py                  # Database setup
│   ├── models/                    # Database models
│   │   ├── student_model.py
│   │   ├── course_model.py
│   │   └── enrollment_model.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── student_schema.py
│   │   ├── course_schema.py
│   │   └── enrollment_schema.py
│   ├── repositories/              # Data access layer
│   │   ├── student_repository.py
│   │   ├── course_repository.py
│   │   └── enrollment_repository.py
│   ├── services/                  # Business logic
│   │   ├── student_service.py
│   │   ├── course_service.py
│   │   └── enrollment_service.py
│   ├── controllers/               # API routes
│   │   ├── student_controller.py
│   │   ├── course_controller.py
│   │   └── enrollment_controller.py
│   ├── dependencies/              # Dependency injection
│   │   └── dependencies.py
│   └── middleware/                # Cross-cutting concerns
│       └── cors.py
├── requirements.txt
└── README.md
```

## Business Rules

- A student cannot enroll in the same course twice
- Student email must be unique
- Both student and course must exist before enrollment

## Technology Stack

- FastAPI - Web framework
- SQLAlchemy - ORM
- Pydantic - Data validation
- SQLite - Database
- Uvicorn - ASGI server
