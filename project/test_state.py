from ai.state import UserState

# 测试State状态类
def test_user_state():
    print("=== 测试UserState状态类 ===")
    
    # 创建初始状态
    state = UserState(
        user_id="test_user_001",
        user_type="student"
    )
    
    print("1. 初始状态测试:")
    print(f"   用户ID: {state.user_id}")
    print(f"   用户类型: {state.user_type}")
    print(f"   对话历史: {state.conversation_history}")
    print(f"   当前意图: {state.current_intent}")
    print(f"   任务进度: {state.task_progress}")
    print(f"   上下文: {state.context}")
    print(f"   待执行操作: {state.pending_actions}")
    print(f"   通知队列: {state.notification_queue}")
    
    # 测试添加消息
    print("\n2. 添加消息测试:")
    state.add_message("user", "我想申请请假")
    state.add_message("assistant", "好的，我来帮您处理请假申请", "transaction_agent")
    print(f"   对话历史长度: {len(state.conversation_history)}")
    for i, msg in enumerate(state.conversation_history):
        print(f"   消息{i+1}: {msg['role']} - {msg['content']} (by {msg['agent']})")
    
    # 测试获取最后一条消息
    print("\n3. 获取最后一条消息测试:")
    last_msg = state.get_last_message()
    print(f"   最后一条消息: {last_msg['role']} - {last_msg['content']}")
    
    # 测试获取用户消息和助手消息
    print("\n4. 消息过滤测试:")
    user_msgs = state.get_user_messages()
    assistant_msgs = state.get_assistant_messages()
    print(f"   用户消息数量: {len(user_msgs)}")
    print(f"   助手消息数量: {len(assistant_msgs)}")
    
    # 测试更新任务进度
    print("\n5. 更新任务进度测试:")
    state.update_task_progress("leave_application_001", 50.0, "processing")
    print(f"   任务进度: {state.task_progress}")
    
    # 测试添加通知
    print("\n6. 添加通知测试:")
    state.add_notification("system", "您的请假申请正在处理中")
    state.add_notification("alert", "您有一条新的学业预警", "high")
    print(f"   通知数量: {len(state.notification_queue)}")
    for i, notification in enumerate(state.notification_queue):
        print(f"   通知{i+1}: [{notification['priority']}] {notification['type']} - {notification['message']}")
    
    # 测试添加待执行操作
    print("\n7. 添加待执行操作测试:")
    state.add_pending_action("send_email", {"to": "student@example.com", "subject": "请假申请确认"})
    print(f"   待执行操作数量: {len(state.pending_actions)}")
    for i, action in enumerate(state.pending_actions):
        print(f"   操作{i+1}: {action['type']} - {action['data']}")
    
    # 测试清空队列
    print("\n8. 清空队列测试:")
    state.clear_pending_actions()
    state.clear_notifications()
    print(f"   待执行操作数量: {len(state.pending_actions)}")
    print(f"   通知数量: {len(state.notification_queue)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_user_state()
