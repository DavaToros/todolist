from fastapi import FastAPI
from app.database import init_db
from app.routes import router

app = FastAPI(title="Todo API", description="Простой REST API для задач", version="1.0")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router)