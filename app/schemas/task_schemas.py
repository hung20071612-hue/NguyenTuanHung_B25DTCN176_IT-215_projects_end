from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user_schemas import UserResponse
from app.models.research_task import TaskStatus, TaskPriority

class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskAssignRequest(BaseModel):
    assignee_id: int

class TaskUpdateStatus(BaseModel):
    status: Optional[str] = None

class TaskUpdateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority
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
