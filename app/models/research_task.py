from app.db.database import Base 
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime,timezone

class ResearchTaskModel(Base):
    __tablename__ = "research_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(50), default="TODO", nullable=False)
    priority = Column(String(50), default="MEDIUM", nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    project = relationship("ResearchProjectModel", back_populates="tasks")
    assignee = relationship("UserModel", back_populates="assigned_tasks")
