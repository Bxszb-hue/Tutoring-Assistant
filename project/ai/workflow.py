#!/usr/bin/env python3
"""
辅导员学生管理智能体系统工作流
根据用户类型路由到不同的智能体
"""
from langgraph.graph import StateGraph, END
from .state import UserState
from ai.student_qa_agent import student_qa_agent_node
from ai.counselor_qa_agent import counselor_qa_agent_node

def supervisor_node(state: UserState) -> UserState:
    """
    调度中枢节点
    
    根据用户类型（学生/辅导员）路由到对应的智能体
    """
    # 检查是否有用户消息需要处理
    if state.conversation_history:
        last_message = state.conversation_history[-1]
        if last_message['role'] == 'user':
            # 检查是否已经处理过这个用户消息
            if state.context.get("last_user_message") == last_message['content']:
                state.current_intent = "finished"
                return state
            
            state.context["last_user_message"] = last_message['content']
            
            # 根据用户类型确定路由
            user_type = state.user_type
            
            if user_type == "student":
                # 学生用户路由到学生智能体
                state.current_intent = "student_qa"
            elif user_type == "counselor":
                # 辅导员用户路由到辅导员智能体
                state.current_intent = "counselor_qa"
            else:
                # 默认按学生处理
                state.current_intent = "student_qa"
    
    return state

def workflow_router(state: UserState) -> str:
    """
    工作流路由函数
    
    根据用户类型和当前意图路由到不同节点
    """
    intent = state.current_intent
    
    if intent == "student_qa":
        return "student_qa"
    elif intent == "counselor_qa":
        return "counselor_qa"
    elif intent == "finished":
        return END
    
    # 默认结束
    return END

def create_workflow() -> StateGraph:
    """
    创建工作流图
    
    Returns:
        StateGraph: 工作流图
    """
    # 创建状态图
    graph = StateGraph(UserState)
    
    # 添加节点
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("student_qa", student_qa_agent_node)
    graph.add_node("counselor_qa", counselor_qa_agent_node)
    
    # 设置入口
    graph.set_entry_point("supervisor")
    
    # 添加边
    graph.add_conditional_edges(
        "supervisor",
        workflow_router,
        {
            "student_qa": "student_qa",
            "counselor_qa": "counselor_qa",
            END: END
        }
    )
    
    # 子智能体执行完后结束
    graph.add_edge("student_qa", END)
    graph.add_edge("counselor_qa", END)
    
    # 编译并返回
    return graph.compile()
