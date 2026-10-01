
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.models.task import TaskORM
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)
app.include_router(router=category_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)