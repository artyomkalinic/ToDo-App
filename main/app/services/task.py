from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskId, TaskEdit
from app.models.user import User
from app.models.task import Task
from app.repositories.task import create_task_db, delete_task_db, edit_task_db

def create_task(task_data: TaskCreate, db: Session, current_user: User):
    return create_task_db(task_data, db, current_user)

def delete_task(task_data: TaskId, db: Session, current_user: User):
    return delete_task_db(task_data, db, current_user)

def edit_task(task_data: TaskId, task_to_edit: TaskEdit, db: Session, current_user: User):
    return edit_task_db(task_data, task_to_edit, db, current_user)