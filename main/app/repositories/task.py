from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.task import TaskCreate
from app.schemas.task import TaskResponse
from app.models.user import User
from app.models.task import Task
from app.models.permission import Permission


async def get_task_by_id(task_data, db: AsyncSession) -> Task:
    task_query = select(Task).filter(Task.id == task_data.id)
    task_result = await db.execute(task_query)
    task = task_result.scalars().first()

    return task


async def create_task_db(task_data: TaskCreate, db: AsyncSession, user: User) -> TaskResponse:
    task = Task(name=task_data.name, description=task_data.description, status=False, creator_id=user.id)

    db.add(task)
    await db.commit()
    await db.refresh(task)


    permission = Permission(task_id=task.id,
                            user_id=user.id,
                            allowed_edit=True,
                            allowed_delete=True)
    
    db.add(permission)
    await db.commit()
    await db.refresh(permission)

    task_response = TaskResponse(id=task.id, creator_id=task.creator_id)

    return task_response


async def delete_task_db(task, db: AsyncSession):
    db.delete(task)
    await db.commit()

    return {"message": "Task deleted"}


async def edit_task_db(task, db) -> Task:
    await db.commit()
    await db.refresh(task)

    return task

async def get_current_tasks_db(db: AsyncSession, current_user: User) -> List[Task]:
    task_query = select(Task).filter(Task.creator_id == current_user.id)
    task_result = await db.execute(task_query)
    tasks = task_result.scalars().all()

    return tasks