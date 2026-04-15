from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from datetime import datetime

class UserState(BaseModel):
    """用户状态类
    
    用于管理多智能体系统中的用户状态，包括对话历史、当前任务、上下文信息等
    """
    # 基本信息
    user_id: str
    user_type: str  # student, counselor, admin
    
    # 对话相关
    conversation_history: List[Dict[str, Any]] = []
    current_intent: Optional[str] = None
    
    # 任务相关
    current_task: Optional[str] = None
    task_progress: Dict[str, Any] = {}
    
    # 上下文信息
    context: Dict[str, Any] = {}
    
    # 操作队列
    pending_actions: List[Dict[str, Any]] = []
    
    # 通知队列
    notification_queue: List[Dict[str, Any]] = []
    
    # 时间戳
    last_updated: datetime = datetime.now()
    
    def add_message(self, role: str, content: str, agent: str = "system") -> None:
        """添加对话消息
        
        Args:
            role: 消息角色 (user, assistant)
            content: 消息内容
            agent: 处理消息的智能体
        """
        self.conversation_history.append({
            "role": role,
            "content": content,
            "agent": agent,
            "timestamp": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def update_task_progress(self, task_id: str, progress: float, status: str) -> None:
        """更新任务进度
        
        Args:
            task_id: 任务ID
            progress: 任务进度 (0-100)
            status: 任务状态 (pending, processing, completed, failed)
        """
        self.task_progress[task_id] = {
            "progress": progress,
            "status": status,
            "updated_at": datetime.now().isoformat()
        }
        self.last_updated = datetime.now()
    
    def add_notification(self, notification_type: str, message: str, priority: str = "medium") -> None:
        """添加通知
        
        Args:
            notification_type: 通知类型
            message: 通知消息
            priority: 通知优先级 (low, medium, high)
        """
        self.notification_queue.append({
            "type": notification_type,
            "message": message,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def add_pending_action(self, action_type: str, action_data: Dict[str, Any]) -> None:
        """添加待执行操作
        
        Args:
            action_type: 操作类型
            action_data: 操作数据
        """
        self.pending_actions.append({
            "type": action_type,
            "data": action_data,
            "created_at": datetime.now().isoformat()
        })
        self.last_updated = datetime.now()
    
    def clear_pending_actions(self) -> None:
        """清空待执行操作队列"""
        self.pending_actions = []
        self.last_updated = datetime.now()
    
    def clear_notifications(self) -> None:
        """清空通知队列"""
        self.notification_queue = []
        self.last_updated = datetime.now()
    
    def get_last_message(self) -> Optional[Dict[str, Any]]:
        """获取最后一条消息
        
        Returns:
            最后一条消息,如果没有消息则返回None
        """
        if self.conversation_history:
            return self.conversation_history[-1]
        return None
    
    def get_user_messages(self) -> List[Dict[str, Any]]:
        """获取用户消息
        
        Returns:
            用户消息列表
        """
        return [msg for msg in self.conversation_history if msg.get("role") == "user"]
    
    def get_assistant_messages(self) -> List[Dict[str, Any]]:
        """获取助手消息
        
        Returns:
            助手消息列表
        """
        return [msg for msg in self.conversation_history if msg.get("role") == "assistant"]
