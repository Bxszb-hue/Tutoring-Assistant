from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尝试导入必要的模块
try:
    from ai.state import UserState
    from ai.workflow import create_workflow
    from .database import get_db, engine, Base
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