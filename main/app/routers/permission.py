from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db_connection
from app.repositories.auth import get_current_user
from app.services.permission import give_permission_task
from app.models.user import User
from app.schemas.user import UserId
from app.schemas.permission import PermissionCreate

router = APIRouter()


@router.post("/give")
def give_permission(task_data: PermissionCreate,
                    to_user: UserId, 
                    db: Session = Depends(get_db_connection), 
                    current_user: User = Depends(get_current_user) 
                    
):
    try:
        return give_permission_task(task_data, to_user, db, current_user)
    except HTTPException as e:
        raise e