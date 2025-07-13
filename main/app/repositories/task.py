from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskId, TaskEdit
from app.schemas.task import TaskResponse
from app.models.user import User
from app.models.task import Task
from app.models.permission import Permission

def create_task_db(task_data: TaskCreate, db: Session, user: User) -> TaskResponse:

    task = Task(name=task_data.name, description=task_data.description, status=False, creator_id=user.id)

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

    task_response = TaskResponse(id=task.id, creator_id=task.creator_id)
    return task_response

def delete_task_db(task_data: TaskId, db: Session, user: User):
    task = db.query(Task).filter(Task.id == task_data.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You're not allowed to delete this task")
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}

def edit_task_db(task_data: TaskId, task_to_edit: TaskEdit, db: Session, user: User) -> Task:
    task = db.query(Task).filter(Task.id == task_data.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    perm = db.query(Permission).filter(Permission.task_id == task.id, 
                                       Permission.user_id == user.id,
                                       Permission.allowed_edit == True).first()
    
    if not perm:
        raise HTTPException(status_code=403, detail="Failed to edit the task")

    if task_to_edit.description is not None:
        task.description = task_to_edit.description
    
    if task_to_edit.status is not None:
        task.status = task_to_edit.status

    db.commit()
    db.refresh(task)

    return task