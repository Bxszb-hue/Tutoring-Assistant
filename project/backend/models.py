from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True)
    user_type = Column(String(20))  # student, counselor, admin
    name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Conversation(Base):
    """对话表"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"))
    agent_type = Column(String(50))
    content = Column(Text)
    role = Column(String(20))  # user, assistant
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Task(Base):
    """任务表"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), ForeignKey("users.user_id"))
    task_type = Column(String(50))
    task_status = Column(String(20))  # pending, processing, completed, failed
    task_data = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Alert(Base):
    """预警表"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"))
    alert_type = Column(String(50))  # academic, psychological
    alert_level = Column(String(20))  # low, medium, high
    alert_message = Column(Text)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
