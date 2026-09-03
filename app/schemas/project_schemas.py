from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.user_schemas import UserResponse
from app.models.research_project import MemberRole

class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class MemberAddRequest(BaseModel):
    user_id: int
    role: MemberRole = MemberRole.MEMBER

class MemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
