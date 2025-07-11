from pydantic import BaseModel

class PermissionCreate(BaseModel):
    task_id: int
    user_id: int
    allowed_edit: bool = False
    allowed_delete: bool = False