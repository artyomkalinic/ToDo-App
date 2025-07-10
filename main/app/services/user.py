from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.user import UserCreate
from app.repositories.auth import get_hashed_password, verify_password, verify_token, create_access_token
from app.repositories.user import create_user, get_user_by_username, get_user_by_id, is_user_an_admin

def register_user(user: UserCreate, db: Session):
    hashed_password = get_hashed_password(user.password)
    create_user(db, user, hashed_password)

def login_user(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    is_admin = is_user_an_admin(db, user.id)
    
    access_token = create_access_token(data={"sub": str(user.id), "is_admin": is_admin})
    
    return user.id, access_token