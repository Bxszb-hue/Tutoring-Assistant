from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
import json

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尝试导入必要的模块
try:
    from ai.state import UserState
    from ai.workflow import create_workflow
    from .database import get_db, engine, Base
    from .business_integration import BusinessSystemIntegration
    logger.info("Successfully imported all modules")
except Exception as e:
    logger.error(f"Error importing modules: {str(e)}")
    raise

# 配置本地Ollama模型
try:
    from langchain_ollama import OllamaLLM
    # 初始化Ollama模型
    llm = OllamaLLM(model="qwen2.5:7b", base_url="http://localhost:11434")
    logger.info("Successfully initialized Ollama model")
except Exception as e:
    logger.error(f"Error initializing Ollama model: {str(e)}")
    llm = None

# 创建数据库表
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Successfully created database tables")
except Exception as e:
    logger.error(f"Error creating database tables: {str(e)}")
    # 继续执行，即使数据库连接失败

app = FastAPI(title="辅导员学生管理智能体系统")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化工作流
try:
    workflow = create_workflow()
    logger.info("Successfully initialized workflow")
except Exception as e:
    logger.error(f"Error initializing workflow: {str(e)}")
    raise

class MessageRequest(BaseModel):
    user_id: str
    user_type: str
    content: str

class MessageResponse(BaseModel):
    response: str
    agent: str

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """处理用户聊天请求"""
    try:
        # 初始化状态
        state = UserState(
            user_id=request.user_id,
            user_type=request.user_type,
            conversation_history=[
                {
                    "role": "user",
                    "content": request.content
                }
            ]
        )
        
        # 运行工作流
        result = workflow.invoke(state)
        
        # 处理返回的结果（可能是字典或 UserState 对象）
        if isinstance(result, dict):
            # 如果是字典，使用字典访问方式
            conversation_history = result.get('conversation_history', [])
        else:
            # 如果是 UserState 对象，使用属性访问方式
            conversation_history = result.conversation_history
        
        # 获取最后一条消息
        if conversation_history:
            last_message = conversation_history[-1]
            return MessageResponse(
                response=last_message["content"],
                agent=last_message.get("agent", "system")
            )
        else:
            raise HTTPException(status_code=400, detail="No response generated")
    except Exception as e:
        import traceback
        print(f"Error in chat endpoint: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 测试数据库连接
        from sqlalchemy import text
        from .database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# 业务系统集成API
class TransactionRequest(BaseModel):
    transaction_type: str
    transaction_data: dict

class ProcessTransactionRequest(BaseModel):
    status: str
    approver: str

@app.get("/api/student/{student_id}/info")
async def get_student_info(student_id: str, db: Session = Depends(get_db)):
    """获取学生详细信息"""
    try:
        business = BusinessSystemIntegration(db)
        info = business.get_student_info(student_id)
        if not info:
            raise HTTPException(status_code=404, detail="学生不存在")
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/courses")
async def get_courses(department: str = None, db: Session = Depends(get_db)):
    """获取课程列表"""
    try:
        business = BusinessSystemIntegration(db)
        courses = business.get_courses(department)
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/courses")
async def get_student_courses(student_id: str, semester: str = None, db: Session = Depends(get_db)):
    """获取学生已选课程"""
    try:
        business = BusinessSystemIntegration(db)
        courses = business.get_student_courses(student_id, semester)
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/grades")
async def get_student_grades(student_id: str, semester: str = None, db: Session = Depends(get_db)):
    """获取学生成绩"""
    try:
        business = BusinessSystemIntegration(db)
        grades = business.get_student_grades(student_id, semester)
        return grades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/student/{student_id}/transactions")
async def submit_transaction(student_id: str, request: TransactionRequest, db: Session = Depends(get_db)):
    """提交事务申请"""
    try:
        business = BusinessSystemIntegration(db)
        result = business.submit_transaction(student_id, request.transaction_type, request.transaction_data)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/transactions")
async def get_student_transactions(student_id: str, status: str = None, db: Session = Depends(get_db)):
    """获取学生的事务申请"""
    try:
        business = BusinessSystemIntegration(db)
        transactions = business.get_transactions(student_id, status)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transactions/{transaction_id}/process")
async def process_transaction(transaction_id: int, request: ProcessTransactionRequest, db: Session = Depends(get_db)):
    """处理事务申请"""
    try:
        business = BusinessSystemIntegration(db)
        result = business.process_transaction(transaction_id, request.status, request.approver)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/transactions")
async def get_all_transactions(status: str = None, db: Session = Depends(get_db)):
    """获取所有事务申请（用于辅导员）"""
    try:
        business = BusinessSystemIntegration(db)
        transactions = business.get_all_transactions(status)
        return transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 请假申请API
class LeaveRequest(BaseModel):
    leave_type: str
    start_date: str
    end_date: str
    reason: str

class ProcessLeaveRequest(BaseModel):
    status: str
    approver: str
    approver_comment: Optional[str] = None

@app.post("/api/student/{student_id}/leaves")
async def submit_leave(student_id: str, request: LeaveRequest, db: Session = Depends(get_db)):
    """提交请假申请"""
    try:
        from datetime import datetime
        start_date = datetime.fromisoformat(request.start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(request.end_date.replace('Z', '+00:00'))
        
        business = BusinessSystemIntegration(db)
        result = business.submit_leave(student_id, request.leave_type, start_date, end_date, request.reason)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/student/{student_id}/leaves")
async def get_student_leaves(student_id: str, status: str = None, db: Session = Depends(get_db)):
    """获取学生的请假记录"""
    try:
        business = BusinessSystemIntegration(db)
        leaves = business.get_student_leaves(student_id, status)
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leaves")
async def get_all_leaves(status: str = None, db: Session = Depends(get_db)):
    """获取所有请假申请（用于辅导员）"""
    try:
        business = BusinessSystemIntegration(db)
        leaves = business.get_all_leaves(status)
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/leaves/{leave_id}/process")
async def process_leave(leave_id: int, request: ProcessLeaveRequest, db: Session = Depends(get_db)):
    """处理请假申请"""
    try:
        business = BusinessSystemIntegration(db)
        result = business.process_leave(leave_id, request.status, request.approver, request.approver_comment)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))