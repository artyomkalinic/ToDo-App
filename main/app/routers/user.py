from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db_connection
from app.services.user import register_user, login_user
from app.schemas.user import UserCreate


router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db_connection)):
    try:
        user = await register_user(user, db)
        return {"message": "Registration successful", "user_id": user.id}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Registration failed")
    

@router.post("/login", status_code=200)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_connection)):
    try:
        user_id, access_token = await login_user(form_data.username, form_data.password, db)

        response = JSONResponse(content = {"message" : "Login successful", "user_id": user_id})
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="Lax", path="/", )
        
        return response

    except HTTPException as e:
        raise e
    
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")