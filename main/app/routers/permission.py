from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db_connection
from app.repositories.auth import get_current_user
from app.services.permission import give_permission_task, take_permission_task
from app.models.user import User
from app.schemas.user import UserId
from app.schemas.permission import PermissionCreate, PermissionTaskUserId


router = APIRouter()


@router.post("/give")
async def give_permission(task_data: PermissionCreate,
                    to_user: UserId, 
                    db: AsyncSession = Depends(get_db_connection), 
                    current_user: User = Depends(get_current_user) 
                    
):
    try:
        return await give_permission_task(task_data, to_user, db, current_user)
    except HTTPException as e:
        raise e


@router.delete("/take")
async def take_permission(task_data: PermissionTaskUserId,
                    from_user: UserId,
                    db: AsyncSession = Depends(get_db_connection), 
                    current_user: User = Depends(get_current_user)
):
    try:
        return await take_permission_task(task_data, from_user, db, current_user)
    except HTTPException as e:
        raise e