from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    UserNotFoundException,
    JobNotFoundException,
    ApplicationNotFoundException,
    DuplicateEmailException
)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "User not found", "detail": str(exc)}
        )
    
    @app.exception_handler(JobNotFoundException)
    async def job_not_found_handler(request: Request, exc: JobNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "Job not found", "detail": str(exc)}
        )
    
    @app.exception_handler(ApplicationNotFoundException)
    async def application_not_found_handler(request: Request, exc: ApplicationNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"error": "Application not found", "detail": str(exc)}
        )
    
    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(
            status_code=400,
            content={"error": "Duplicate email", "detail": str(exc)}
        )
