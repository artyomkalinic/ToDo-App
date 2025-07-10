from fastapi import FastAPI
from app.routers import user, task

app = FastAPI()

app.include_router(user.router, prefix="/api")
app.include_router(task.router, prefix="/task")