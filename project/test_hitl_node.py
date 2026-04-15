from ai.state import UserState
from ai.workflow import human_in_the_loop_node

# 测试HITL人机协同节点
def test_hitl_node():
    print("=== 测试HITL人机协同节点 ===")
    
    # 测试用例1: 用户请求人工介入
    print("\n1. 测试用户请求人工介入:")
    test_state1 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我要找辅导员"}
        ]
    )
    result1 = human_in_the_loop_node(test_state1)
    last_message1 = result1.get_last_message()
    print(f"   用户输入: {test_state1.conversation_history[0]['content']}")
    print(f"   助手响应: {last_message1['content']}")
    print(f"   处理智能体: {last_message1['agent']}")
    print(f"   待执行操作: {result1.pending_actions}")
    print(f"   通知: {result1.notification_queue}")
    print(f"   人工介入信息: {result1.context.get('human_intervention', 'N/A')}")
    
    # 测试用例2: 心理危机情况
    print("\n2. 测试心理危机情况:")
    test_state2 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我感到绝望，不想活了"}
        ],
        context={"intervention_reason": "psychological_crisis"}
    )
    result2 = human_in_the_loop_node(test_state2)
    last_message2 = result2.get_last_message()
    print(f"   用户输入: {test_state2.conversation_history[0]['content']}")
    print(f"   助手响应: {last_message2['content']}")
    print(f"   处理智能体: {last_message2['agent']}")
    print(f"   待执行操作: {result2.pending_actions}")
    print(f"   通知: {result2.notification_queue}")
    print(f"   人工介入信息: {result2.context.get('human_intervention', 'N/A')}")
    
    # 测试用例3: 复杂事务处理
    print("\n3. 测试复杂事务处理:")
    test_state3 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我需要办理休学手续，涉及很多复杂的流程"}
        ],
        context={"intervention_reason": "complex_transaction"}
    )
    result3 = human_in_the_loop_node(test_state3)
    last_message3 = result3.get_last_message()
    print(f"   用户输入: {test_state3.conversation_history[0]['content']}")
    print(f"   助手响应: {last_message3['content']}")
    print(f"   处理智能体: {last_message3['agent']}")
    print(f"   待执行操作: {result3.pending_actions}")
    print(f"   通知: {result3.notification_queue}")
    print(f"   人工介入信息: {result3.context.get('human_intervention', 'N/A')}")
    
    # 测试用例4: 系统错误情况
    print("\n4. 测试系统错误情况:")
    test_state4 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "系统无法处理我的请求"}
        ],
        context={"intervention_reason": "system_error", "error_message": "数据库连接失败"}
    )
    result4 = human_in_the_loop_node(test_state4)
    last_message4 = result4.get_last_message()
    print(f"   用户输入: {test_state4.conversation_history[0]['content']}")
    print(f"   助手响应: {last_message4['content']}")
    print(f"   处理智能体: {last_message4['agent']}")
    print(f"   待执行操作: {result4.pending_actions}")
    print(f"   通知: {result4.notification_queue}")
    print(f"   人工介入信息: {result4.context.get('human_intervention', 'N/A')}")
    
    # 测试用例5: 清除人工介入标志
    print("\n5. 测试清除人工介入标志:")
    test_state5 = UserState(
        user_id="test_user_001",
        user_type="student",
        conversation_history=[
            {"role": "user", "content": "我要找辅导员"}
        ],
        context={"need_human_intervention": True, "intervention_reason": "user_request"}
    )
    result5 = human_in_the_loop_node(test_state5)
    print(f"   原始人工介入标志: {test_state5.context.get('need_human_intervention')}")
    print(f"   处理后人工介入标志: {result5.context.get('need_human_intervention', '已清除')}")
    print(f"   原始介入原因: {test_state5.context.get('intervention_reason')}")
    print(f"   处理后介入原因: {result5.context.get('intervention_reason', '已清除')}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_hitl_node()
