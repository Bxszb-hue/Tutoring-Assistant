#!/usr/bin/env python3
"""
导员端智能体工作流
使用LangGraph编排导员端的多个智能体
"""
from typing import Dict, Any, Optional, List
from langgraph.graph import StateGraph, END
from ai.state import UserState
from ai.counselor_qa_agent import CounselorQAAgent

class AcademicWarningAgent:
    """学业预警智能体"""
    
    def __init__(self):
        self.knowledge_base = None
    
    def detect_warning(self, state: UserState) -> Dict[str, Any]:
        """
        检测学业预警
        
        Args:
            state: 用户状态
            
        Returns:
            Dict[str, Any]: 预警信息
        """
        warning_info = {
            "warning_students": [
                {"name": "张伟", "id": "2021001", "warning_type": "学业预警", "level": "中度", "reason": "连续两门课程挂科"},
                {"name": "李明", "id": "2021002", "warning_type": "学业预警", "level": "轻度", "reason": "多门课程成绩下滑"},
                {"name": "王芳", "id": "2021003", "warning_type": "心理预警", "level": "中度", "reason": "近期情绪波动较大"}
            ],
            "total_count": 3,
            "academic_count": 2,
            "psychological_count": 1
        }
        
        return warning_info
    
    def generate_report(self, warning_info: Dict[str, Any]) -> str:
        """
        生成预警报告
        
        Args:
            warning_info: 预警信息
            
        Returns:
            str: 预警报告
        """
        report = f"学业预警报告\n\n"
        report += f"预警总人数：{warning_info['total_count']}人\n"
        report += f"- 学业预警：{warning_info['academic_count']}人\n"
        report += f"- 心理预警：{warning_info['psychological_count']}人\n\n"
        report += "预警学生列表：\n"
        
        for student in warning_info['warning_students']:
            report += f"【{student['name']}】（学号：{student['id']}）\n"
            report += f"  - 预警类型：{student['warning_type']}\n"
            report += f"  - 预警等级：{student['level']}\n"
            report += f"  - 预警原因：{student['reason']}\n\n"
        
        report += "建议措施：\n"
        report += "1. 及时与预警学生沟通，了解具体情况\n"
        report += "2. 针对学业预警学生，制定个性化帮扶计划\n"
        report += "3. 针对心理预警学生，建议预约心理咨询\n"
        report += "4. 定期跟踪预警学生的状态变化"
        
        return report

class ReportGenerationAgent:
    """报表生成智能体"""
    
    def __init__(self):
        pass
    
    def generate_report(self, query: str) -> str:
        """
        根据自然语言查询生成报表
        
        Args:
            query: 用户查询
            
        Returns:
            str: 报表内容
        """
        query_lower = query.lower()
        
        if "考勤" in query_lower:
            return self.generate_attendance_report()
        elif "成绩" in query_lower:
            return self.generate_grade_report()
        elif "预警" in query_lower:
            return self.generate_warning_report()
        elif "事务" in query_lower:
            return self.generate_transaction_report()
        else:
            return self.generate_summary_report()
    
    def generate_attendance_report(self) -> str:
        """生成考勤统计报表"""
        report = "学生考勤统计报表\n\n"
        report += "统计周期：2024年9月\n\n"
        report += "班级考勤概况：\n"
        report += "┌──────────┬────────────┬────────┬─────────┐\n"
        report += "│ 班级名称 │ 应到人数 │ 实到 │ 出勤率 │\n"
        report += "├──────────┼────────────┼────────┼─────────┤\n"
        report += "│ 计科2101 │    35     │  34   │  97.1%  │\n"
        report += "│ 计科2102 │    32     │  31   │  96.9%  │\n"
        report += "│ 计科2103 │    30     │  28   │  93.3%  │\n"
        report += "└──────────┴────────────┴────────┴─────────┘\n\n"
        report += "考勤异常学生：\n"
        report += "1. 张三（计科2103）- 旷课2次\n"
        report += "2. 李四（计科2102）- 迟到3次\n\n"
        report += "整体出勤率：95.8%\n"
        report += "备注：整体出勤情况良好，建议关注考勤异常学生"
        
        return report
    
    def generate_grade_report(self) -> str:
        """生成成绩统计报表"""
        report = "学生成绩统计报表\n\n"
        report += "统计周期：2024年秋季学期\n\n"
        report += "成绩分布：\n"
        report += "┌─────────────┬────────┬───────┐\n"
        report += "│   成绩区间   │ 人数  │ 占比  │\n"
        report += "├─────────────┼────────┼───────┤\n"
        report += "│   90-100    │  15   │ 15%   │\n"
        report += "│   80-89     │  30   │ 30%   │\n"
        report += "│   70-79     │  25   │ 25%   │\n"
        report += "│   60-69     │  20   │ 20%   │\n"
        report += "│    <60      │  10   │ 10%   │\n"
        report += "└─────────────┴────────┴───────┘\n\n"
        report += "平均绩点：3.25\n"
        report += "挂科率：10%\n\n"
        report += "学业预警建议：\n"
        report += "1. 关注挂科学生，提供学业辅导\n"
        report += "2. 组织学习经验分享会\n"
        report += "3. 建立一对一帮扶机制"
        
        return report
    
    def generate_warning_report(self) -> str:
        """生成预警统计报表"""
        report = "学生预警统计报表\n\n"
        report += "统计周期：2024年9月\n\n"
        report += "预警类型分布：\n"
        report += "┌─────────────┬────────┬───────┐\n"
        report += "│   预警类型   │ 数量  │ 占比  │\n"
        report += "├─────────────┼────────┼───────┤\n"
        report += "│   学业预警   │  12   │ 48%   │\n"
        report += "│   心理预警   │   8   │ 32%   │\n"
        report += "│   日常预警   │   5   │ 20%   │\n"
        report += "└─────────────┴────────┴───────┘\n\n"
        report += "预警等级分布：\n"
        report += "- 轻度预警：15人（60%）\n"
        report += "- 中度预警：7人（28%）\n"
        report += "- 重度预警：3人（12%）\n\n"
        report += "预警处理情况：\n"
        report += "- 已处理：18人（72%）\n"
        report += "- 待处理：7人（28%）\n\n"
        report += "建议：加快待处理预警的跟进速度，关注重度预警学生"
        
        return report
    
    def generate_transaction_report(self) -> str:
        """生成事务办理统计报表"""
        report = "学生事务办理统计报表\n\n"
        report += "统计周期：2024年9月\n\n"
        report += "事务类型统计：\n"
        report += "┌─────────────┬────────┬─────────┐\n"
        report += "│   事务类型   │ 数量  │ 完成率  │\n"
        report += "├─────────────┼────────┼─────────┤\n"
        report += "│    请假     │  45   │  100%   │\n"
        report += "│   开具证明   │  28   │   96%   │\n"
        report += "│  补办证件   │  12   │  100%   │\n"
        report += "│   其他事务   │   8   │   88%   │\n"
        report += "└─────────────┴────────┴─────────┘\n\n"
        report += "事务办理平均时长：2.1天\n"
        report += "满意度：95%\n\n"
        report += "建议：继续保持高效的事务处理效率"
        
        return report
    
    def generate_summary_report(self) -> str:
        """生成综合统计报表"""
        report = "辅导员工作综合统计报表\n\n"
        report += "统计周期：2024年9月\n\n"
        report += "【学生管理】\n"
        report += "- 负责学生数：100人\n"
        report += "- 谈心谈话：35人次\n"
        report += "- 家访/家校沟通：8次\n\n"
        report += "【预警管理】\n"
        report += "- 预警学生：25人\n"
        report += "- 已处理：18人\n"
        report += "- 待处理：7人\n\n"
        report += "【事务办理】\n"
        report += "- 处理事务：93件\n"
        report += "- 平均办理时长：2.1天\n"
        report += "- 满意度：95%\n\n"
        report += "【活动组织】\n"
        report += "- 主题班会：4场\n"
        report += "- 班级活动：2场\n"
        report += "- 参与人次：200+\n\n"
        report += "月度总结：本月工作进展顺利，各项指标良好。建议关注预警学生的跟进情况，确保及时处理。"
        
        return report

class NotificationAgent:
    """通知分发智能体"""
    
    def __init__(self):
        pass
    
    def create_notification(self, title: str, content: str, target_groups: List[str] = None) -> Dict[str, Any]:
        """
        创建通知
        
        Args:
            title: 通知标题
            content: 通知内容
            target_groups: 目标群体
            
        Returns:
            Dict[str, Any]: 通知发送结果
        """
        if not target_groups:
            target_groups = ["全体学生"]
        
        result = {
            "success": True,
            "message": "通知发送成功",
            "title": title,
            "target_groups": target_groups,
            "estimated_recipients": len(target_groups) * 50,
            "send_time": "2024-09-15 10:00:00"
        }
        
        return result
    
    def get_notification_form(self) -> str:
        """
        获取通知发布表单
        
        Returns:
            str: 表单描述
        """
        form = "通知发布表单\n\n"
        form += "【基本信息】\n"
        form += "▢ 通知标题：________________________\n\n"
        form += "【目标群体】（可多选）\n"
        form += "▢ 全体学生\n"
        form += "▢ 特定年级：□ 大一 □ 大二 □ 大三 □ 大四\n"
        form += "▢ 特定班级：________________________\n"
        form += "▢ 特定学生：________________________\n\n"
        form += "【通知类型】\n"
        form += "▢ 普通通知 ▢ 重要通知 ▢ 紧急通知\n\n"
        form += "【通知内容】\n"
        form += "____________________________________\n"
        form += "____________________________________\n"
        form += "____________________________________\n\n"
        form += "【附件】\n"
        form += "□ 上传附件\n\n"
        form += "【发送时间】\n"
        form += "▢ 立即发送 ▢ 定时发送：____年____月____日 ____:____\n\n"
        form += "【操作】\n"
        form += "[预览] [保存草稿] [发送通知]"
        
        return form

class CounselorWorkflow:
    """导员端智能体工作流"""
    
    def __init__(self):
        self.qa_agent = CounselorQAAgent()
        self.warning_agent = AcademicWarningAgent()
        self.report_agent = ReportGenerationAgent()
        self.notification_agent = NotificationAgent()
    
    def detect_intent(self, query: str) -> str:
        """
        检测导员的提问意图
        
        Args:
            query: 用户查询
            
        Returns:
            str: 意图类型
        """
        query_lower = query.lower()
        
        # 优先级：报表 > 通知 > 预警 > 问答
        # 因为"生成预警报表"应该优先识别为报表生成，而不是预警
        
        # 检测报表生成意图（最高优先级）
        if any(keyword in query_lower for keyword in ["生成报表", "统计报表", "报表生成", "工作报告生成"]):
            return "report_generation"
        
        # 检测通知分发意图
        if any(keyword in query_lower for keyword in ["发布通知", "发送通知", "通知学生"]):
            return "notification"
        
        # 检测预警查询意图
        if any(keyword in query_lower for keyword in ["查看预警", "预警学生", "预警名单", "预警处理", "预警统计"]):
            return "academic_warning"
        
        # 检测统计/报表意图（通用）
        if any(keyword in query_lower for keyword in ["报表", "统计", "报告", "数据"]):
            return "report_generation"
        
        # 检测通知意图（通用）
        if any(keyword in query_lower for keyword in ["通知", "公告"]):
            return "notification"
        
        # 检测预警意图（通用）
        if any(keyword in query_lower for keyword in ["预警", "学业预警", "心理预警"]):
            return "academic_warning"
        
        return "qa"
    
    def run(self, state: UserState) -> UserState:
        """
        运行导员端工作流
        
        Args:
            state: 用户状态
            
        Returns:
            UserState: 更新后的状态
        """
        last_message = state.get_last_message()
        if not last_message or last_message.get("role") != "user":
            return state
        
        query = last_message.get("content", "")
        intent = self.detect_intent(query)
        
        if intent == "academic_warning":
            # 调用学业预警智能体
            warning_info = self.warning_agent.detect_warning(state)
            response = self.warning_agent.generate_report(warning_info)
            agent_name = "academic_warning_agent"
            
        elif intent == "report_generation":
            # 调用报表生成智能体
            response = self.report_agent.generate_report(query)
            agent_name = "report_generation_agent"
            
        elif intent == "notification":
            # 调用通知分发智能体
            response = self.notification_agent.get_notification_form()
            agent_name = "notification_agent"
            
        else:
            # 调用导员问答智能体
            response = self.qa_agent.generate_answer(query)
            agent_name = "counselor_qa_agent"
        
        # 添加回复消息
        state.add_message(
            "assistant",
            response,
            agent_name
        )
        
        # 更新状态
        state.current_intent = intent
        state.current_task = "completed"
        state.update_task_progress("completed", 100.0, "completed")
        
        return state


def create_counselor_workflow():
    """创建导员端工作流"""
    workflow = CounselorWorkflow()
    return workflow
