from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.permission import PermissionCreate, PermissionTaskUserId
from app.models.task import Task
from app.models.user import User
from app.repositories.permission import give_permission_task_db, take_permission_task_db, get_perm_by_user_task_id, get_task_by_task_id


async def give_permission_task(task_data: PermissionCreate, to_user: User, db: AsyncSession, creator_user: User):
    task = await get_task_by_task_id(task_data, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != creator_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can give permission")
    
    is_permission_exists = await get_perm_by_user_task_id(task_data, to_user, db)
    
    if is_permission_exists:
        raise HTTPException(status_code=403, detail="Permission already exists")
    
    return await give_permission_task_db(task_data, to_user, db)


async def take_permission_task(task_data: PermissionTaskUserId, from_user: User, db: AsyncSession, creator_user: User):
    task = await get_task_by_task_id(task_data, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != creator_user.id:
        raise HTTPException(status_code=403, detail="Only the creator can take permission")

    permission = await get_perm_by_user_task_id(task_data, from_user, db)
    
    if not permission:
        raise HTTPException(status_code=404, detail="Permission doesn't exist")
    
    return await take_permission_task_db(permission, db)