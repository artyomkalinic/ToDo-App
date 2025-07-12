from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    name: str
    description: str

class TaskResponse(BaseModel):
    id: int
    creator_id: int

class TaskId(BaseModel):
    id: int

class TaskEdit(BaseModel):
    description: Optional[str] = None
    status: Optional[bool] = None
