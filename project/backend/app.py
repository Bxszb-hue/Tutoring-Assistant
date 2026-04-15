from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from ai.state import UserState
from ai.workflow import create_workflow
from .database import get_db, engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="辅导员学生管理智能体系统")

# 初始化工作流
workflow = create_workflow()

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
        
        # 获取最后一条消息
        if result.conversation_history:
            last_message = result.conversation_history[-1]
            return MessageResponse(
                response=last_message["content"],
                agent=last_message.get("agent", "system")
            )
        else:
            raise HTTPException(status_code=400, detail="No response generated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """健康检查"""
    try:
        # 测试数据库连接
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}