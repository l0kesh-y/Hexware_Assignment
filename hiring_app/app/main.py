from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base
from app.controllers import user_controller, job_controller, application_controller
from app.middleware.cors import setup_cors
from app.middleware.logging import setup_logging
from app.exceptions.exception_handlers import setup_exception_handlers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hiring Application API", version="1.0.0")

# Setup middleware
setup_cors(app)
setup_logging(app)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(user_controller.router, prefix="/users", tags=["Users"])
app.include_router(job_controller.router, prefix="/jobs", tags=["Jobs"])
app.include_router(application_controller.router, prefix="/applications", tags=["Applications"])

@app.get("/")
def root():
    return {"message": "Hiring Application API"}
