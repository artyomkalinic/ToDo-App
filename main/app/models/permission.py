from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from app.database.db import Base
from app.models.user import User

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    allowed_edit = Column(Boolean, default=False)
    allowed_delete = Column(Boolean, default=False)