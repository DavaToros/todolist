from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="todo api", description="todo лист", lifespan=lifespan)

app.include_router(router)
