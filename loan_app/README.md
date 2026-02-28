# Loan Application & Approval Management System

A fintech backend API system for digitizing loan processing workflow built with FastAPI following Clean Architecture principles.

## Business Problem

Replaces manual loan processing with:
- Automated eligibility validation
- Structured approval workflow
- Real-time status tracking
- Complete audit trail

## Features

- Submit loan applications
- Automatic eligibility validation
- Approve/Reject loans with business rules
- Track application status
- List all applications

## Business Rules

1. **Eligibility Rule**: Maximum loan = Income × 10
2. **Auto-Rejection**: Applications exceeding eligibility are auto-rejected
3. **Status Validation**: Only PENDING loans can be approved or rejected
4. **State Transition**: Cannot approve/reject already processed loans

## Architecture

Clean Architecture with clear separation of concerns:

```
Controller → Service → Repository → Database
```

### Layer Responsibilities

- **Controller**: HTTP endpoints, request/response handling
- **Service**: Business logic, eligibility validation, state transitions
- **Repository**: Database operations (CRUD)
- **Schema**: Request/response validation with Pydantic
- **Model**: Database table definitions
- **Dependencies**: Dependency injection for loose coupling
- **Middleware**: Cross-cutting concerns (CORS)

## Installation

1. Install dependencies:
```bash
cd loan_app
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## API Documentation

Interactive Swagger UI: http://localhost:8000/docs

## API Endpoints

### Submit Loan Application
```
POST /loans
```

**Request Body:**
```json
{
  "applicant_name": "Rahul Kumar",
  "income": 50000,
  "loan_amount": 200000
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "applicant_name": "Rahul Kumar",
  "income": 50000,
  "loan_amount": 200000,
  "status": "PENDING"
}
```

### Get Loan Application by ID
```
GET /loans/{loan_id}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "applicant_name": "Rahul Kumar",
  "income": 50000,
  "loan_amount": 200000,
  "status": "PENDING"
}
```

**Error (404 Not Found):**
```json
{
  "detail": "Loan application not found"
}
```

### Get All Loan Applications
```
GET /loans
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "applicant_name": "Rahul Kumar",
    "loan_amount": 200000,
    "status": "PENDING"
  },
  {
    "id": 2,
    "applicant_name": "Anita Sharma",
    "loan_amount": 300000,
    "status": "APPROVED"
  }
]
```

### Approve Loan
```
PUT /loans/{loan_id}/approve
```

**Response (200 OK):**
```json
{
  "message": "Loan approved successfully",
  "status": "APPROVED"
}
```

**Error - Exceeds Eligibility (400 Bad Request):**
```json
{
  "detail": "Loan amount exceeds eligibility limit"
}
```

**Error - Invalid Status (400 Bad Request):**
```json
{
  "detail": "Only pending loans can be approved"
}
```

### Reject Loan
```
PUT /loans/{loan_id}/reject
```

**Response (200 OK):**
```json
{
  "message": "Loan rejected",
  "status": "REJECTED"
}
```

## Example Usage with cURL

### Submit Application
```bash
curl -X POST "http://localhost:8000/loans" \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_name": "Rahul Kumar",
    "income": 50000,
    "loan_amount": 200000
  }'
```

### Get Application
```bash
curl -X GET "http://localhost:8000/loans/1"
```

### Approve Loan
```bash
curl -X PUT "http://localhost:8000/loans/1/approve"
```

### Reject Loan
```bash
curl -X PUT "http://localhost:8000/loans/1/reject"
```

## HTTP Status Codes

| Scenario | Status Code |
|----------|-------------|
| Loan created | 201 |
| Fetch success | 200 |
| Not found | 404 |
| Business validation failed | 400 |
| Invalid input | 422 |

## Project Structure

```
loan_app/
├── app/
│   ├── main.py                      # Application entry point
│   ├── core/
│   │   └── config.py                # Configuration & DB setup
│   ├── models/
│   │   └── loan_model.py            # Database model
│   ├── schemas/
│   │   └── loan_schema.py           # Pydantic schemas
│   ├── repositories/
│   │   └── loan_repository.py       # Data access layer
│   ├── services/
│   │   └── loan_service.py          # Business logic
│   ├── controllers/
│   │   └── loan_controller.py       # API routes
│   ├── dependencies/
│   │   └── loan_dependency.py       # Dependency injection
│   └── middleware/
│       └── cors.py                  # CORS configuration
├── requirements.txt
└── README.md
```

## Technology Stack

- **FastAPI**: Modern web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **SQLite**: Database
- **Uvicorn**: ASGI server

## Business Logic Highlights

### Eligibility Calculation
```python
max_eligible_loan = income × 10
```

### Auto-Rejection
Applications with `loan_amount > max_eligible_loan` are automatically rejected upon submission.

### State Machine
```
PENDING → APPROVED
PENDING → REJECTED
```

Only PENDING applications can transition to APPROVED or REJECTED states.

## Testing the API

1. Start the server
2. Visit http://localhost:8000/docs
3. Use the interactive Swagger UI to test all endpoints
4. Try different scenarios:
   - Submit valid application
   - Submit application exceeding eligibility
   - Approve pending loan
   - Try to approve already approved loan (should fail)

## Future Enhancements

- Authentication & Authorization
- Payment integration
- Document upload
- Credit score integration
- Email notifications
- Loan repayment tracking
