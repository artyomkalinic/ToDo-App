from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.db import get_db_connection
from app.repositories.auth import get_current_user
from app.services.task import create_task
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter()

@router.post("/create")
def create(task_data: TaskCreate, db: Session = Depends(get_db_connection), current_user: User = Depends(get_current_user)):
    try:
        create_task(task_data, db, current_user)
    except HTTPException as e:
        raise e


