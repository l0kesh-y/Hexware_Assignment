from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    UserNotFoundException,
    ProductNotFoundException,
    ApplicationNotFoundException,
    DuplicateEmailException,
    InvalidLoanAmountException,
    InvalidStatusTransitionException,
    InvalidRepaymentException
)

def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=404, content={"error": "User not found", "detail": str(exc)})
    
    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(request: Request, exc: ProductNotFoundException):
        return JSONResponse(status_code=404, content={"error": "Product not found", "detail": str(exc)})
    
    @app.exception_handler(ApplicationNotFoundException)
    async def application_not_found_handler(request: Request, exc: ApplicationNotFoundException):
        return JSONResponse(status_code=404, content={"error": "Application not found", "detail": str(exc)})
    
    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(status_code=400, content={"error": "Duplicate email", "detail": str(exc)})
    
    @app.exception_handler(InvalidLoanAmountException)
    async def invalid_loan_amount_handler(request: Request, exc: InvalidLoanAmountException):
        return JSONResponse(status_code=400, content={"error": "Invalid loan amount", "detail": str(exc)})
    
    @app.exception_handler(InvalidStatusTransitionException)
    async def invalid_status_handler(request: Request, exc: InvalidStatusTransitionException):
        return JSONResponse(status_code=400, content={"error": "Invalid status transition", "detail": str(exc)})
    
    @app.exception_handler(InvalidRepaymentException)
    async def invalid_repayment_handler(request: Request, exc: InvalidRepaymentException):
        return JSONResponse(status_code=400, content={"error": "Invalid repayment", "detail": str(exc)})
