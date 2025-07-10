from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate
from app.models.user import User
from app.models.task import Task
from app.repositories.task import create_task_db

def create_task(task_data: TaskCreate, db: Session, current_user: User):
    return create_task_db(task_data, db, current_user.id)