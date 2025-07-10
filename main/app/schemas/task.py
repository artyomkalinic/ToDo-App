from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    description: str

class TaskResponse(BaseModel):
    id: int
    creator_id: int
