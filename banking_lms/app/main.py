from fastapi import FastAPI
from app.core.database import engine, Base
from app.controllers import user_controller, product_controller, application_controller, repayment_controller
from app.middleware.cors import setup_cors
from app.middleware.logging_middleware import setup_logging
from app.exceptions.exception_handlers import setup_exception_handlers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banking Loan Management System", version="1.0.0")

# Setup middleware
setup_cors(app)
setup_logging(app)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(user_controller.router, prefix="/users", tags=["Users"])
app.include_router(product_controller.router, prefix="/loan-products", tags=["Loan Products"])
app.include_router(application_controller.router, prefix="/loan-applications", tags=["Loan Applications"])
app.include_router(repayment_controller.router, prefix="/repayments", tags=["Repayments"])

@app.get("/")
def root():
    return {"message": "Banking Loan Management System API"}
