from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers import auth_router, itadmin_router, employee_router, manager_router
from app.middleware.logging import setup_logging
from app.middleware.exception_handler import setup_exception_handlers

# Import all models to ensure they are registered with SQLAlchemy
from app.models import user, department, asset, asset_assignment, asset_request

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise Asset Management System",
    version="1.0.0",
    description="RBAC-based asset management with JWT authentication"
)

# Setup middleware
setup_logging(app)
setup_exception_handlers(app)

# Include routers
app.include_router(auth_router.router)
app.include_router(itadmin_router.router)
app.include_router(employee_router.router)
app.include_router(manager_router.router)

@app.get("/")
def root():
    return {
        "message": "Enterprise Asset Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
