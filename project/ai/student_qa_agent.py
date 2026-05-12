#!/usr/bin/env python3
"""
学生端问答智能体
专门服务于学生用户的问答智能体
"""
from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.knowledge_base_simple import SimpleKnowledgeBaseTool, SimpleDocument
from ai.llm_client import llm_complete, llm_chat
from ai.transaction_agent import transaction_agent_node
from ai.psychological_agent import psychological_agent_node

class StudentQAAgent:
    """学生端问答智能体"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        """初始化学生端问答智能体"""
        self.knowledge_base = SimpleKnowledgeBaseTool()
        try:
            self.knowledge_base.load()
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
        self.llm_provider = llm_provider
    
    def detect_intent(self, query: str) -> str:
        """
        检测学生用户的提问意图
        
        Args:
            query: 用户提问
            
        Returns:
            str: 意图类型
        """
        query_lower = query.lower()
        
        # 事务办理类意图
        transaction_keywords = [
            "请假", "请假流程", "补办", "学生证", "成绩查询",
            "在读证明", "一卡通", "挂失", "宿舍报修", "困难认定",
            "事务办理", "办事流程", "怎么申请", "如何办理", "申请",
            "补办证件", "证明开具", "成绩", "课表", "查询"
        ]
        if any(keyword in query_lower for keyword in transaction_keywords):
            return "transaction"
        
        # 心理关怀类意图
        psychological_keywords = [
            "心情不好", "压力大", "焦虑", "抑郁", "难过",
            "想不开", "心理咨询", "心情", "情绪", "孤独",
            "不开心", "很难受", "烦恼", "迷茫", "困惑",
            "失眠", "压力", "累", "疲惫", "无助",
            "痛苦", "伤心", "绝望", "害怕", "恐惧"
        ]
        if any(keyword in query_lower for keyword in psychological_keywords):
            return "psychological"
        
        # 知识库问答类意图（默认）
        return "qa"
    
    def retrieve_relevant_documents(self, query: str, k: int = 3) -> List[SimpleDocument]:
        """
        检索相关文档（针对学生）
        
        Args:
            query: 用户查询
            k: 返回文档数量
            
        Returns:
            List[SimpleDocument]: 相关文档列表
        """
        try:
            return self.knowledge_base.search(query, k=k)
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def build_prompt(self, query: str, documents: List[SimpleDocument]) -> str:
        """
        构建学生端提示词
        
        Args:
            query: 用户查询
            documents: 相关文档列表
            
        Returns:
            str: 构建好的提示词
        """
        context = ""
        for i, doc in enumerate(documents):
            context += f"[{i+1}] {doc.page_content}\n"
            context += f"来源: {doc.metadata.get('source', '未知')}\n\n"
        
        prompt = ("你是一个专业、温暖、耐心的辅导员学生管理智能助手，专门为在校大学生提供服务。\n\n"
                "你的职责是：\n"
                "1. 解答学生关于学校规章制度、办事流程、奖助学金等方面的问题\n"
                "2. 提供准确的学校相关信息\n"
                "3. 用友好、易懂的语言回答问题\n"
                "4. 当问题超出知识库范围时，坦诚告知并提供建议\n\n"
                "知识库信息：\n"
                f"{context}\n\n"
                "学生问题："
                f"{query}\n\n"
                "请基于以上信息，给学生提供帮助。回答要：\n"
                "- 语言亲切、友好、有温度\n"
                "- 内容准确、条理清晰\n"
                "- 适当给出可操作性的建议\n"
                "- 如果信息不够明确，可以询问更多细节\n"
                "- 不要编造信息，不确定的请如实告知\n"
                "- 回答要简洁明了，不要使用星号、井号等符号进行格式化")
        return prompt
    
    def clean_answer(self, answer: str) -> str:
        """
        清理回答中的不美观符号

        Args:
            answer: 大模型生成的回答

        Returns:
            str: 清理后的回答
        """
        # 移除Markdown格式的符号
        answer = answer.replace('**', '')
        answer = answer.replace('##', '')
        answer = answer.replace('#', '')
        answer = answer.replace('---', '')
        answer = answer.replace('__', '')
        
        # 移除多余的空行
        while '\n\n\n' in answer:
            answer = answer.replace('\n\n\n', '\n\n')
        
        return answer

    def generate_answer(self, query: str) -> str:
        """
        生成学生端回答

        Args:
            query: 用户查询

        Returns:
            str: 生成的回答
        """
        # 检索相关文档
        documents = self.retrieve_relevant_documents(query, k=3)

        if not documents:
            # 如果没有相关文档，使用大模型的通用知识
            fallback_prompt = ("你是一个专业的辅导员学生管理智能助手，为学生解答问题。\n\n"
                           "学生问题："
                           f"{query}\n\n"
                           "请用友好、专业的语言回答学生的问题。如果涉及学校具体政策，请说明这是一般性建议，建议学生咨询辅导员或相关部门获取准确信息。\n"
                           "回答要简洁明了，不要使用星号、井号等符号进行格式化。")
            try:
                answer = llm_complete(fallback_prompt, provider=self.llm_provider, temperature=0.7)
                return self.clean_answer(answer)
            except Exception as e:
                print(f"Error with LLM: {e}")
                return "同学你好！关于这个问题我暂时无法提供准确的信息。建议你可以：\n\n1. 咨询辅导员\n2. 查询学校官方网站\n3. 到相关部门办事大厅询问\n\n如果有其他问题，欢迎继续问我！"

        # 构建提示词
        prompt = self.build_prompt(query, documents)

        # 调用大模型生成回答
        try:
            answer = llm_complete(prompt, provider=self.llm_provider, temperature=0.7)
            return self.clean_answer(answer)
        except Exception as e:
            print(f"Error with LLM: {e}")
            # 降级方案
            answer = f"同学你好！根据学校的相关规定，关于'{query}'的信息如下：\n\n"
            for doc in documents[:2]:
                title = doc.metadata.get('title', doc.metadata.get('process_name', doc.metadata.get('question', '')))
                if title:
                    answer += f"【{title}】\n"
                content = doc.page_content[:400] + "..." if len(doc.page_content) > 400 else doc.page_content
                answer += f"{content}\n\n"
            answer += "希望这些信息对你有帮助！如需更详细的说明，可以咨询辅导员或相关部门。"
            return answer
    
    def check_need_human(self, query: str) -> bool:
        """
        检查是否需要转人工处理
        
        Args:
            query: 用户查询
            
        Returns:
            bool: 是否需要转人工
        """
        high_risk_keywords = [
            "自杀", "自残", "不想活", "结束生命", "暴力",
            "伤人", "打架", "严重违纪", "退学", "开除",
            "杀人", "伤害", "威胁", "死亡", "轻生"
        ]
        
        for keyword in high_risk_keywords:
            if keyword in query.lower():
                return True
        
        return False


def student_qa_agent_node(state: UserState) -> UserState:
    """
    学生端问答智能体节点
    
    Args:
        state: 用户状态
        
    Returns:
        UserState: 更新后的状态
    """
    # 获取最后一条用户消息
    last_message = state.get_last_message()
    if not last_message or last_message.get("role") != "user":
        return state
    
    query = last_message.get("content", "")
    
    # 创建智能体实例
    agent = StudentQAAgent()
    
    # 检测意图
    intent = agent.detect_intent(query)
    
    # 根据意图路由到不同的子智能体
    if intent == "transaction":
        return transaction_agent_node(state)
    elif intent == "psychological":
        return psychological_agent_node(state)
    else:
        # 知识库问答
        answer = agent.generate_answer(query)
        
        # 检查是否需要转人工
        need_human = agent.check_need_human(query)
        if need_human:
            state.add_pending_action(
                "human_attention_needed",
                {
                    "query": query,
                    "reason": "high_risk_detected"
                }
            )
            answer += "\n\n注意：你的情况比较重要，我已通知辅导员，辅导员会尽快与你联系。"
        
        # 添加回复消息
        state.add_message(
            "assistant",
            answer,
            "student_qa_agent"
        )
        
        # 更新状态
        state.current_intent = "qa"
        state.current_task = "answer_question"
        state.update_task_progress("answer_question", 100.0, "completed")
    
    return state
