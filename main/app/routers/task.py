from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db_connection
from app.repositories.auth import get_current_user
from app.services.task import create_task, delete_task, edit_task, get_current_tasks
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskId, TaskEdit


router = APIRouter()


@router.post("/create", status_code=201)
async def create(task_data: TaskCreate, db: AsyncSession = Depends(get_db_connection), current_user: User = Depends(get_current_user)):
    try:
        return await create_task(task_data, db, current_user)
    except HTTPException as e:
        raise e
    

@router.delete("/delete", status_code=204)
async def delete(task_data: TaskId, db: AsyncSession = Depends(get_db_connection), current_user: User = Depends(get_current_user)):
    try:
       return await delete_task(task_data, db, current_user)
    except HTTPException as e:
        raise e


@router.patch("/edit", status_code=200)
async def edit(task_data: TaskId, task_to_edit: TaskEdit, db: AsyncSession = Depends(get_db_connection), current_user: User = Depends(get_current_user)):
    try:
        return await edit_task(task_data, task_to_edit, db, current_user)
    except HTTPException as e:
        raise e
    

@router.get("/get_current", status_code=201)
async def get_current(db: AsyncSession = Depends(get_db_connection), current_user: User = Depends(get_current_user)):
    try:
        return await get_current_tasks(db, current_user)
    except HTTPException as e:
        raise e