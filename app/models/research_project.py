import enum
from app.db.database import Base 
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

class MemberRole(str, enum.Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"

class ResearchProjectModel(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    owner = relationship("UserModel", back_populates="owned_projects")
    members = relationship("ResearchMemberModel", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("ResearchTaskModel", back_populates="project", cascade="all, delete-orphan")

class ResearchMemberModel(Base):
    __tablename__ = "research_members"

    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(Enum(MemberRole),default=MemberRole.MEMBER , nullable=False)
    joined_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project = relationship("ResearchProjectModel", back_populates="members")
    user = relationship("UserModel", back_populates="memberships")
