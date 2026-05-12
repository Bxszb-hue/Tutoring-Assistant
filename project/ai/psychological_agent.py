#!/usr/bin/env python3
"""
心理关怀智能体
负责处理学生心理健康相关的问题，提供心理支持和疏导
"""
from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.knowledge_base_simple import SimpleKnowledgeBaseTool
from ai.llm_client import llm_complete, llm_chat

class PsychologicalAgent:
    """心理关怀智能体"""

    # 心理风险关键词
    RISK_KEYWORDS = [
        "自杀", "自残", "绝望", "无助", "不想活", "活着没意思",
        "抑郁", "崩溃", "极度焦虑", "恐慌发作"  
    ]

    # 中度风险关键词
    MODERATE_RISK_KEYWORDS = [
        "压力", "焦虑", "失眠", "烦恼", "心情不好", "失落",
        "迷茫", "孤独", "无助感", "自我否定"
    ]

    def __init__(self, llm_provider: str = None):
        """初始化心理关怀智能体"""
        self.knowledge_base = SimpleKnowledgeBaseTool()
        try:
            self.knowledge_base.load()
        except:
            pass
        self.llm_provider = llm_provider

    def assess_risk_level(self, message: str) -> str:
        """
        评估心理风险等级

        Args:
            message: 用户消息

        Returns:
            str: 风险等级 (high, moderate, low)
        """
        message_lower = message.lower()

        # 检查高风险关键词
        for keyword in self.RISK_KEYWORDS:
            if keyword in message_lower:
                return "high"

        # 检查中度风险关键词
        for keyword in self.MODERATE_RISK_KEYWORDS:
            if keyword in message_lower:
                return "moderate"

        return "low"

    def get_relevant_guidance(self, message: str) -> List[str]:
        """
        获取相关的心理导言

        Args:
            message: 用户消息

        Returns:
            List[str]: 相关的导言内容列表
        """
        results = self.knowledge_base.search(message, k=3)

        # 过滤出心理导言类别的文档
        guidance_list = []
        for doc in results:
            if doc.metadata.get("category") == "psychological_guidance":
                guidance_list.append(doc.page_content)

        return guidance_list

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

    def generate_response(self, message: str, risk_level: str) -> str:
        """
        生成心理关怀响应

        Args:
            message: 用户消息
            risk_level: 风险等级

        Returns:
            str: 响应内容
        """
        # 获取相关的心理导言
        guidance_list = self.get_relevant_guidance(message)

        # 构建提示词
        guidance_context = "\n".join([f"- {g}" for g in guidance_list]) if guidance_list else "暂无相关导言"

        prompt = f"""您是一个温暖、专业的心理关怀助手，正在与一位学生进行对话。

学生说：{message}

风险评估等级：{risk_level}

相关的心理导言：
{guidance_context}

请根据以下要求生成回复：
1. 如果风险等级是"high"，请立即提供危机干预资源和专业帮助建议
2. 如果风险等级是"moderate"，请提供理解和支持，并给出实用的应对建议
3. 如果风险等级是"low"，请保持温暖友好的态度，给予积极正面的引导
4. 适当引用相关的心理导言内容
5. 始终保持同理心，不要给出简单的解决方案或评判
6. 如果学生表达的情绪特别强烈，优先表达理解和共情

请用温暖、真诚的语言回复。
回答要简洁明了，不要使用星号、井号等符号进行格式化。
"""

        try:
            # 尝试使用大模型生成响应
            response = llm_complete(prompt, provider=self.llm_provider, temperature=0.8)
            return self.clean_answer(response)
        except:
            # 如果大模型调用失败，使用规则方法
            return self.generate_response_with_rules(message, risk_level, guidance_list)

    def generate_response_with_rules(self, message: str, risk_level: str, guidance_list: List[str]) -> str:
        """
        使用规则生成响应（降级方案）

        Args:
            message: 用户消息
            risk_level: 风险等级
            guidance_list: 导言列表

        Returns:
            str: 响应内容
        """
        if risk_level == "high":
            response = """我听到您了，我注意到您可能正在经历非常困难的时刻。

您的感受非常重要，也值得被认真对待。我强烈建议您：

1. **立即寻求专业帮助**：
   - 拨打心理危机干预热线：400-161-9995（全国24小时）
   - 或联系学校心理咨询中心：xxx-xxxx-xxxx

2. **告诉信任的人**：请尽快联系您的家人、朋友或辅导员，告诉他们您的感受

3. **保持安全**：如果当前有自我伤害的想法，请先离开可能造成伤害的环境

记住：**您不是一个人**，有人愿意帮助您度过这个困难时刻。
"""
        elif risk_level == "moderate":
            response = """谢谢您愿意和我分享您的感受。

在学习和生活中感到压力、焦虑是很正常的，很多人都有类似的经历。"""

            if guidance_list:
                response += f"\n\n我想和您分享一些可能有帮助的建议：\n{guidance_list[0][:200]}..."

            response += """

记住：
- 您的感受是有效的
- 寻求帮助是一种勇气，不是软弱
- 您可以随时联系我，或者预约专业的心理咨询

您想更多地聊聊是什么让您感到压力吗？
"""
        else:
            response = """谢谢您分享您的想法和感受。

大学生活充满了各种挑战和机遇，感到有时迷茫或有些小困扰是很正常的。"""

            if guidance_list:
                response += f"\n\n{guidance_list[0][:200]}..."

            response += """

如果您想聊更多，或者有任何困扰想要倾诉，我都在这里倾听。
有时候，把心里的想法说出来，本身就是一种很好的疗愈方式。
"""

        return response

    def should_escalate(self, risk_level: str) -> bool:
        """
        判断是否需要升级处理（通知人工）

        Args:
            risk_level: 风险等级

        Returns:
            bool: 是否需要升级
        """
        # 高风险和中度风险都需要升级
        return risk_level in ["high", "moderate"]


# 心理关怀节点函数
def psychological_agent_node(state: UserState) -> UserState:
    """
    心理关怀智能体节点函数

    Args:
        state: 用户状态

    Returns:
        UserState: 更新后的状态
    """
    # 创建心理关怀智能体实例
    psych_agent = PsychologicalAgent()

    # 获取用户最后一条消息
    last_message = state.get_last_message()
    if not last_message or last_message.get("role") != "user":
        # 如果没有用户消息，发送欢迎消息
        welcome_msg = """欢迎来到心理关怀树洞

这里是一个安全、温暖的空间，您可以自由地分享您的想法和感受。

我会认真倾听，并尽我所能为您提供支持。如果您需要专业帮助，我也会为您提供相关资源。

今天想和我聊聊什么呢？"""
        state.add_message("assistant", welcome_msg, "psychological_agent")
        return state

    # 提取用户消息
    message = last_message.get("content", "")

    # 评估风险等级
    risk_level = psych_agent.assess_risk_level(message)

    # 生成响应
    response = psych_agent.generate_response(message, risk_level)

    # 添加助手消息
    state.add_message("assistant", response, "psychological_agent")

    # 检查是否需要升级
    if psych_agent.should_escalate(risk_level):
        # 添加通知
        state.add_notification(
            "psychological_alert",
            f"学生可能存在心理风险（等级：{risk_level}），请关注",
            "high" if risk_level == "high" else "medium"
        )

        # 如果是高风险，添加高优先级操作
        if risk_level == "high":
            state.add_pending_action(
                "psychological_intervention",
                {
                    "risk_level": risk_level,
                    "message": message,
                    "priority": "high"
                }
            )

    # 更新状态
    state.current_intent = "psychological"
    state.current_task = "psychological_support"
    state.update_task_progress("psychological_support", 100.0, "completed")

    return state


# 测试代码
if __name__ == "__main__":
    print("测试心理关怀智能体")

    # 测试正常对话
    test_state = UserState(
        user_id="test_user",
        user_type="student"
    )
    test_state.add_message("user", "最近学习压力有点大，感觉有点累")
    result = psychological_agent_node(test_state)

    print("\n正常对话测试结果：")
    for msg in result.conversation_history:
        print(f"{msg['role']}: {msg['content'][:100]}...")

    # 测试中度风险
    print("\n" + "="*50)

    test_state2 = UserState(
        user_id="test_user2",
        user_type="student"
    )
    test_state2.add_message("user", "最近总是失眠，心情很低落，对什么都提不起兴趣")
    result2 = psychological_agent_node(test_state2)

    print("\n中度风险测试结果：")
    for msg in result2.conversation_history:
        print(f"{msg['role']}: {msg['content'][:100]}...")

    # 打印通知
    print("\n通知列表：")
    for notification in result2.notification_queue:
        print(f"- {notification}")
