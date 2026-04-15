from ai.state import UserState
from ai.workflow import create_workflow

# 测试LangGraph工作流框架
def test_workflow_framework():
    print("=== 测试LangGraph工作流框架 ===")
    
    # 创建工作流
    print("1. 初始化工作流...")
    try:
        workflow = create_workflow()
        print("   工作流初始化成功！")
    except Exception as e:
        print(f"   工作流初始化失败: {e}")
        return
    
    # 测试问答智能体
    print("\n2. 测试问答智能体:")
    test_state1 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "如何申请奖学金？"}
        ]
    )
    
    try:
        result1 = workflow.invoke(test_state1)
        last_message1 = result1.get_last_message()
        print(f"   用户: {test_state1.conversation_history[0]['content']}")
        print(f"   助手: {last_message1['content']}")
        print(f"   处理智能体: {last_message1['agent']}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试事务办理智能体
    print("\n3. 测试事务办理智能体:")
    test_state2 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我想申请请假"}
        ]
    )
    
    try:
        result2 = workflow.invoke(test_state2)
        last_message2 = result2.get_last_message()
        print(f"   用户: {test_state2.conversation_history[0]['content']}")
        print(f"   助手: {last_message2['content']}")
        print(f"   处理智能体: {last_message2['agent']}")
        print(f"   待执行操作: {result2.pending_actions}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试学业预警智能体
    print("\n4. 测试学业预警智能体:")
    test_state3 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我的成绩怎么样？"}
        ]
    )
    
    try:
        result3 = workflow.invoke(test_state3)
        last_message3 = result3.get_last_message()
        print(f"   用户: {test_state3.conversation_history[0]['content']}")
        print(f"   助手: {last_message3['content']}")
        print(f"   处理智能体: {last_message3['agent']}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试心理关怀智能体
    print("\n5. 测试心理关怀智能体:")
    test_state4 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我最近压力很大，感到焦虑"}
        ]
    )
    
    try:
        result4 = workflow.invoke(test_state4)
        last_message4 = result4.get_last_message()
        print(f"   用户: {test_state4.conversation_history[0]['content']}")
        print(f"   助手: {last_message4['content']}")
        print(f"   处理智能体: {last_message4['agent']}")
        print(f"   通知: {result4.notification_queue}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试报表生成智能体
    print("\n6. 测试报表生成智能体:")
    test_state5 = UserState(
        user_id="test_user_002",
        user_type="counselor",
        conversation_history=[
            {"role": "user", "content": "生成班级考勤报表"}
        ]
    )
    
    try:
        result5 = workflow.invoke(test_state5)
        last_message5 = result5.get_last_message()
        print(f"   用户: {test_state5.conversation_history[0]['content']}")
        print(f"   助手: {last_message5['content']}")
        print(f"   处理智能体: {last_message5['agent']}")
        print(f"   待执行操作: {result5.pending_actions}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试通知分发智能体
    print("\n7. 测试通知分发智能体:")
    test_state6 = UserState(
        user_id="test_user_002",
        user_type="counselor",
        conversation_history=[
            {"role": "user", "content": "发布考试通知"}
        ]
    )
    
    try:
        result6 = workflow.invoke(test_state6)
        last_message6 = result6.get_last_message()
        print(f"   用户: {test_state6.conversation_history[0]['content']}")
        print(f"   助手: {last_message6['content']}")
        print(f"   处理智能体: {last_message6['agent']}")
        print(f"   通知: {result6.notification_queue}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试工单调度智能体
    print("\n8. 测试工单调度智能体:")
    test_state7 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "宿舍漏水需要维修"}
        ]
    )
    
    try:
        result7 = workflow.invoke(test_state7)
        last_message7 = result7.get_last_message()
        print(f"   用户: {test_state7.conversation_history[0]['content']}")
        print(f"   助手: {last_message7['content']}")
        print(f"   处理智能体: {last_message7['agent']}")
        print(f"   待执行操作: {result7.pending_actions}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    # 测试人工介入
    print("\n9. 测试人工介入:")
    test_state8 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我要找辅导员"}
        ]
    )
    
    try:
        result8 = workflow.invoke(test_state8)
        last_message8 = result8.get_last_message()
        print(f"   用户: {test_state8.conversation_history[0]['content']}")
        print(f"   助手: {last_message8['content']}")
        print(f"   处理智能体: {last_message8['agent']}")
    except Exception as e:
        print(f"   测试失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_workflow_framework()
