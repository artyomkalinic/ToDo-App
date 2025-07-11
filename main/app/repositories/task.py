from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskDelete
from app.schemas.permission import PermissionCreate
from app.models.user import User
from app.models.task import Task
from app.models.permission import Permission

def create_task_db(task_data: TaskCreate, db: Session, user: User) -> Task:

    task = Task(name=task_data.name, description=task_data.description, creator_id=user.id)

    db.add(task)
    db.commit()
    db.refresh(task)


    permission = Permission(task_id=task.id,
                            user_id=user.id,
                            allowed_edit=True,
                            allowed_delete=True)
    
    db.add(permission)
    db.commit()
    db.refresh(permission)


    return task

def delete_task_db(task_data: TaskDelete, db: Session, user: User):
    task = db.query(Task).filter(Task.id == task_data.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You're not allowed to delete this task")
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}