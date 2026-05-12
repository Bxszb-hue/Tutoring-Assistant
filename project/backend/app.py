from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
import sys
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目路径到sys.path（放在所有导入之前）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 尝试导入必要的模块
try:
    from ai.state import UserState
    from ai.counselor_workflow import create_counselor_workflow
    from ai.student_workflow import create_student_workflow
    from backend.database import get_db, engine, Base
    from backend.knowledge_base_api import router as kb_router
    logger.info("Successfully imported all modules")
except Exception as e:
    logger.error(f"Error importing modules: {str(e)}")
    raise

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

# 注册知识库路由
app.include_router(kb_router)

# 初始化工作流
try:
    counselor_workflow = create_counselor_workflow()
    student_workflow = create_student_workflow()
    logger.info("Successfully initialized workflows")
except Exception as e:
    logger.error(f"Error initializing workflows: {str(e)}")
    raise

class MessageRequest(BaseModel):
    user_id: str
    user_type: str
    content: str

class MessageResponse(BaseModel):
    response: str
    agent: str

class ChatMessageRequest(BaseModel):
    session_id: str
    sender_id: str
    sender_name: str
    sender_role: str
    content: str

class ChatMessageResponse(BaseModel):
    id: int
    session_id: str
    sender_id: str
    sender_name: str
    sender_role: str
    content: str
    created_at: str

class ChatSessionResponse(BaseModel):
    session_id: str
    student_id: str
    student_name: str
    counselor_id: str
    counselor_name: str
    last_message: str | None
    last_message_time: str | None
    unread_count: int

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
        
        # 根据用户类型选择工作流
        if request.user_type == "counselor":
            final_state = counselor_workflow.run(state)
        else:
            final_state = student_workflow.run(state)
        
        # 获取最后一条消息
        if final_state and hasattr(final_state, 'conversation_history') and final_state.conversation_history:
            last_message = final_state.get_last_message()
            if last_message and last_message["role"] == "assistant":
                return MessageResponse(
                    response=last_message["content"],
                    agent=last_message.get("agent", "system")
                )
        
        # 如果没有回答，返回默认消息
        return MessageResponse(
            response="我暂时无法理解您的问题，请稍后再试。",
            agent="system"
        )
    except Exception as e:
        import traceback
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        # 捕获编码错误
        if "codec can't encode character" in str(e):
            return MessageResponse(
                response="系统暂时无法处理您的请求，请稍后再试。",
                agent="system"
            )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 测试数据库连接
        from sqlalchemy import text
        from backend.database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.post("/chat/message")
async def send_message(request: ChatMessageRequest, db: Session = Depends(get_db)):
    """发送聊天消息"""
    try:
        from backend.models import ChatMessage, ChatSession
        from sqlalchemy import func
        
        # 创建消息记录
        new_message = ChatMessage(
            session_id=request.session_id,
            sender_id=request.sender_id,
            sender_name=request.sender_name,
            sender_role=request.sender_role,
            content=request.content,
            created_at=func.now()
        )
        db.add(new_message)
        
        # 更新会话信息
        session = db.query(ChatSession).filter(ChatSession.session_id == request.session_id).first()
        if session:
            session.last_message = request.content
            session.last_message_time = func.now()
            # 如果是学生发送的消息，增加辅导员端的未读计数
            if request.sender_role == "student":
                session.unread_count = (session.unread_count or 0) + 1
        
        db.commit()
        
        return {"status": "success", "message": "消息发送成功"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/sessions/{user_id}")
async def get_sessions(user_id: str, user_type: str, db: Session = Depends(get_db)):
    """获取用户的聊天会话列表"""
    try:
        from backend.models import ChatSession
        
        if user_type == "counselor":
            sessions = db.query(ChatSession).filter(
                ChatSession.counselor_id == user_id
            ).order_by(ChatSession.last_message_time.desc()).all()
        else:
            sessions = db.query(ChatSession).filter(
                ChatSession.student_id == user_id
            ).all()
        
        result = []
        for session in sessions:
            result.append({
                "session_id": session.session_id,
                "student_id": session.student_id,
                "student_name": session.student_name,
                "counselor_id": session.counselor_id,
                "counselor_name": session.counselor_name,
                "last_message": session.last_message,
                "last_message_time": session.last_message_time.isoformat() if session.last_message_time else None,
                "unread_count": session.unread_count or 0
            })
        
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/messages/{session_id}")
async def get_messages(session_id: str, db: Session = Depends(get_db)):
    """获取会话的消息列表"""
    try:
        from backend.models import ChatMessage, ChatSession
        
        messages = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at).all()
        
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "session_id": msg.session_id,
                "sender_id": msg.sender_id,
                "sender_name": msg.sender_name,
                "sender_role": msg.sender_role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            })
        
        # 标记已读
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if session:
            session.unread_count = 0
            db.commit()
        
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/session")
async def create_session(request: dict, db: Session = Depends(get_db)):
    """创建聊天会话"""
    try:
        from backend.models import ChatSession
        
        session_id = request.get("session_id", f"chat_{hash(request.get('student_id', '') + request.get('counselor_id', ''))}")
        
        # 检查是否已存在会话
        existing = db.query(ChatSession).filter(
            ChatSession.student_id == request.get("student_id")
        ).filter(
            ChatSession.counselor_id == request.get("counselor_id")
        ).first()
        
        if existing:
            return {"status": "success", "session_id": existing.session_id}
        
        new_session = ChatSession(
            session_id=session_id,
            student_id=request.get("student_id"),
            student_name=request.get("student_name"),
            counselor_id=request.get("counselor_id"),
            counselor_name=request.get("counselor_name"),
            unread_count=0
        )
        db.add(new_session)
        db.commit()
        
        return {"status": "success", "session_id": session_id}
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
