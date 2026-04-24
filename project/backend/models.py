from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
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

class StudentInfo(Base):
    """学生详细信息表"""
    __tablename__ = "student_info"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"), unique=True)
    class_name = Column(String(50))
    major = Column(String(100))
    grade = Column(String(10))
    department = Column(String(100))
    enrollment_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Course(Base):
    """课程信息表"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String(50), unique=True, index=True)
    course_name = Column(String(200))
    course_type = Column(String(20))
    credits = Column(Integer)
    teacher = Column(String(100))
    department = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Enrollment(Base):
    """选课记录表"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"))
    course_id = Column(String(50), ForeignKey("courses.course_id"))
    semester = Column(String(20))
    status = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Grade(Base):
    """成绩表"""
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"))
    course_id = Column(String(50), ForeignKey("courses.course_id"))
    score = Column(Float)
    grade_point = Column(Float)
    semester = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    """事务申请表"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"))
    transaction_type = Column(String(50))
    transaction_data = Column(Text)
    status = Column(String(20))
    approver = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

class Leave(Base):
    """请假申请表"""
    __tablename__ = "leaves"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("users.user_id"))
    leave_type = Column(String(20))  # 事假, 病假, 公假
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    reason = Column(Text)
    status = Column(String(20))  # pending, approved, rejected
    approver = Column(String(50))
    approver_comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
