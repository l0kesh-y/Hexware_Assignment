from fastapi import FastAPI
from app.core.config import init_db
from app.middleware.cors import setup_cors
from app.controllers import loan_controller

app = FastAPI(
    title="Loan Application & Approval Management System",
    description="Fintech Loan Processing API with Clean Architecture",
    version="1.0.0"
)

# Setup middleware
setup_cors(app)

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()

# Include routers
app.include_router(loan_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to Loan Management API"}
