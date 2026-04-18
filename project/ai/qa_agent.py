from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.knowledge_base import KnowledgeBaseTool
from langchain.schema import Document
import time

class QAAgent:
    def __init__(self):
        """
        初始化问答智能体
        """
        self.knowledge_base = KnowledgeBaseTool()
        # 尝试加载已有的向量存储
        self.knowledge_base.load()
        
    def retrieve_relevant_documents(self, query: str, k: int = 3) -> List[Document]:
        """
        检索相关文档
        
        Args:
            query: 用户查询
            k: 返回的文档数量
        
        Returns:
            List[Document]: 相关文档列表
        """
        return self.knowledge_base.search(query, k=k)
    
    def build_prompt(self, query: str, documents: List[Document]) -> str:
        """
        构建提示词
        
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
        
        prompt = f"""
你是一个专业的辅导员学生管理智能助手，需要根据提供的知识库信息回答用户的问题。

知识库信息：
{context}

用户问题：{query}

请基于知识库信息，用自然、友好的语言回答用户问题。如果知识库中没有相关信息，请明确告知用户。
回答要求：
1. 准确反映知识库中的信息
2. 语言简洁明了
3. 保持专业、友好的语气
4. 引用相关来源（如果有）
"""
        
        return prompt
    
    def generate_answer(self, query: str) -> str:
        """
        生成回答（RAG增强）
        
        Args:
            query: 用户查询
        
        Returns:
            str: 生成的回答
        """
        # 检索相关文档
        documents = self.retrieve_relevant_documents(query, k=3)
        
        if not documents:
            return "抱歉，我暂时没有关于这个问题的信息。"
        
        # 构建提示词
        prompt = self.build_prompt(query, documents)
        
        # 这里可以集成大语言模型进行生成
        # 由于是示例，我们使用规则生成回答
        answer = self.generate_answer_with_rules(prompt, documents)
        
        return answer
    
    def generate_answer_with_rules(self, prompt: str, documents: List[Document]) -> str:
        """
        使用规则生成回答
        
        Args:
            prompt: 提示词
            documents: 相关文档列表
        
        Returns:
            str: 生成的回答
        """
        # 提取用户问题
        lines = prompt.split('\n')
        user_query = ""
        for line in lines:
            if line.startswith("用户问题："):
                user_query = line[6:].strip()
                break
        
        # 构建回答
        answer = f"根据我的知识库，关于'{user_query}'的信息如下：\n\n"
        
        for i, doc in enumerate(documents):
            answer += f"[{i+1}] {doc.page_content}\n"
            if doc.metadata.get('source'):
                answer += f"来源: {doc.metadata['source']}\n"
            answer += "\n"
        
        answer += "希望这些信息对您有帮助！"
        
        return answer
    
    def check_need_human_intervention(self, query: str) -> bool:
        """
        检查是否需要人工干预
        
        Args:
            query: 用户查询
        
        Returns:
            bool: 是否需要人工干预
        """
        # 检索相关文档
        results = self.knowledge_base.search_with_score(query, k=1)
        
        if not results:
            return True
        
        # 检查相似度分数
        doc, score = results[0]
        if score > 0.5:  # 相似度阈值
            return True
        
        # 检查是否是复杂问题
        complex_keywords = ["如何申请", "流程", "步骤", "政策", "法规"]
        if any(keyword in query for keyword in complex_keywords):
            # 对于复杂问题，即使有相关信息也可能需要人工干预
            if len(results) < 2:
                return True
        
        return False

# 问答节点函数
def qa_agent_node(state: UserState) -> Dict[str, Any]:
    """
    问答智能体节点函数
    
    Args:
        state: 用户状态
    
    Returns:
        Dict[str, Any]: 更新后的状态
    """
    # 创建问答智能体实例
    qa_agent = QAAgent()
    
    # 获取用户最后一条消息
    last_message = state.get_last_message()
    if not last_message or last_message.get("role") != "user":
        # 如果没有用户消息，返回原状态
        return {"state": state}
    
    # 提取用户查询
    query = last_message.get("content", "")
    
    # 检查是否需要人工干预
    need_human = qa_agent.check_need_human_intervention(query)
    
    if need_human:
        # 需要人工干预，添加待处理操作
        state.add_pending_action(
            "human_intervention",
            {
                "query": query,
                "reason": "知识库中没有相关信息"
            }
        )
        
        # 添加助手消息
        state.add_message(
            "assistant",
            "您的问题需要人工处理，我已经将您的请求转交给相关人员。",
            "qa_agent"
        )
    else:
        # 生成回答
        answer = qa_agent.generate_answer(query)
        
        # 添加助手消息
        state.add_message(
            "assistant",
            answer,
            "qa_agent"
        )
    
    # 更新状态
    state.current_intent = "qa"
    state.current_task = "answer_question"
    state.update_task_progress("answer_question", 100.0, "completed")
    
    return {"state": state}

# 测试代码
if __name__ == "__main__":
    # 创建测试状态
    test_state = UserState(
        user_id="test_user",
        user_type="student"
    )
    
    # 添加用户消息
    test_state.add_message("user", "辅导员的职责是什么？")
    
    # 测试问答节点
    result = qa_agent_node(test_state)
    updated_state = result["state"]
    
    # 打印结果
    print("测试结果：")
    for msg in updated_state.conversation_history:
        print(f"{msg['role']}: {msg['content']}")
    
    # 测试需要人工干预的情况
    test_state2 = UserState(
        user_id="test_user2",
        user_type="student"
    )
    
    # 添加一个知识库中没有的问题
    test_state2.add_message("user", "如何申请出国留学？")
    
    # 测试问答节点
    result2 = qa_agent_node(test_state2)
    updated_state2 = result2["state"]
    
    # 打印结果
    print("\n测试人工干预：")
    for msg in updated_state2.conversation_history:
        print(f"{msg['role']}: {msg['content']}")
    
    # 打印待处理操作
    print("\n待处理操作：")
    for action in updated_state2.pending_actions:
        print(f"{action['type']}: {action['data']}")
