from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserId(BaseModel):
    id: int