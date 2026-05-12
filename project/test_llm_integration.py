#!/usr/bin/env python3
"""
测试大模型连接
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ai.llm_client import LLMFactory, llm_complete, llm_chat
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_llm_connection():
    """测试大模型连接"""
    print("=" * 60)
    print("测试大模型连接")
    print("=" * 60)

    # 测试不同的模型提供商
    providers = ["deepseek", "qwen", "openai"]

    for provider in providers:
        print(f"\n测试 {provider}...")
        try:
            # 测试文本生成
            prompt = "请用一句话介绍自己"
            response = llm_complete(prompt, provider=provider, temperature=0.7)
            print(f"[OK] {provider} 文本生成成功: {response[:100]}...")

            # 测试对话
            messages = [
                {"role": "system", "content": "你是一个友好的AI助手"},
                {"role": "user", "content": "你好，请问你叫什么名字？"}
            ]
            chat_response = llm_chat(messages, provider=provider, temperature=0.7)
            print(f"[OK] {provider} 对话成功: {chat_response[:100]}...")

        except Exception as e:
            print(f"[FAIL] {provider} 测试失败: {e}")

    print("\n" + "=" * 60)
    print("大模型连接测试完成")
    print("=" * 60)

def test_qa_agent():
    """测试问答智能体"""
    print("\n" + "=" * 60)
    print("测试问答智能体")
    print("=" * 60)

    try:
        from ai.qa_agent import QAAgent

        agent = QAAgent()

        # 测试问答
        question = "奖学金如何申请？"
        print(f"\n问题: {question}")

        answer = agent.generate_answer(question)
        print(f"回答: {answer[:200]}...")

        print("\n[OK] 问答智能体测试成功")

    except Exception as e:
        print(f"\n[FAIL] 问答智能体测试失败: {e}")

def test_transaction_agent():
    """测试事务办理智能体"""
    print("\n" + "=" * 60)
    print("测试事务办理智能体")
    print("=" * 60)

    try:
        from ai.transaction_agent import TransactionAgent

        agent = TransactionAgent()

        # 测试事务检测
        query = "我想请假一周"
        trans_type = agent.detect_transaction_type(query)
        print(f"\n查询: {query}")
        print(f"检测到事务类型: {trans_type}")

        # 生成响应
        if trans_type:
            response = agent.generate_response(query, trans_type)
            print(f"响应: {response[:200]}...")

        print("\n[OK] 事务办理智能体测试成功")

    except Exception as e:
        print(f"\n[FAIL] 事务办理智能体测试失败: {e}")

def test_psychological_agent():
    """测试心理关怀智能体"""
    print("\n" + "=" * 60)
    print("测试心理关怀智能体")
    print("=" * 60)

    try:
        from ai.psychological_agent import PsychologicalAgent

        agent = PsychologicalAgent()

        # 测试风险评估
        messages = [
            "最近学习压力有点大",
            "感觉好焦虑，睡不着觉",
            "活着真没意思"
        ]

        for msg in messages:
            risk_level = agent.assess_risk_level(msg)
            print(f"\n消息: {msg}")
            print(f"风险等级: {risk_level}")

        # 生成响应
        response = agent.generate_response("最近感觉压力很大", "moderate")
        print(f"\n响应: {response[:200]}...")

        print("\n[OK] 心理关怀智能体测试成功")

    except Exception as e:
        print(f"\n[FAIL] 心理关怀智能体测试失败: {e}")

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("辅导员学生管理智能体系统 - 大模型集成测试")
    print("=" * 60)

    # 测试大模型连接
    test_llm_connection()

    # 测试各智能体
    test_qa_agent()
    test_transaction_agent()
    test_psychological_agent()

    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)
    print("\n提示：要启用大模型功能，请在 .env 文件中配置 API 密钥")
    print("支持的模型：DeepSeek (推荐)、通义千问、OpenAI")
    print("=" * 60)

if __name__ == "__main__":
    main()
