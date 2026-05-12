#!/usr/bin/env python3
"""
辅导员端问答智能体
专门服务于辅导员用户的智能助手
"""
from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.knowledge_base_simple import SimpleKnowledgeBaseTool, SimpleDocument
from ai.llm_client import llm_complete, llm_chat

class CounselorQAAgent:
    """辅导员端智能体"""
    
    def __init__(self, llm_provider: str = "deepseek"):
        """初始化辅导员端智能体"""
        self.knowledge_base = SimpleKnowledgeBaseTool()
        try:
            self.knowledge_base.load()
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
        self.llm_provider = llm_provider
    
    def detect_intent(self, query: str) -> str:
        """
        检测辅导员用户的提问意图
        
        Args:
            query: 用户提问
            
        Returns:
            str: 意图类型
        """
        query_lower = query.lower()
        
        # 学生管理类意图
        student_management_keywords = [
            "学生管理", "班级管理", "评优", "评奖", "奖学金评定",
            "处分", "违纪", "考勤", "请假审批", "困难生认定",
            "心理预警", "学业预警", "学生档案", "就业推荐",
            "学生画像", "综合素质测评", "荣誉称号"
        ]
        if any(keyword in query_lower for keyword in student_management_keywords):
            return "student_management"
        
        # 政策咨询类意图
        policy_keywords = [
            "政策", "规定", "文件", "通知", "办法", "条例",
            "制度", "标准", "要求", "程序", "流程",
            "法律法规", "校纪校规", "管理规定"
        ]
        if any(keyword in query_lower for keyword in policy_keywords):
            return "policy"
        
        # 工作助手类意图
        work_keywords = [
            "工作总结", "工作计划", "报告", "材料", "发言稿",
            "谈心谈话", "班会", "家长会", "评语", "鉴定",
            "案例分析", "工作方案", "活动策划"
        ]
        if any(keyword in query_lower for keyword in work_keywords):
            return "work_assistant"
        
        # 数据统计类意图
        data_keywords = [
            "统计", "数据", "报表", "分析", "汇总",
            "考勤统计", "成绩统计", "违纪统计", "预警统计"
        ]
        if any(keyword in query_lower for keyword in data_keywords):
            return "data_analysis"
        
        # 默认是知识库问答
        return "qa"
    
    def retrieve_relevant_documents(self, query: str, k: int = 4) -> List[SimpleDocument]:
        """
        检索相关文档（针对辅导员，优先返回政策文件类）
        
        Args:
            query: 用户查询
            k: 返回文档数量
            
        Returns:
            List[SimpleDocument]: 相关文档列表
        """
        try:
            # 检索所有相关文档
            all_docs = self.knowledge_base.search(query, k=k+2)
            
            # 优先返回规章制度和办事流程类文档
            prioritized = []
            other = []
            
            for doc in all_docs:
                category = doc.metadata.get('category', '')
                if category in ['regulation', 'process']:
                    prioritized.append(doc)
                else:
                    other.append(doc)
            
            return (prioritized + other)[:k]
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
    
    def build_prompt(self, query: str, documents: List[SimpleDocument]) -> str:
        """
        构建辅导员端提示词
        
        Args:
            query: 用户查询
            documents: 相关文档列表
            
        Returns:
            str: 构建好的提示词
        """
        context = ""
        for i, doc in enumerate(documents):
            context += f"[{i+1}] {doc.page_content}\n"
            category = doc.metadata.get('category', '')
            source = doc.metadata.get('source', '未知')
            if category:
                context += f"类型: {category}, 来源: {source}\n\n"
        
        prompt = f"""你是一个专业、高效、懂业务的辅导员智能助手，专门为高校辅导员提供工作支持。

你的职责是：
1. 解答辅导员关于学生工作、学校政策、办事流程等方面的专业问题
2. 协助辅导员完成各种文案工作（总结、计划、报告、发言稿等）
3. 提供准确的政策文件解读和工作指导
4. 以专业、严谨、高效的风格回答问题

知识库信息：
{context}

辅导员问题：{query}

请基于以上信息，为辅导员提供帮助。回答要：
- 专业、准确、条理清晰
- 语言简洁明了，适合工作场景
- 给出可操作性的建议
- 如果涉及政策文件，请引用具体出处
- 如果信息不足，给出可进一步获取信息的渠道
- 对于文案工作，可以提供结构框架或示例
- 回答要简洁明了，不要使用星号、井号等符号进行格式化
"""
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
        生成辅导员端回答

        Args:
            query: 用户查询

        Returns:
            str: 生成的回答
        """
        # 检测意图
        intent = self.detect_intent(query)
        
        # 检索相关文档
        documents = self.retrieve_relevant_documents(query, k=4)
        
        # 根据意图构建不同的提示词
        if intent == "work_assistant":
            # 工作助手类，不需要太多知识库信息
            prompt = f"""你是一个专业的辅导员工作助手，帮助辅导员完成各种文案工作。

辅导员需要：{query}

请提供专业、实用的内容，包括结构框架、关键要点和示例内容。回答要符合辅导员工作场景，语言正式规范。
回答要简洁明了，不要使用星号、井号等符号进行格式化。"""
        else:
            # 其他类型，使用标准提示词
            prompt = self.build_prompt(query, documents)
        
        # 调用大模型生成回答
        try:
            answer = llm_complete(prompt, provider=self.llm_provider, temperature=0.7)
            return self.clean_answer(answer)
        except Exception as e:
            print(f"Error with LLM: {e}")
            # 降级方案
            if documents:
                answer = f"您好！根据相关规定，关于'{query}'的信息如下：\n\n"
                for doc in documents[:3]:
                    title = doc.metadata.get('title', doc.metadata.get('process_name', ''))
                    if title:
                        answer += f"【{title}】\n"
                    content = doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content
                    answer += f"{content}\n\n"
                answer += "以上信息供参考，具体请以学校最新文件为准。"
                return answer
            else:
                # 没有相关文档时的通用回答
                general_prompt = f"""你是一个专业的辅导员工作助手。

辅导员问题：{query}

请根据辅导员工作的专业知识，提供专业、实用的回答。
回答要简洁明了，不要使用星号、井号等符号进行格式化。"""
                try:
                    answer = llm_complete(general_prompt, provider=self.llm_provider, temperature=0.7)
                    return self.clean_answer(answer)
                except:
                    return f"您好！关于'{query}'这个问题，我暂时无法提供准确信息。建议您：\n\n1. 查阅学校相关文件或通知\n2. 咨询学校相关职能部门\n3. 与同事交流经验\n\n如有其他问题，欢迎继续提问！"


def counselor_qa_agent_node(state: UserState) -> UserState:
    """
    辅导员端问答智能体节点
    
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
    agent = CounselorQAAgent()
    
    # 检测意图
    intent = agent.detect_intent(query)
    
    # 生成回答
    answer = agent.generate_answer(query)
    
    # 添加回复消息
    state.add_message(
        "assistant",
        answer,
        "counselor_qa_agent"
    )
    
    # 更新状态
    state.current_intent = intent
    state.current_task = "answer_counselor_question"
    state.update_task_progress("answer_counselor_question", 100.0, "completed")
    
    return state
