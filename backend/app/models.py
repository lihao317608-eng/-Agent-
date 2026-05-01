from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    tasks = relationship("ContentTask", back_populates="owner")

class ContentTask(Base):
    __tablename__ = "content_tasks"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(255), nullable=False)
    platform = Column(String(50), nullable=False)
    count = Column(Integer, default=5)
    status = Column(String(30), default="queued")

    trend_output = Column(Text)
    generated_output = Column(Text)
    rewritten_output = Column(Text)
    evaluated_output = Column(Text)
    error_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="tasks")
