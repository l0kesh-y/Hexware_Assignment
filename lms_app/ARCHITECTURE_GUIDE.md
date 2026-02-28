# LMS Architecture Visual Guide

## 🎯 The Big Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER / CLIENT                            │
│                    (Web Browser / Mobile App)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Request
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FASTAPI APP                              │
│                        (main.py)                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    MIDDLEWARE                               │ │
│  │              (CORS, Authentication, etc.)                   │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONTROLLER LAYER                              │
│                   (student_controller.py)                        │
│                                                                  │
│  • Receives HTTP requests                                       │
│  • Validates request format                                     │
│  • Calls service layer                                          │
│  • Returns HTTP responses                                       │
│                                                                  │
│  Example: POST /students                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│                   (student_service.py)                           │
│                                                                  │
│  • Implements business rules                                    │
│  • Validates business logic                                     │
│  • Orchestrates multiple operations                             │
│  • Handles errors                                               │
│                                                                  │
│  Example: Check if email already exists                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   REPOSITORY LAYER                               │
│                 (student_repository.py)                          │
│                                                                  │
│  • Performs database operations                                 │
│  • CRUD operations (Create, Read, Update, Delete)               │
│  • Database queries                                             │
│  • No business logic                                            │
│                                                                  │
│  Example: INSERT INTO students...                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATABASE                                  │
│                      (SQLite - lms.db)                           │
│                                                                  │
│  Tables: students, courses, enrollments                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Complete Request Flow: Creating a Student

```
┌──────────────────────────────────────────────────────────────────┐
│ STEP 1: User Sends Request                                       │
└──────────────────────────────────────────────────────────────────┘

POST http://localhost:8000/students
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 2: FastAPI Receives & Validates                             │
│ File: app/schemas/student_schema.py                              │
└──────────────────────────────────────────────────────────────────┘

class StudentCreate(BaseModel):
    name: str              ✓ Check: Is it a string?
    email: EmailStr        ✓ Check: Is it valid email format?

If validation fails → Return 422 Unprocessable Entity
If validation passes → Continue

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 3: Controller Receives Request                              │
│ File: app/controllers/student_controller.py                      │
└──────────────────────────────────────────────────────────────────┘

@router.post("", response_model=StudentResponse, status_code=201)
def register_student(
    student: StudentCreate,                    ← Validated data
    service: StudentService = Depends(...)     ← Injected service
):
    return service.create_student(student)     ← Call service

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 4: Dependency Injection                                     │
│ File: app/dependencies/dependencies.py                           │
└──────────────────────────────────────────────────────────────────┘

def get_student_service(db: Session = Depends(get_db)):
    1. Get database session
    2. Create repository with session
    3. Create service with repository
    4. Return service

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 5: Service Layer - Business Logic                           │
│ File: app/services/student_service.py                            │
└──────────────────────────────────────────────────────────────────┘

def create_student(self, student: StudentCreate):
    
    # Business Rule: Check duplicate email
    existing = self.repository.get_by_email(student.email)
    
    if existing:
        ❌ raise HTTPException(400, "Email already registered")
    
    # Create student
    db_student = self.repository.create(student)
    
    # Convert to response format
    return StudentResponse.model_validate(db_student)

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 6: Repository Layer - Database Operation                    │
│ File: app/repositories/student_repository.py                     │
└──────────────────────────────────────────────────────────────────┘

def create(self, student: StudentCreate):
    # Create database model
    db_student = Student(
        name=student.name,
        email=student.email
    )
    
    # Add to session
    self.db.add(db_student)
    
    # Save to database
    self.db.commit()
    
    # Refresh to get ID
    self.db.refresh(db_student)
    
    return db_student

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 7: Database Executes SQL                                    │
│ Database: lms.db                                                 │
└──────────────────────────────────────────────────────────────────┘

INSERT INTO students (name, email) 
VALUES ('John Doe', 'john@example.com');

-- Database generates ID = 1
-- Returns: {id: 1, name: 'John Doe', email: 'john@example.com'}

                    ↓

┌──────────────────────────────────────────────────────────────────┐
│ STEP 8: Response Flows Back                                      │
└──────────────────────────────────────────────────────────────────┘

Repository → Service → Controller → FastAPI → User

HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

## 🎭 Understanding Each Layer with Real Examples

### Layer 1: Models (Database Structure)

```python
# app/models/student_model.py

from sqlalchemy import Column, Integer, String
from app.core.db import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
```

**What it does:**
```
Creates this table in database:

┌────┬─────────────┬──────────────────────┐
│ id │    name     │        email         │
├────┼─────────────┼──────────────────────┤
│ 1  │ John Doe    │ john@example.com     │
│ 2  │ Jane Smith  │ jane@example.com     │
│ 3  │ Bob Wilson  │ bob@example.com      │
└────┴─────────────┴──────────────────────┘
```

**Key Points:**
- `primary_key=True` → Unique identifier
- `unique=True` → No duplicate emails
- `nullable=False` → Field is required
- `index=True` → Fast searching

---

### Layer 2: Schemas (Validation)

```python
# app/schemas/student_schema.py

from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True
```

**What it does:**

```
INPUT VALIDATION:

✅ Valid Request:
{
  "name": "John Doe",
  "email": "john@example.com"
}

❌ Invalid Request:
{
  "name": "",              ← Empty string
  "email": "not-an-email"  ← Invalid format
}

Response: 422 Unprocessable Entity
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**Two Different Schemas:**

```
StudentCreate (Input)          StudentResponse (Output)
├── name                       ├── id (added by database)
└── email                      ├── name
                               └── email
```

---

### Layer 3: Repository (Database Operations)

```python
# app/repositories/student_repository.py

class StudentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, student: StudentCreate) -> Student:
        db_student = Student(name=student.name, email=student.email)
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    def get_by_id(self, student_id: int) -> Student:
        return self.db.query(Student).filter(Student.id == student_id).first()
    
    def get_by_email(self, email: str) -> Student:
        return self.db.query(Student).filter(Student.email == email).first()
```

**What it does:**

```
CRUD Operations:

┌─────────────────────────────────────────────────────────────┐
│ CREATE                                                      │
├─────────────────────────────────────────────────────────────┤
│ repository.create(student)                                  │
│ → INSERT INTO students (name, email) VALUES (?, ?)         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ READ                                                        │
├─────────────────────────────────────────────────────────────┤
│ repository.get_by_id(1)                                     │
│ → SELECT * FROM students WHERE id = 1                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ READ BY EMAIL                                               │
├─────────────────────────────────────────────────────────────┤
│ repository.get_by_email("john@example.com")                 │
│ → SELECT * FROM students WHERE email = 'john@example.com'  │
└─────────────────────────────────────────────────────────────┘
```

**Repository Pattern Benefits:**

```
❌ Without Repository (Bad):

def create_student(student):
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    # Database logic mixed with business logic

✅ With Repository (Good):

def create_student(student):
    if self.repository.get_by_email(student.email):
        raise HTTPException(400, "Email exists")
    return self.repository.create(student)
    # Clean separation: business logic only
```

---

### Layer 4: Service (Business Logic)

```python
# app/services/student_service.py

class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository
    
    def create_student(self, student: StudentCreate) -> StudentResponse:
        # Business Rule: Email must be unique
        existing = self.repository.get_by_email(student.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create student
        db_student = self.repository.create(student)
        
        # Convert to response
        return StudentResponse.model_validate(db_student)
    
    def get_student(self, student_id: int) -> StudentResponse:
        student = self.repository.get_by_id(student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return StudentResponse.model_validate(student)
```

**What it does:**

```
BUSINESS RULES:

┌─────────────────────────────────────────────────────────────┐
│ Rule 1: Email Must Be Unique                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ User tries to register: john@example.com                    │
│                                                             │
│ Service checks: Does this email exist?                      │
│ ├─ Yes → Return 400 "Email already registered"             │
│ └─ No  → Create student                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Rule 2: Student Must Exist                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ User requests: GET /students/999                            │
│                                                             │
│ Service checks: Does student 999 exist?                     │
│ ├─ Yes → Return student data                                │
│ └─ No  → Return 404 "Student not found"                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Service Layer Responsibilities:**

```
✅ Service Layer SHOULD:
- Validate business rules
- Orchestrate multiple repositories
- Handle business errors
- Transform data between layers

❌ Service Layer SHOULD NOT:
- Handle HTTP requests/responses
- Write SQL queries
- Know about FastAPI
- Access database directly
```

---

### Layer 5: Controller (API Endpoints)

```python
# app/controllers/student_controller.py

from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def register_student(
    student: StudentCreate,
    service: StudentService = Depends(get_student_service)
):
    return service.create_student(student)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    service: StudentService = Depends(get_student_service)
):
    return service.get_student(student_id)
```

**What it does:**

```
API ENDPOINTS:

┌─────────────────────────────────────────────────────────────┐
│ POST /students                                              │
├─────────────────────────────────────────────────────────────┤
│ Purpose: Create a new student                               │
│ Input: StudentCreate (name, email)                          │
│ Output: StudentResponse (id, name, email)                   │
│ Status: 201 Created                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ GET /students/{student_id}                                  │
├─────────────────────────────────────────────────────────────┤
│ Purpose: Get student by ID                                  │
│ Input: student_id (path parameter)                          │
│ Output: StudentResponse (id, name, email)                   │
│ Status: 200 OK                                              │
└─────────────────────────────────────────────────────────────┘
```

**Controller Responsibilities:**

```
✅ Controller SHOULD:
- Define HTTP routes
- Parse request parameters
- Call service methods
- Return HTTP responses
- Handle HTTP-specific concerns

❌ Controller SHOULD NOT:
- Implement business logic
- Access database
- Validate business rules
- Transform data
```

---

## 🔗 Dependency Injection Explained

```python
# app/dependencies/dependencies.py

def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    repository = StudentRepository(db)
    return StudentService(repository)
```

**How it works:**

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: FastAPI sees Depends(get_student_service)          │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Calls get_student_service()                         │
│         Which needs: db: Session = Depends(get_db)          │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Calls get_db()                                      │
│         Returns: Database session                           │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Creates repository with database session            │
│         repository = StudentRepository(db)                  │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Creates service with repository                     │
│         service = StudentService(repository)                │
└─────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Injects service into controller function            │
│         register_student(student, service)                  │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**

```
1. LOOSE COUPLING
   Controller doesn't create service
   Service doesn't create repository
   Each layer is independent

2. EASY TESTING
   Can inject mock service for testing
   Can inject mock repository for testing

3. AUTOMATIC CLEANUP
   Database session automatically closed
   Resources properly managed

4. FLEXIBILITY
   Can swap implementations easily
   Can add caching, logging, etc.
```

---

## 🎓 Enrollment System (Complex Example)

### The Problem

```
Many-to-Many Relationship:

Student ←→ Enrollment ←→ Course

One student can enroll in many courses
One course can have many students
```

### The Solution

```python
# app/models/enrollment_model.py

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),
    )
```

**Database Structure:**

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│    STUDENTS     │         │   ENROLLMENTS    │         │     COURSES     │
├─────────────────┤         ├──────────────────┤         ├─────────────────┤
│ id   │ name     │         │ id │ student_id  │         │ id   │ title    │
├──────┼──────────┤         ├────┼─────────────┤         ├──────┼──────────┤
│ 1    │ John     │◄────────┤ 1  │ 1  │ 1      ├────────►│ 1    │ Python   │
│ 2    │ Jane     │         │ 2  │ 1  │ 2      │         │ 2    │ Java     │
│ 3    │ Bob      │◄────────┤ 3  │ 2  │ 1      ├────────►│ 3    │ React    │
└──────┴──────────┘         │ 4  │ 3  │ 3      │         └──────┴──────────┘
                            └────┴────┴─────────┘

Interpretation:
- John (1) enrolled in Python (1) and Java (2)
- Jane (2) enrolled in Python (1)
- Bob (3) enrolled in React (3)
```

### Business Rules in Enrollment Service

```python
# app/services/enrollment_service.py

def enroll_student(self, enrollment: EnrollmentCreate):
    # Rule 1: Student must exist
    student = self.student_repo.get_by_id(enrollment.student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    
    # Rule 2: Course must exist
    course = self.course_repo.get_by_id(enrollment.course_id)
    if not course:
        raise HTTPException(404, "Course not found")
    
    # Rule 3: No duplicate enrollments
    if self.enrollment_repo.exists(enrollment.student_id, enrollment.course_id):
        raise HTTPException(400, "Already enrolled")
    
    # All checks passed - create enrollment
    return self.enrollment_repo.create(enrollment)
```

**Flow Diagram:**

```
User: Enroll student 1 in course 1
            ↓
┌───────────────────────────────────────┐
│ Check: Does student 1 exist?          │
│ Query: SELECT * FROM students         │
│        WHERE id = 1                   │
├───────────────────────────────────────┤
│ ✓ Yes → Continue                      │
│ ✗ No  → Return 404 "Student not found"│
└───────────────────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ Check: Does course 1 exist?           │
│ Query: SELECT * FROM courses          │
│        WHERE id = 1                   │
├───────────────────────────────────────┤
│ ✓ Yes → Continue                      │
│ ✗ No  → Return 404 "Course not found" │
└───────────────────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ Check: Already enrolled?              │
│ Query: SELECT * FROM enrollments      │
│        WHERE student_id = 1           │
│        AND course_id = 1              │
├───────────────────────────────────────┤
│ ✓ Exists → Return 400 "Already enrolled"│
│ ✗ Not exists → Continue               │
└───────────────────────────────────────┘
            ↓
┌───────────────────────────────────────┐
│ Create enrollment                     │
│ Query: INSERT INTO enrollments        │
│        (student_id, course_id)        │
│        VALUES (1, 1)                  │
├───────────────────────────────────────┤
│ Return: 201 Created                   │
└───────────────────────────────────────┘
```

---

## 🧪 Testing Scenarios

### Scenario 1: Happy Path

```
1. Create Course
   POST /courses
   {"title": "Python", "duration": 40}
   → 201 Created {id: 1, ...}

2. Register Student
   POST /students
   {"name": "John", "email": "john@example.com"}
   → 201 Created {id: 1, ...}

3. Enroll Student
   POST /enrollments
   {"student_id": 1, "course_id": 1}
   → 201 Created {id: 1, ...}

4. View Enrollments
   GET /enrollments/students/1/enrollments
   → 200 OK [{course_id: 1, course_title: "Python"}]
```

### Scenario 2: Duplicate Email

```
1. Register Student
   POST /students
   {"name": "John", "email": "john@example.com"}
   → 201 Created

2. Try Same Email Again
   POST /students
   {"name": "Jane", "email": "john@example.com"}
   → 400 Bad Request "Email already registered"
```

### Scenario 3: Duplicate Enrollment

```
1. Enroll Student
   POST /enrollments
   {"student_id": 1, "course_id": 1}
   → 201 Created

2. Try Same Enrollment Again
   POST /enrollments
   {"student_id": 1, "course_id": 1}
   → 400 Bad Request "Already enrolled"
```

### Scenario 4: Invalid Data

```
1. Invalid Email Format
   POST /students
   {"name": "John", "email": "not-an-email"}
   → 422 Unprocessable Entity

2. Missing Required Field
   POST /students
   {"name": "John"}
   → 422 Unprocessable Entity

3. Invalid Data Type
   POST /courses
   {"title": "Python", "duration": "forty"}
   → 422 Unprocessable Entity
```

---

## 📊 HTTP Status Codes Reference

```
┌──────┬─────────────────────┬──────────────────────────────────┐
│ Code │ Name                │ When to Use                      │
├──────┼─────────────────────┼──────────────────────────────────┤
│ 200  │ OK                  │ Successful GET request           │
│ 201  │ Created             │ Successful POST (created)        │
│ 400  │ Bad Request         │ Business rule violation          │
│ 404  │ Not Found           │ Resource doesn't exist           │
│ 422  │ Unprocessable       │ Validation error (invalid format)│
│ 500  │ Server Error        │ Unexpected error                 │
└──────┴─────────────────────┴──────────────────────────────────┘
```

**In LMS:**

```
200 OK
├─ GET /students/1 (student exists)
├─ GET /courses (list courses)
└─ GET /enrollments (list enrollments)

201 Created
├─ POST /students (student created)
├─ POST /courses (course created)
└─ POST /enrollments (enrollment created)

400 Bad Request
├─ Email already registered
└─ Already enrolled

404 Not Found
├─ Student not found
├─ Course not found
└─ Enrollment not found

422 Unprocessable Entity
├─ Invalid email format
├─ Missing required field
└─ Invalid data type
```

---

## 🎯 Key Takeaways

### 1. Separation of Concerns

```
Each layer has ONE job:

Controller  → Handle HTTP
Service     → Business logic
Repository  → Database operations
Schema      → Validation
Model       → Database structure
```

### 2. Dependency Flow

```
Controller depends on Service
Service depends on Repository
Repository depends on Database

But NOT the other way around!
```

### 3. Testing Strategy

```
Unit Tests:
├─ Service (mock repository)
├─ Repository (test database)
└─ Schemas (validation)

Integration Tests:
├─ Controller + Service + Repository
└─ Full API endpoints
```

### 4. Real-World Benefits

```
✅ Easy to maintain
✅ Easy to test
✅ Easy to extend
✅ Easy to understand
✅ Team can work on different layers
✅ Can swap implementations
```

---

## 🚀 Next Steps

1. **Run the application** and explore Swagger UI
2. **Test all endpoints** with different scenarios
3. **Read the code** layer by layer
4. **Modify** - Add a new field or entity
5. **Extend** - Add authentication or caching

**Practice makes perfect!** 🎓
