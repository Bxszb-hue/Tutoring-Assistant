from ai.state import UserState
from ai.workflow import supervisor_node

# 测试调度中枢节点
def test_supervisor_node():
    print("=== 测试调度中枢节点 ===")
    
    # 测试用例1: 事务办理意图
    print("\n1. 测试事务办理意图:")
    test_state1 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我想申请请假"}
        ]
    )
    result1 = supervisor_node(test_state1)
    print(f"   用户输入: {test_state1.conversation_history[0]['content']}")
    print(f"   识别意图: {result1.current_intent}")
    print(f"   意图置信度: {result1.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例2: 学业预警意图
    print("\n2. 测试学业预警意图:")
    test_state2 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我的成绩怎么样？"}
        ]
    )
    result2 = supervisor_node(test_state2)
    print(f"   用户输入: {test_state2.conversation_history[0]['content']}")
    print(f"   识别意图: {result2.current_intent}")
    print(f"   意图置信度: {result2.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例3: 心理关怀意图
    print("\n3. 测试心理关怀意图:")
    test_state3 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我最近压力很大，感到焦虑"}
        ]
    )
    result3 = supervisor_node(test_state3)
    print(f"   用户输入: {test_state3.conversation_history[0]['content']}")
    print(f"   识别意图: {result3.current_intent}")
    print(f"   意图置信度: {result3.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例4: 报表生成意图
    print("\n4. 测试报表生成意图:")
    test_state4 = UserState(
        user_id="test_user_002",
        user_type="counselor",
        conversation_history=[
            {"role": "user", "content": "生成班级考勤报表"}
        ]
    )
    result4 = supervisor_node(test_state4)
    print(f"   用户输入: {test_state4.conversation_history[0]['content']}")
    print(f"   识别意图: {result4.current_intent}")
    print(f"   意图置信度: {result4.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例5: 通知分发意图
    print("\n5. 测试通知分发意图:")
    test_state5 = UserState(
        user_id="test_user_002",
        user_type="counselor",
        conversation_history=[
            {"role": "user", "content": "发布考试通知"}
        ]
    )
    result5 = supervisor_node(test_state5)
    print(f"   用户输入: {test_state5.conversation_history[0]['content']}")
    print(f"   识别意图: {result5.current_intent}")
    print(f"   意图置信度: {result5.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例6: 工单调度意图
    print("\n6. 测试工单调度意图:")
    test_state6 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "宿舍漏水需要维修"}
        ]
    )
    result6 = supervisor_node(test_state6)
    print(f"   用户输入: {test_state6.conversation_history[0]['content']}")
    print(f"   识别意图: {result6.current_intent}")
    print(f"   意图置信度: {result6.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例7: 人工介入意图
    print("\n7. 测试人工介入意图:")
    test_state7 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我要找辅导员"}
        ]
    )
    result7 = supervisor_node(test_state7)
    print(f"   用户输入: {test_state7.conversation_history[0]['content']}")
    print(f"   识别意图: {result7.current_intent}")
    print(f"   意图置信度: {result7.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例8: 默认问答意图
    print("\n8. 测试默认问答意图:")
    test_state8 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "你好"}
        ]
    )
    result8 = supervisor_node(test_state8)
    print(f"   用户输入: {test_state8.conversation_history[0]['content']}")
    print(f"   识别意图: {result8.current_intent}")
    print(f"   意图置信度: {result8.context.get('intent_confidence', 'N/A')}")
    
    # 测试用例9: 上下文感知（未完成任务）
    print("\n9. 测试上下文感知（未完成任务）:")
    test_state9 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我想申请请假"},
            {"role": "assistant", "content": "请提供请假类型和时间"},
            {"role": "user", "content": "病假，从明天开始，为期3天"}
        ],
        current_task="leave_application",
        task_progress={"leave_application": {"status": "processing"}}
    )
    # 先识别第一次输入的意图
    result9_1 = supervisor_node(test_state9)
    print(f"   当前任务: {result9_1.current_task}")
    print(f"   任务状态: {result9_1.task_progress.get('leave_application', {}).get('status')}")
    print(f"   识别意图: {result9_1.current_intent}")
    
    # 测试用例10: 人工介入标志
    print("\n10. 测试人工介入标志:")
    test_state10 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我想申请请假"}
        ],
        context={"need_human_intervention": True}
    )
    result10 = supervisor_node(test_state10)
    print(f"   人工介入标志: {test_state10.context.get('need_human_intervention')}")
    print(f"   识别意图: {result10.current_intent}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_supervisor_node()
