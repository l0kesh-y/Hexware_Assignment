from fastapi import FastAPI, Request
import logging
import time

logger = logging.getLogger("banking_lms")

def setup_logging(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
        return response
