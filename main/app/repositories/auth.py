import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.db import get_db_connection
from app.models.user import User
from app.models.task import Task

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRED_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)

    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    
    except JWTError:
        return None

def verify_password(entered_password: str, hashed_password: str):
    return pwd_context.verify(entered_password, hashed_password)

def get_hashed_password(entered_password: str):
    return pwd_context.hash(entered_password)


def get_current_user(request: Request, db: Session = Depends(get_db_connection)):
    token = request.cookies.get("access_token")
   
    if token is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    if (token.startswith("Bearer ")):
        token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise HTTPException(status_code=403, detail="User not found")

        return user 

    except JWTError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
