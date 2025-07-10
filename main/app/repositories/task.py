from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate
from app.models.user import User
from app.models.task import Task

def create_task_db(task_data: TaskCreate, db: Session, user_id: int) -> Task:
    task = Task(name=task_data.name, description=task_data.description, creator_id=user_id)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task
