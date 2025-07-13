from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.permission import PermissionCreate
from app.models.user import User
from app.models.task import Task
from app.models.permission import Permission

async def get_task_by_task_id(task_data, db: AsyncSession):
    task_query = select(Task).filter(Task.id == task_data.task_id)
    task_result = await db.execute(task_query)
    task = task_result.scalars().first()

    return task


async def get_perm_by_user_task_id(task, user, db: AsyncSession):
    perm_query = select(Permission).filter(Permission.task_id == task.task_id, Permission.user_id == user.id)
    perm_result = await db.execute(perm_query)
    perm = perm_result.scalars().first()

    return perm


async def get_allowed_to_edit_perm(task, current_user, db:AsyncSession):
    query = select(Permission).filter(Permission.task_id == task.id, 
                                      Permission.user_id == current_user.id,
                                      Permission.allowed_edit == True)
    result = await db.execute(query)
    perm = result.scalars().first()

    return perm


async def give_permission_task_db(task_data: PermissionCreate, to_user: User, db: AsyncSession):
    permission = Permission(task_id=task_data.task_id, 
                            user_id=to_user.id,
                            allowed_edit=True,
                            allowed_delete=False)
    
    db.add(permission)
    await db.commit()
    await db.refresh(permission)

    return {"message": "Permission is given"}


async def take_permission_task_db(permission: Permission, db: AsyncSession):
    db.delete(permission)
    await db.commit()

    return {"message": "Permission is taken"}