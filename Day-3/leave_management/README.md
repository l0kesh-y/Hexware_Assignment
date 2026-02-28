# Enterprise Leave Management System (ELMS)

Complete enterprise-grade leave management system with JWT authentication and role-based access control.

## Features

- JWT Authentication with secure password hashing
- Role-Based Access Control (RBAC)
  - Admin: Full system access
  - Manager: Department-level access
  - Employee: Personal leave management
- Leave request workflow (Apply → Approve/Reject)
- Department management
- Overlap detection for leave requests
- Pagination support
- Comprehensive logging
- Global exception handling

## Architecture

- **Controllers**: HTTP request handling
- **Services**: Business logic and validation
- **Repositories**: Database operations
- **Models**: SQLAlchemy ORM
- **Schemas**: Pydantic validation
- **Dependencies**: RBAC and authentication
- **Middleware**: Logging and exception handling

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/leave_management
SECRET_KEY=your-secret-key-here
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login and get JWT token

### Employee Endpoints (Requires Authentication)
- POST /employee/leaves - Apply for leave
- GET /employee/leaves - Get my leave requests
- GET /employee/leaves/{id} - Get specific leave request

### Manager Endpoints (Requires Manager Role)
- GET /manager/employees - Get department employees
- GET /manager/leaves - Get department leave requests
- PATCH /manager/leaves/{id}/approve - Approve/reject leave

### Admin Endpoints (Requires Admin Role)
- GET /admin/users - List all users
- POST /admin/departments - Create department
- GET /admin/departments - List departments
- PUT /admin/departments/{id} - Update department
- DELETE /admin/departments/{id} - Delete department
- GET /admin/leaves - List all leaves
- PATCH /admin/leaves/{id}/status - Override leave status

## Authentication Flow

1. Register user: POST /auth/register
2. Login: POST /auth/login (returns JWT token)
3. Use token in Authorization header: `Bearer <token>`

## Role-Based Access

- **ADMIN**: Full CRUD on users, departments, leaves
- **MANAGER**: View department employees, approve/reject leaves
- **EMPLOYEE**: Apply for leave, view own leaves

## Business Rules

1. Leave dates must be valid (start < end)
2. No overlapping leave requests
3. Only managers can approve leaves in their department
4. Admin can override any leave status
5. Leave status: PENDING → APPROVED/REJECTED

## Database Schema

### Users
- id, name, email, password, role, department_id

### Departments
- id, name, manager_id

### LeaveRequests
- id, employee_id, start_date, end_date, reason, status, approved_by

## Testing

Run tests:
```bash
pytest tests/
```

## Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Role-based authorization
- SQL injection protection via ORM
