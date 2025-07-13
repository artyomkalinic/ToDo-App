from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserCreate

async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)

    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    query = select(User).filter(User.username == username)
    result = await db.execute(query)

    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str) -> User:
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except:
        await db.rollback()
        raise