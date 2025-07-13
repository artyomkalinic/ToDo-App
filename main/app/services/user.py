from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.schemas.user import UserCreate
from app.repositories.auth import get_hashed_password, verify_password, create_access_token
from app.repositories.user import create_user, get_user_by_username

async def register_user(user: UserCreate, db: AsyncSession):
    
    if await get_user_by_username(db, user.username) is not None:
        raise HTTPException(status_code=403, detail="Username is already in use")
    
    hashed_password = await get_hashed_password(user.password)

    return await create_user(db, user, hashed_password)

async def login_user(username: str, password: str, db: AsyncSession):
    user = await get_user_by_username(db, username)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not await verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")
    
    access_token = await create_access_token(data={"id": str(user.id)})
    
    return user.id, access_token