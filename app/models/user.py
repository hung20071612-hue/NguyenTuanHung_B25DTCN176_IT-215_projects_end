import enum
from app.db.database import Base 
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    owned_projects = relationship("ResearchProjectModel", back_populates="owner")
    memberships = relationship("ResearchMemberModel", back_populates="user")
    assigned_tasks = relationship("ResearchTaskModel", back_populates="assignee")
