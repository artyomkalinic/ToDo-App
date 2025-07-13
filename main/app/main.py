from fastapi import FastAPI
from app.routers import user, task, permission

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(task.router, prefix="/task")
app.include_router(permission.router, prefix="/permission")

# rm ~/.docker/config.json