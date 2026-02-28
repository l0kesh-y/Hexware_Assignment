from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.routers.user_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service")

app.include_router(router)