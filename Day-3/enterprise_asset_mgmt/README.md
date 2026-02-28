# Enterprise Asset Management System (EAMS)

Complete enterprise-grade asset management system with JWT authentication and role-based access control.

## Features

- **Multi-Role Support**: SuperAdmin, IT Admin, Manager, Employee
- **Asset Management**: Track laptops, monitors, licenses, vehicles, etc.
- **Assignment Tracking**: Assign assets to employees with full audit trail
- **Request Workflow**: Employees request assets, IT Admin approves
- **Department Management**: Organize assets and users by department
- **RBAC**: Role-based access control for all operations
- **Audit Trail**: Complete history of all asset movements

## Roles & Permissions

| Feature | SuperAdmin | IT Admin | Manager | Employee |
|---------|-----------|----------|---------|----------|
| Create Asset | ✅ | ✅ | ❌ | ❌ |
| Assign Asset | ✅ | ✅ | ❌ | ❌ |
| View Department Assets | ✅ | ✅ | ✅ | ❌ |
| View Own Assets | ✅ | ✅ | ✅ | ✅ |
| Request Asset | ❌ | ❌ | ❌ | ✅ |
| Approve Request | ✅ | ✅ | ❌ | ❌ |

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database in `.env`:
```
DATABASE_URL=postgresql://postgres:root@localhost/asset_management
SECRET_KEY=your-secret-key-here
```

3. Create database:
```bash
python -c "import psycopg2; conn = psycopg2.connect('host=localhost user=postgres password=root'); conn.autocommit = True; cur = conn.cursor(); cur.execute('CREATE DATABASE asset_management')"
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login and get JWT token

### IT Admin Endpoints
- POST /itadmin/assets - Create asset
- GET /itadmin/assets - List all assets (with pagination & filtering)
- POST /itadmin/assignments - Assign asset to user
- PATCH /itadmin/assignments/{id}/return - Return asset
- GET /itadmin/requests - View all asset requests
- PATCH /itadmin/requests/{id}/approve - Approve/reject request

### Employee Endpoints
- POST /employee/requests - Request an asset
- GET /employee/requests - View my requests
- GET /employee/assets - View my assigned assets

### Manager Endpoints
- GET /manager/assets - View department assets

## Workflows

### Employee Requests Laptop
1. Employee: POST /employee/requests
2. IT Admin: GET /itadmin/requests (sees pending request)
3. IT Admin: PATCH /itadmin/requests/{id}/approve
4. System automatically assigns available laptop
5. Employee: GET /employee/assets (sees assigned laptop)

### Asset Return
1. IT Admin: PATCH /itadmin/assignments/{id}/return
2. System updates asset status to AVAILABLE
3. Asset ready for next assignment

## Database Schema

### Users
- id, name, email, password, role, department_id

### Departments
- id, name, manager_id

### Assets
- id, asset_tag (unique), asset_type, brand, model, purchase_date, status, department_id

### Asset Assignments
- id, asset_id, user_id, assigned_date, returned_date, condition_on_return

### Asset Requests
- id, employee_id, asset_type, reason, status, approved_by

## Testing

Run tests:
```bash
pytest tests/ -v
```

## Security

- JWT authentication
- Password hashing with bcrypt
- Role-based authorization
- SQL injection protection via ORM
