from fastapi import FastAPI
from app.core.db import init_db
from app.middleware.cors import setup_cors
from app.controllers import student_controller, course_controller, enrollment_controller

app = FastAPI(
    title="Learning Management System API",
    description="Course Enrollment Platform with Clean Architecture",
    version="1.0.0"
)

# Setup middleware
setup_cors(app)

# Initialize database
@app.on_event("startup")
def startup_event():
    init_db()

# Include routers
app.include_router(student_controller.router)
app.include_router(course_controller.router)
app.include_router(enrollment_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to LMS API"}
