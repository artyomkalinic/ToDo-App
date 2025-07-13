from sqlalchemy.orm import Session
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except:
        db.rollback()
        raise