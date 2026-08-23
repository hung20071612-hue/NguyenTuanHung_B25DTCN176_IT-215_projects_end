from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user_schemas import UserResponse

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    created_at: datetime
    assignee: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
