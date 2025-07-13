from sqlalchemy.orm import Session
from app.schemas.permission import PermissionCreate, PermissionTaskUserId
from app.models.task import Task
from app.models.user import User
from app.repositories.permission import give_permission_task_db, take_permission_task_db

def give_permission_task(task_data: PermissionCreate, to_user: User, db: Session, creator_user: User):
    return give_permission_task_db(task_data, to_user, db, creator_user)

def take_permission_task(task_data: PermissionTaskUserId, from_user: User, db: Session, creator_user: User):
    return take_permission_task_db(task_data, from_user, db, creator_user)