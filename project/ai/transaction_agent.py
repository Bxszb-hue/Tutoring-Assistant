#!/usr/bin/env python3
"""
事务办理智能体
负责处理学生事务办理的相关请求，如请假、补办证件等
"""
from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.knowledge_base_simple import SimpleKnowledgeBaseTool
from ai.llm_client import llm_complete, llm_chat

class TransactionAgent:
    """事务办理智能体"""

    # 支持的事务类型
    TRANSACTION_TYPES = {
        "请假": "leave_request",
        "补办学生证": "student_card_reissue",
        "成绩查询": "grade_query",
        "在读证明": "study_certificate",
        "一卡通挂失": "card_report_loss",
        "宿舍报修": "dorm_repair",
        "家庭经济困难认定": "financial_assistance",
        "奖学金": "scholarship_application"
    }

    def __init__(self, llm_provider: str = None):
        """初始化事务办理智能体"""
        self.knowledge_base = SimpleKnowledgeBaseTool()
        try:
            self.knowledge_base.load()
        except:
            pass
        self.llm_provider = llm_provider

    def detect_transaction_type(self, query: str) -> Optional[str]:
        """
        检测用户请求的事务类型

        Args:
            query: 用户查询

        Returns:
            str: 事务类型，如果没有匹配则返回None
        """
        # 首先尝试完全匹配
        for keyword, trans_type in self.TRANSACTION_TYPES.items():
            if keyword in query:
                return trans_type
        
        # 尝试部分匹配，处理用户表述不同的情况
        query_lower = query.lower()
        
        # 请假
        if any(keyword in query_lower for keyword in ["请假", "申请请假", "请假流程"]):
            return "leave_request"
        
        # 补办学生证
        if any(keyword in query_lower for keyword in ["学生证", "补办学生证", "学生证丢了"]):
            return "student_card_reissue"
        
        # 成绩查询
        if any(keyword in query_lower for keyword in ["成绩", "成绩查询", "查成绩"]):
            return "grade_query"
        
        # 在读证明
        if any(keyword in query_lower for keyword in ["在读证明", "开具证明"]):
            return "study_certificate"
        
        # 一卡通挂失
        if any(keyword in query_lower for keyword in ["一卡通", "挂失", "校园卡"]):
            return "card_report_loss"
        
        # 宿舍报修
        if any(keyword in query_lower for keyword in ["宿舍", "报修", "维修"]):
            return "dorm_repair"
        
        # 家庭经济困难认定
        if any(keyword in query_lower for keyword in ["困难", "经济困难", "贫困认定"]):
            return "financial_assistance"
        
        # 奖学金
        if any(keyword in query_lower for keyword in ["奖学金", "申请奖学金"]):
            return "scholarship_application"

        return None

    def get_process_info(self, trans_type: str) -> Optional[str]:
        """
        获取事务办理流程信息

        Args:
            trans_type: 事务类型

        Returns:
            str: 流程信息
        """
        # 根据事务类型查找对应的流程文档
        process_name_map = {
            "leave_request": "学生请假办理流程",
            "student_card_reissue": "学生证补办流程",
            "grade_query": "成绩查询与复核流程",
            "study_certificate": "在读证明开具流程",
            "card_report_loss": "一卡通挂失与补办流程",
            "dorm_repair": "学生宿舍报修流程",
            "financial_assistance": "家庭经济困难学生认定流程",
            "scholarship_application": "奖学金"
        }

        process_name = process_name_map.get(trans_type)
        if process_name:
            results = self.knowledge_base.search(process_name, k=1)
            if results:
                return results[0].page_content

        return None

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

    def generate_response(self, query: str, trans_type: str) -> str:
        """
        生成事务办理的响应

        Args:
            query: 用户查询
            trans_type: 事务类型

        Returns:
            str: 响应内容
        """
        # 获取流程信息
        process_info = self.get_process_info(trans_type)

        if process_info:
            # 构建提示词
            prompt = f"""您是一个专业的辅导员学生管理智能助手。用户想要办理以下事务：
            事务类型：{trans_type}
            用户需求：{query}

            相关办理流程：
            {process_info}

            请用简洁、友好的语言向用户解释办理流程，并提供清晰的步骤指导。
            回答要简洁明了，不要使用星号、井号等符号进行格式化。
            """

            try:
                # 尝试使用大模型生成响应
                response = llm_complete(prompt, provider=self.llm_provider, temperature=0.7)
                return self.clean_answer(response)
            except:
                # 如果大模型调用失败，使用规则方法
                return self.generate_response_with_rules(query, trans_type, process_info)
        else:
            return "抱歉，我暂时无法获取该事务的办理流程信息，请稍后再试或直接联系相关部门。"

    def generate_response_with_rules(self, query: str, trans_type: str, process_info: str) -> str:
        """
        使用规则生成响应（降级方案）

        Args:
            query: 用户查询
            trans_type: 事务类型
            process_info: 流程信息

        Returns:
            str: 响应内容
        """
        response = f"好的，我来为您提供【{trans_type}】的相关信息：\n\n"
        response += f"{process_info}\n\n"
        response += "如果您需要更详细的指导或有其他问题，请随时告诉我。您也可以联系相关部门获取帮助。"
        return response

    def check_need_approval(self, trans_type: str) -> bool:
        """
        检查事务是否需要人工审批

        Args:
            trans_type: 事务类型

        Returns:
            bool: 是否需要审批
        """
        # 一些事务需要审批
        approval_required = [
            "leave_request",
            "study_certificate",
            "financial_assistance"
        ]
        return trans_type in approval_required


# 事务办理节点函数
def transaction_agent_node(state: UserState) -> UserState:
    """
    事务办理智能体节点函数

    Args:
        state: 用户状态

    Returns:
        UserState: 更新后的状态
    """
    # 创建事务办理智能体实例
    trans_agent = TransactionAgent()

    # 获取用户最后一条消息
    last_message = state.get_last_message()
    if not last_message or last_message.get("role") != "user":
        return state

    # 提取用户查询
    query = last_message.get("content", "")

    # 检测事务类型
    trans_type = trans_agent.detect_transaction_type(query)

    if trans_type:
        # 生成响应
        response = trans_agent.generate_response(query, trans_type)

        # 检查是否需要审批
        need_approval = trans_agent.check_need_approval(trans_type)

        if need_approval:
            # 添加待审批操作
            state.add_pending_action(
                "approval_required",
                {
                    "transaction_type": trans_type,
                    "query": query
                }
            )

            # 添加助手消息
            state.add_message(
                "assistant",
                response + "\n\n注意：该事务需要人工审批，我已经为您记录了请求。",
                "transaction_agent"
            )
        else:
            # 添加助手消息
            state.add_message(
                "assistant",
                response,
                "transaction_agent"
            )

        # 更新状态
        state.current_intent = "transaction"
        state.current_task = "process_transaction"
        state.update_task_progress("process_transaction", 100.0, "completed")

    else:
        # 无法识别事务类型，退回问答智能体
        help_text = '我暂时无法识别您的事务类型，请您更明确地描述您的需求，例如：我想请假或我想补办学生证。'
        state.add_message(
            "assistant",
            help_text,
            "transaction_agent"
        )

    return state


# 测试代码
if __name__ == "__main__":
    print("测试事务办理智能体")

    # 创建测试状态
    test_state = UserState(
        user_id="test_user",
        user_type="student"
    )

    # 测试请假申请
    test_state.add_message("user", "我想请假，请问怎么办？")
    result = transaction_agent_node(test_state)

    print("\n请假申请测试结果：")
    for msg in result.conversation_history:
        print(f"{msg['role']}: {msg['content']}")

    # 测试其他事务
    print("\n" + "="*50)

    test_state2 = UserState(
        user_id="test_user2",
        user_type="student"
    )
    test_state2.add_message("user", "学生证丢了，怎么补办？")
    result2 = transaction_agent_node(test_state2)

    print("\n补办学生证测试结果：")
    for msg in result2.conversation_history:
        print(f"{msg['role']}: {msg['content']}")
