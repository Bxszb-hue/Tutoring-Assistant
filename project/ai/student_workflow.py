#!/usr/bin/env python3
"""
学生端智能体工作流
使用LangGraph编排学生端的多个智能体
"""
from typing import Dict, Any, Optional, List
from ai.state import UserState
from ai.student_qa_agent import StudentQAAgent
from ai.psychological_agent import PsychologicalAgent

class LeaveApplicationAgent:
    """请假办理智能体"""
    
    def __init__(self):
        pass
    
    def create_application(self, query: str) -> Dict[str, Any]:
        """
        创建请假申请
        
        Args:
            query: 用户查询
            
        Returns:
            Dict[str, Any]: 申请信息
        """
        # 解析用户查询中的请假信息
        days = self._extract_days(query)
        reason = self._extract_reason(query)
        leave_type = self._extract_leave_type(query)
        
        application = {
            "type": leave_type,
            "days": days,
            "reason": reason,
            "start_date": "2024-09-16",
            "end_date": "2024-09-17",
            "status": "pending",
            "submitted_at": "2024-09-15 09:30:00",
            "message": "请假申请已提交，等待辅导员审批"
        }
        
        return application
    
    def _extract_days(self, query: str) -> int:
        """从查询中提取请假天数"""
        import re
        match = re.search(r'(\d+)\s*天', query)
        if match:
            return int(match.group(1))
        return 1
    
    def _extract_reason(self, query: str) -> str:
        """从查询中提取请假原因"""
        if "生病" in query or "感冒" in query or "发烧" in query:
            return "生病就医"
        elif "家里" in query or "回家" in query:
            return "家中有事"
        elif "面试" in query or "实习" in query:
            return "实习/面试"
        else:
            return "个人事务"
    
    def _extract_leave_type(self, query: str) -> str:
        """从查询中提取请假类型"""
        if "病假" in query or "生病" in query:
            return "病假"
        elif "事假" in query:
            return "事假"
        else:
            return "事假"
    
    def generate_application_form(self) -> str:
        """
        生成请假申请表单
        
        Returns:
            str: 表单描述
        """
        form = "请假申请表\n\n"
        form += "【基本信息】\n"
        form += "姓名：________________________\n"
        form += "学号：________________________\n"
        form += "班级：________________________\n\n"
        form += "【请假类型】\n"
        form += "▢ 病假 ▢ 事假 ▢ 其他________\n\n"
        form += "【请假时间】\n"
        form += "开始日期：____年____月____日\n"
        form += "结束日期：____年____月____日\n"
        form += "共计：________天\n\n"
        form += "【请假原因】\n"
        form += "____________________________________\n"
        form += "____________________________________\n\n"
        form += "【证明材料】\n"
        form += "□ 医院诊断证明（病假需提供）\n"
        form += "□ 其他证明材料\n\n"
        form += "【联系方式】\n"
        form += "手机：________________________\n"
        form += "紧急联系人：________________________\n\n"
        form += "【承诺】\n"
        form += "本人承诺以上信息属实，请假期间遵守学校相关规定。\n"
        form += "申请人签名：________________________\n"
        form += "申请日期：____年____月____日\n\n"
        form += "[提交申请] [保存草稿]"
        
        return form

class MentalHealthAssessmentAgent:
    """心理健康测评智能体"""
    
    def __init__(self):
        self.tests = {
            "depression": "抑郁自评量表(SDS)",
            "anxiety": "焦虑自评量表(SAS)",
            "stress": "压力自评量表(PSS)",
            "sleep": "睡眠质量量表(PSQI)"
        }
    
    def get_test_list(self) -> str:
        """获取测评列表"""
        result = "心理健康测评中心\n\n"
        result += "请选择您想进行的测评：\n\n"
        result += "1. 【抑郁自评量表(SDS)】\n"
        result += "   用于评估抑郁情绪程度，共20题，约5分钟完成\n\n"
        result += "2. 【焦虑自评量表(SAS)】\n"
        result += "   用于评估焦虑情绪程度，共20题，约5分钟完成\n\n"
        result += "3. 【压力自评量表(PSS)】\n"
        result += "   用于评估当前压力水平，共14题，约3分钟完成\n\n"
        result += "4. 【睡眠质量量表(PSQI)】\n"
        result += "   用于评估睡眠质量，共19题，约5分钟完成\n\n"
        result += "请输入序号选择测评，或告诉我您想了解哪一个测评。"
        
        return result
    
    def generate_test_result(self, test_type: str, answers: List[int]) -> str:
        """
        生成测评结果
        
        Args:
            test_type: 测评类型
            answers: 答案列表
            
        Returns:
            str: 测评结果
        """
        test_names = {
            "depression": "抑郁自评量表(SDS)",
            "anxiety": "焦虑自评量表(SAS)",
            "stress": "压力自评量表(PSS)",
            "sleep": "睡眠质量量表(PSQI)"
        }
        
        # 模拟测评结果
        score = sum(answers) % 100
        level = "正常" if score < 50 else "轻度" if score < 60 else "中度" if score < 70 else "重度"
        
        result = f"{test_names.get(test_type, '未知测评')}\n\n"
        result += f"测评得分：{score}分\n"
        result += f"评估等级：{level}\n\n"
        
        if level == "正常":
            result += "【评估结果】\n"
            result += "您的心理状态良好，继续保持！\n\n"
            result += "【建议】\n"
            result += "- 保持良好的生活习惯\n"
            result += "- 继续保持积极乐观的心态\n"
            result += "- 如有需要，随时可以进行心理咨询"
        else:
            result += "【评估结果】\n"
            result += f"您目前可能存在{level}的{test_type}问题。\n\n"
            result += "【建议】\n"
            result += "- 尝试自我调节，如运动、听音乐等\n"
            result += "- 与朋友或家人多沟通交流\n"
            result += "- 建议预约学校心理咨询\n"
            result += "- 如情况持续，及时寻求专业帮助"
        
        return result

class StudentWorkflow:
    """学生端智能体工作流"""
    
    def __init__(self):
        self.qa_agent = StudentQAAgent()
        self.leave_agent = LeaveApplicationAgent()
        self.psychological_agent = PsychologicalAgent()
        self.assessment_agent = MentalHealthAssessmentAgent()
    
    def detect_intent(self, query: str) -> str:
        """
        检测学生的提问意图
        
        Args:
            query: 用户查询
            
        Returns:
            str: 意图类型
        """
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in ["请假", "请假申请", "请几天假"]):
            return "leave_application"
        
        if any(keyword in query_lower for keyword in ["心理测评", "测评", "测试", "心理健康"]):
            return "mental_assessment"
        
        if any(keyword in query_lower for keyword in ["心情", "压力", "焦虑", "抑郁", "难过", "倾诉"]):
            return "psychological"
        
        return "qa"
    
    def run(self, state: UserState) -> UserState:
        """
        运行学生端工作流
        
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
        
        if intent == "leave_application":
            # 调用请假办理智能体
            application = self.leave_agent.create_application(query)
            response = f"{application['message']}\n\n"
            response += f"请假类型：{application['type']}\n"
            response += f"请假天数：{application['days']}天\n"
            response += f"请假原因：{application['reason']}\n"
            response += f"请假时间：{application['start_date']} 至 {application['end_date']}\n"
            response += f"提交时间：{application['submitted_at']}"
            agent_name = "leave_application_agent"
            
        elif intent == "mental_assessment":
            # 调用心理健康测评智能体
            response = self.assessment_agent.get_test_list()
            agent_name = "mental_assessment_agent"
            
        elif intent == "psychological":
            # 调用心理关怀智能体
            risk_level = self.psychological_agent.assess_risk_level(query)
            response = self.psychological_agent.generate_response(query, risk_level)
            agent_name = "psychological_agent"
            
            # 检查是否需要预警
            if self.psychological_agent.should_escalate(risk_level):
                state.add_notification(
                    "psychological_alert",
                    f"学生可能存在心理风险（等级：{risk_level}）",
                    "high" if risk_level == "high" else "medium"
                )
            
        else:
            # 调用学生问答智能体
            response = self.qa_agent.generate_answer(query)
            agent_name = "student_qa_agent"
        
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


def create_student_workflow():
    """创建学生端工作流"""
    workflow = StudentWorkflow()
    return workflow
