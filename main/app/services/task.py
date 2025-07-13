from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskId, TaskEdit
from app.models.user import User
from app.models.task import Task
from app.repositories.task import create_task_db, delete_task_db, edit_task_db, get_task_by_id
from app.repositories.permission import get_allowed_to_edit_perm

async def create_task(task_data: TaskCreate, db: AsyncSession, current_user: User):
    return await create_task_db(task_data, db, current_user)


async def delete_task(task_data: TaskId, db: AsyncSession, current_user: User):
    task = await get_task_by_id(task_data, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="You're not allowed to delete this task")
    
    return await delete_task_db(task_data, db)


async def edit_task(task_data: TaskId, task_to_edit: TaskEdit, db: AsyncSession, current_user: User):
    task = await get_task_by_id(task_data, db)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    perm = await get_allowed_to_edit_perm(task, current_user, db)
    
    if not perm:
        raise HTTPException(status_code=403, detail="Failed to edit the task")

    if task_to_edit.description is not None:
        task.description = task_to_edit.description
    
    if task_to_edit.status is not None:
        task.status = task_to_edit.status

    return await edit_task_db(task, db)