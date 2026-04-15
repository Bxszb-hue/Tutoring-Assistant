from langgraph.graph import StateGraph, END
from .state import UserState
import re
from datetime import datetime

# 定义节点函数
def supervisor_node(state: UserState) -> UserState:
    """调度中枢节点
    
    负责分析用户输入，识别意图，并将任务分配给合适的智能体
    """
    # 检查是否需要人工介入
    if state.context.get("need_human_intervention", False):
        state.current_intent = "human"
        return state
    
    # 分析用户输入，识别意图
    if state.conversation_history:
        last_message = state.conversation_history[-1]
        if last_message['role'] == 'user':
            # 增强的意图识别逻辑
            content = last_message['content'].lower()
            
            # 意图置信度计算
            intent_confidence = {}
            
            # 事务办理意图
            transaction_patterns = [
                r'请假', r'补证', r'查询', r'办理', r'申请', r'注册', r'缴费',
                r'宿舍', r'学生证', r'证明', r'手续', r'流程'
            ]
            transaction_matches = sum(1 for pattern in transaction_patterns if re.search(pattern, content))
            if transaction_matches > 0:
                intent_confidence['transaction'] = transaction_matches / len(transaction_patterns)
            
            # 学业预警意图
            academic_patterns = [
                r'成绩', r'挂科', r'预警', r'学业', r'考试', r'重修',
                r'学分', r'绩点', r'毕业', r'课程'
            ]
            academic_matches = sum(1 for pattern in academic_patterns if re.search(pattern, content))
            if academic_matches > 0:
                intent_confidence['academic_alert'] = academic_matches / len(academic_patterns)
            
            # 心理关怀意图
            psychological_patterns = [
                r'心理', r'情绪', r'树洞', r'困扰', r'压力', r'焦虑',
                r'抑郁', r'失眠', r'烦恼', r'心情'
            ]
            psychological_matches = sum(1 for pattern in psychological_patterns if re.search(pattern, content))
            if psychological_matches > 0:
                intent_confidence['psychological'] = psychological_matches / len(psychological_patterns)
            
            # 报表生成意图
            report_patterns = [
                r'报表', r'统计', r'数据', r'分析', r'汇总', r'图表',
                r'考勤', r'签到', r'汇总', r'导出'
            ]
            report_matches = sum(1 for pattern in report_patterns if re.search(pattern, content))
            if report_matches > 0:
                intent_confidence['report'] = report_matches / len(report_patterns)
            
            # 通知分发意图
            notification_patterns = [
                r'通知', r'推送', r'消息', r'公告', r'发布', r'提醒'
            ]
            notification_matches = sum(1 for pattern in notification_patterns if re.search(pattern, content))
            if notification_matches > 0:
                intent_confidence['notification'] = notification_matches / len(notification_patterns)
            
            # 工单调度意图
            ticket_patterns = [
                r'工单', r'报修', r'问题', r'故障', r'维修', r'投诉',
                r'建议', r'反馈'
            ]
            ticket_matches = sum(1 for pattern in ticket_patterns if re.search(pattern, content))
            if ticket_matches > 0:
                intent_confidence['ticket'] = ticket_matches / len(ticket_patterns)
            
            # 人工介入意图（优先级最高）
            human_patterns = [
                r'人工', r'客服', r'老师', r'辅导员', r'转接', r'真人'
            ]
            if any(re.search(pattern, content) for pattern in human_patterns):
                state.current_intent = 'human'
                state.context['intent_confidence'] = 1.0
            
            # 根据置信度选择意图
            elif intent_confidence:
                # 选择置信度最高的意图
                best_intent = max(intent_confidence, key=intent_confidence.get)
                best_confidence = intent_confidence[best_intent]
                
                # 只有当置信度超过阈值时才使用该意图
                if best_confidence >= 0.3:
                    state.current_intent = best_intent
                    state.context['intent_confidence'] = best_confidence
                else:
                    # 置信度太低，使用默认问答意图
                    state.current_intent = 'qa'
                    state.context['intent_confidence'] = 0.5
            
            # 默认问答意图
            else:
                state.current_intent = 'qa'
                state.context['intent_confidence'] = 0.5
            
            # 上下文感知的意图识别
            # 如果前一个任务尚未完成，继续使用相同的意图
            if state.current_task and state.task_progress.get(state.current_task, {}).get('status') == 'processing':
                # 保持当前意图，继续处理未完成的任务
                pass
    return state

def qa_agent_node(state: UserState) -> UserState:
    """问答智能体节点
    
    处理学生高频事务咨询，调用知识库回答问题，解决不了的转人工
    """
    # 获取用户问题
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问有什么可以帮助您的？"
    else:
        question = last_message['content']
        
        # 简单的问答逻辑
        if '奖学金' in question:
            response = "申请奖学金需要满足以下条件：1. 学习成绩优秀，GPA达到3.0以上；2. 无违纪记录；3. 积极参与社会实践活动。具体申请流程可以在学校官网查看，或到辅导员办公室咨询。"
        elif '宿舍' in question:
            response = "宿舍相关问题请联系宿管中心，电话：12345678。如需调换宿舍，请提交书面申请给辅导员审批。"
        elif '请假' in question:
            response = "请假需要在系统中提交申请，填写请假原因和时间，经辅导员审批后生效。病假需要提供医院证明。"
        elif '就业' in question:
            response = "就业相关信息可以关注学校就业指导中心网站，或参加每周的就业宣讲会。如有具体问题，可以预约就业指导老师进行咨询。"
        else:
            response = "您好，我是智能问答助手，请问有什么可以帮助您的？如果您有具体问题，可以详细描述，我会尽力为您解答。"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "qa_agent")
    return state

def transaction_agent_node(state: UserState) -> UserState:
    """事务办理智能体节点
    
    对接教务、后勤等业务系统，完成请假、补证、查询等操作
    """
    # 获取用户请求
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问您需要办理什么业务？"
    else:
        request = last_message['content']
        
        # 处理不同类型的事务
        if '请假' in request:
            response = "请提供以下信息：请假类型（病假/事假/其他）、请假开始时间、请假结束时间、请假原因。我将帮您提交请假申请。"
            state.add_pending_action("leave_application", {"status": "pending"})
        elif '补证' in request:
            response = "请提供您的学号和需要补办的证件类型（学生证/校园卡/其他），我将帮您提交补证申请。"
            state.add_pending_action("certificate_application", {"status": "pending"})
        elif '查询' in request:
            if '成绩' in request:
                response = "请提供您的学号，我将帮您查询最近的成绩。"
                state.add_pending_action("grade_query", {"status": "pending"})
            elif '课表' in request:
                response = "请提供您的学号和学期，我将帮您查询课程表。"
                state.add_pending_action("timetable_query", {"status": "pending"})
            else:
                response = "请问您需要查询什么信息？"
        else:
            response = "您好，我是事务办理助手，请问您需要办理什么业务？"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "transaction_agent")
    return state

def academic_alert_agent_node(state: UserState) -> UserState:
    """学业预警智能体节点
    
    监测学业数据，生成预警报告并推送辅导员
    """
    # 模拟学业预警分析
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问您需要了解什么学业相关信息？"
    else:
        request = last_message['content']
        
        if '成绩' in request:
            # 模拟成绩查询结果
            response = "您最近的成绩如下：高等数学：85分，大学英语：78分，计算机基础：92分。您的平均绩点为3.2，处于班级中等水平。"
        elif '挂科' in request or '预警' in request:
            # 模拟预警信息
            response = "根据您的学业数据，您目前有一门课程（大学物理）成绩未达标，可能需要补考。建议您及时与任课老师沟通，制定学习计划。"
            state.add_notification("academic_alert", "您有一门课程成绩未达标，需要关注", "high")
        elif '学分' in request:
            # 模拟学分查询
            response = "您当前已修学分：45分，还需修满60分才能毕业。建议您合理安排后续学期的课程。"
        else:
            response = "您好，我是学业预警助手，请问您需要了解什么学业相关信息？"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "academic_alert_agent")
    return state

def psychological_agent_node(state: UserState) -> UserState:
    """心理关怀智能体节点
    
    运营树洞聊天功能，进行初步心理风险评估
    """
    # 模拟心理关怀对话
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，这里是心理关怀树洞，您可以在这里分享您的心情和困扰，我会认真倾听并尽力帮助您。"
    else:
        message = last_message['content']
        
        # 简单的心理风险评估
        risk_keywords = ['压力', '焦虑', '抑郁', '失眠', '自杀', '绝望', '无助']
        risk_level = 0
        for keyword in risk_keywords:
            if keyword in message:
                risk_level += 1
        
        if risk_level >= 2:
            response = "我注意到您可能正在经历一些困难，建议您及时寻求专业心理辅导。学校心理咨询中心的预约电话是：12345678，他们会为您提供专业的帮助。"
            state.add_notification("psychological_alert", "用户可能存在心理风险，需要关注", "high")
        else:
            response = "谢谢您的分享。我能理解您的感受，这种情况是很常见的。建议您尝试一些放松的活动，如运动、听音乐或与朋友交流。如果您需要进一步的帮助，随时可以告诉我。"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "psychological_agent")
    return state

def report_agent_node(state: UserState) -> UserState:
    """报表生成智能体节点
    
    响应自然语言查询，自动生成各类统计报表
    """
    # 模拟报表生成
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问您需要生成什么类型的报表？"
    else:
        request = last_message['content']
        
        if '考勤' in request:
            response = "已生成班级考勤报表，包含本月出勤情况、迟到早退统计等信息。您可以在系统中下载查看详细数据。"
            state.add_pending_action("generate_attendance_report", {"status": "completed"})
        elif '成绩' in request and '统计' in request:
            response = "已生成班级成绩统计报表，包含平均分、及格率、优秀率等数据。您可以在系统中下载查看详细数据。"
            state.add_pending_action("generate_grade_report", {"status": "completed"})
        elif '活动' in request and '统计' in request:
            response = "已生成班级活动参与统计报表，包含各项活动的参与人数、出勤率等信息。您可以在系统中下载查看详细数据。"
            state.add_pending_action("generate_activity_report", {"status": "completed"})
        else:
            response = "您好，我是报表生成助手，请问您需要生成什么类型的报表？"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "report_agent")
    return state

def notification_agent_node(state: UserState) -> UserState:
    """通知分发智能体节点
    
    智能筛选推送对象，多渠道发布通知
    """
    # 模拟通知分发
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问您需要发布什么通知？"
    else:
        request = last_message['content']
        
        if '考试' in request:
            response = "已发布考试通知，将通过短信、邮件和系统消息推送给所有学生。通知内容：\"期末考试将于下周开始，请同学们做好复习准备。\""
            state.add_notification("system", "考试通知已发布", "medium")
        elif '会议' in request:
            response = "已发布会议通知，将通过系统消息推送给所有辅导员。通知内容：\"明天下午3点在行政楼301会议室召开辅导员工作会议，请准时参加。\""
            state.add_notification("system", "会议通知已发布", "medium")
        elif '活动' in request:
            response = "已发布活动通知，将通过系统消息和微信公众号推送给所有学生。通知内容：\"本周末将举办校园文化节，欢迎同学们积极参与。\""
            state.add_notification("system", "活动通知已发布", "medium")
        else:
            response = "您好，我是通知分发助手，请问您需要发布什么通知？"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "notification_agent")
    return state

def ticket_agent_node(state: UserState) -> UserState:
    """工单调度智能体节点
    
    识别问题类型并自动分发给对应职能部门
    """
    # 模拟工单调度
    last_message = state.get_last_message()
    if not last_message or last_message['role'] != 'user':
        response = "您好，请问您需要提交什么问题？"
    else:
        request = last_message['content']
        
        if '宿舍' in request and ('漏水' in request or '维修' in request):
            response = "已生成宿舍维修工单，工单编号：WX20240411001，已分配给后勤维修部门，预计24小时内处理。"
            state.add_pending_action("create_maintenance_ticket", {"ticket_id": "WX20240411001", "status": "pending"})
        elif '网络' in request and ('故障' in request or '断网' in request):
            response = "已生成网络故障工单，工单编号：WL20240411001，已分配给网络中心，预计48小时内处理。"
            state.add_pending_action("create_network_ticket", {"ticket_id": "WL20240411001", "status": "pending"})
        elif '投诉' in request or '建议' in request:
            response = "已生成投诉建议工单，工单编号：TS20240411001，已分配给相关部门，我们会尽快处理并给您回复。"
            state.add_pending_action("create_complaint_ticket", {"ticket_id": "TS20240411001", "status": "pending"})
        else:
            response = "您好，我是工单调度助手，请问您需要提交什么问题？"
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "ticket_agent")
    return state

def human_in_the_loop_node(state: UserState) -> UserState:
    """人机协同节点（HITL）
    
    处理需要人工介入的情况，包括：
    1. 用户明确要求人工介入
    2. 智能体无法处理的问题
    3. 高风险情况（如心理危机）
    4. 复杂的事务处理
    """
    # 获取用户的最后一条消息
    last_message = state.get_last_message()
    user_input = last_message['content'] if last_message and last_message['role'] == 'user' else ""
    
    # 分析人工介入的原因
    intervention_reason = state.context.get("intervention_reason", "user_request")
    
    # 根据介入原因生成不同的响应
    if intervention_reason == "psychological_crisis":
        response = "您好，我注意到您可能正在经历一些困难，已经将您的情况转交给专业的心理辅导员，他们会尽快与您联系。如果情况紧急，请拨打心理危机干预热线：400-161-9995。"
        # 创建紧急工单
        ticket_id = f"PSY{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state.add_pending_action("create_psychological_ticket", {
            "ticket_id": ticket_id,
            "status": "urgent",
            "reason": "心理危机干预"
        })
        # 添加高优先级通知
        state.add_notification("system", f"紧急心理危机工单 #{ticket_id} 需要处理", "high")
    
    elif intervention_reason == "complex_transaction":
        response = "您好，您的请求涉及复杂的事务处理，已经将您的情况转交给辅导员老师，他们会尽快与您联系处理。"
        # 创建事务工单
        ticket_id = f"TRX{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state.add_pending_action("create_transaction_ticket", {
            "ticket_id": ticket_id,
            "status": "pending",
            "reason": "复杂事务处理",
            "details": user_input
        })
        # 添加中优先级通知
        state.add_notification("system", f"事务处理工单 #{ticket_id} 需要处理", "medium")
    
    elif intervention_reason == "system_error":
        response = "您好，系统暂时无法处理您的请求，已经将问题转交给技术人员，辅导员老师会尽快与您联系。"
        # 创建系统错误工单
        ticket_id = f"SYS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state.add_pending_action("create_system_ticket", {
            "ticket_id": ticket_id,
            "status": "pending",
            "reason": "系统错误",
            "details": state.context.get("error_message", "未知错误")
        })
        # 添加中优先级通知
        state.add_notification("system", f"系统错误工单 #{ticket_id} 需要处理", "medium")
    
    else:  # user_request
        response = "您好，我已经将您的问题转交给人工客服，辅导员老师会尽快与您联系。您也可以直接拨打辅导员办公室电话：12345678进行咨询。"
        # 创建普通工单
        ticket_id = f"GEN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        state.add_pending_action("create_general_ticket", {
            "ticket_id": ticket_id,
            "status": "pending",
            "reason": "用户请求人工介入",
            "details": user_input
        })
        # 添加普通优先级通知
        state.add_notification("system", f"普通工单 #{ticket_id} 需要处理", "normal")
    
    # 添加回答到对话历史
    state.add_message("assistant", response, "human_in_the_loop")
    
    # 记录人工介入的信息
    state.context["human_intervention"] = {
        "ticket_id": ticket_id,
        "reason": intervention_reason,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }
    
    # 清除人工介入标志
    if "need_human_intervention" in state.context:
        del state.context["need_human_intervention"]
    if "intervention_reason" in state.context:
        del state.context["intervention_reason"]
    
    return state

# 定义图结构
def create_workflow():
    workflow = StateGraph(UserState)
    
    # 添加节点
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("qa_agent", qa_agent_node)
    workflow.add_node("transaction_agent", transaction_agent_node)
    workflow.add_node("academic_alert_agent", academic_alert_agent_node)
    workflow.add_node("psychological_agent", psychological_agent_node)
    workflow.add_node("report_agent", report_agent_node)
    workflow.add_node("notification_agent", notification_agent_node)
    workflow.add_node("ticket_agent", ticket_agent_node)
    workflow.add_node("human_in_the_loop", human_in_the_loop_node)
    
    # 定义边
    workflow.set_entry_point("supervisor")

    # 从监督者到各智能体的条件边（包括人工介入）
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: {
            "human": "human",
            "qa": "qa",
            "transaction": "transaction",
            "academic_alert": "academic_alert",
            "psychological": "psychological",
            "report": "report",
            "notification": "notification",
            "ticket": "ticket"
        }.get(x.current_intent or "", "continue"),
        {
            "human": "human_in_the_loop",
            "qa": "qa_agent",
            "transaction": "transaction_agent",
            "academic_alert": "academic_alert_agent",
            "psychological": "psychological_agent",
            "report": "report_agent",
            "notification": "notification_agent",
            "ticket": "ticket_agent",
            "continue": "supervisor"
        }
    )
    
    # 从各智能体回到监督者的边
    for agent in ["qa_agent", "transaction_agent", "academic_alert_agent", 
                  "psychological_agent", "report_agent", 
                  "notification_agent", "ticket_agent"]:
        workflow.add_edge(agent, "supervisor")

    # 人工介入后回到监督者
    workflow.add_edge("human_in_the_loop", "supervisor")
    
    # 编译工作流
    return workflow.compile()