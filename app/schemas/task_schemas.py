from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user_schemas import UserResponse

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None

class TaskAssignRequest(BaseModel):
    assignee_id: int

class TaskUpdateStatus(BaseModel):
    status: Optional[str] = None

class TaskUpdateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
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
