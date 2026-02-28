# Banking Loan Management System

Enterprise-grade FastAPI backend for managing loan products, applications, and repayments.

## Features

- User management (admin, loan_officer, customer roles)
- Loan product management
- Loan application processing with approval workflow
- Repayment tracking with automatic loan closure
- Business rule validation
- Transaction management
- Pagination support

## Architecture

- **Controller Layer**: HTTP request handling
- **Service Layer**: Business logic, validation, and transactions
- **Repository Layer**: Database operations
- **Models**: SQLAlchemy ORM models with relationships
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

4. Update `alembic/env.py` to import Base:
```python
from app.core.database import Base
target_metadata = Base.metadata
```

5. Generate migration:
```bash
alembic revision --autogenerate -m "initial schema"
```

6. Apply migration:
```bash
alembic upgrade head
```

7. Run the application:
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

### Loan Products
- POST /loan-products - Create loan product
- GET /loan-products/{product_id} - Get product
- GET /loan-products?skip=0&limit=10 - List products (paginated)
- PUT /loan-products/{product_id} - Update product
- DELETE /loan-products/{product_id} - Delete product

### Loan Applications
- POST /loan-applications - Apply for loan
- GET /loan-applications/{id} - Get application
- GET /loan-applications?skip=0&limit=10 - List applications (paginated)
- PUT /loan-applications/{id}/status - Update application status

### Repayments
- POST /repayments - Add repayment
- GET /repayments/loan-applications/{id}/repayments - Get repayment history

## Business Rules

1. Requested amount cannot exceed product max_amount
2. Only loan officers can approve/reject applications
3. Loans can only be disbursed if status is "approved"
4. Repayments can only be made for disbursed loans
5. Loan automatically closes when fully repaid
6. All financial operations use database transactions

## Database Schema

### Users
- id, name, email (unique), role, hashed_password

### LoanProducts
- id, product_name, interest_rate, max_amount, tenure_months, description

### LoanApplications
- id, user_id (FK), product_id (FK), requested_amount, approved_amount, status, processed_by (FK)

### Repayments
- id, loan_application_id (FK), amount_paid, payment_date, payment_status
