from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.db import get_db_connection
from app.models.user import User, Admin
from app.schemas.user import UserCreate
from app.services.user import register_user, login_user
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


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db_connection)):
    try:
        register_user(user, db)
        return RedirectResponse(url="/api/main", status_code=303)
    except Exception as e:
        print("Registration error:", e) 
        raise HTTPException(status_code=500, detail="Registration failed")
    

@router.post("/login", response_class=RedirectResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_connection)):
    try:
        user_id, access_token = login_user(form_data.username, form_data.password, db)
        response = RedirectResponse(url=f"/api/user/{user_id}", status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        return response
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")
