from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.db import get_db_connection
from app.services.user import register_user, login_user
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate


router = APIRouter()

@router.get("/main")
def main():
    return "- Say my name.\n - I don't know\n - You do know. You all do know who I am\n"


@router.get("/user/{user_id}")
def get_users(user_id: int, db: Session = Depends(get_db_connection)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user.id, "name": user.username}


@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db_connection)):
    try:
        user = register_user(user, db)
        return {"message": "Registration successful", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")
    

@router.post("/login", status_code=200)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_connection)):
    try:
        user_id, access_token = login_user(form_data.username, form_data.password, db)
        # response = RedirectResponse(url=f"/user/user/{user_id}", status_code=303)
        # response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="Lax", path="/", )
        # return response
        # return {"access_token": access_token,
        #         "token_type": "bearer",
        #         "user_id": user_id
        # }
        response = JSONResponse(content = {"message" : "Login successful", "user_id": user_id})
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="Lax", path="/", )
        return response

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")