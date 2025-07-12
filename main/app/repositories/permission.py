from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.permission import PermissionCreate
from app.models.user import User
from app.models.task import Task
from app.models.permission import Permission

def give_permission_task_db(task_data: PermissionCreate, to_user: User, db: Session, current_user: User):
    task = db.query(Task).filter(Task.id == task_data.task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can give permission")

    is_permission_exists = db.query(Permission).filter(Permission.task_id == task.id, 
                                                       Permission.user_id == to_user.id).first()
    
    if is_permission_exists:
        raise HTTPException(status_code=403, detail="Permission already exists")
    
    permission = Permission(task_id=task_data.task_id, 
                            user_id=to_user.id,
                            allowed_edit=True,
                            allowed_delete=False)
    db.add(permission)
    db.commit()
    db.refresh(permission)

    return {"message": "Permission is given"}