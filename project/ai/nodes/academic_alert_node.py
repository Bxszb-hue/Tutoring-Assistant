from typing import Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .academic_alert_tool import AcademicAlertTool

def academic_alert_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    学业预警智能体节点
    
    Args:
        state: 工作流状态
        
    Returns:
        Dict: 更新后的状态
    """
    print("Academic Alert Agent processing...")
    
    llm = state.get('llm')
    db = state.get('db')
    user_id = state.get('user_id')
    student_id = state.get('student_id', user_id)
    
    if not db:
        return {
            **state,
            'response': '无法访问数据库，请稍后重试',
            'agent_type': 'academic_alert'
        }
    
    # 创建预警工具
    alert_tool = AcademicAlertTool(db)
    
    # 分析学生学业状况
    analysis = alert_tool.analyze_student(student_id)
    
    # 生成预警报告
    if analysis['alerts']:
        alert_report = "\n\n".join([f"【{alert['level']}】{alert['message']}" 
                                    for alert in analysis['alerts']])
        
        # 生成预警记录
        for alert in analysis['alerts']:
            alert_tool.generate_alert(
                student_id=student_id,
                alert_type=alert['type'],
                alert_level=alert['level'],
                message=alert['message']
            )
    else:
        alert_report = "学生学业状况良好，暂无预警信息。"
    
    # 如果有LLM，生成自然语言回复
    if llm:
        prompt = PromptTemplate(
            input_variables=["student_id", "alert_report"],
            template="""作为学业预警助手，请根据以下分析结果，用友好、专业的语言向学生反馈：

学生ID: {student_id}

预警分析报告:
{alert_report}

请给出适当的建议和指导。
"""
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        response = chain.run(student_id=student_id, alert_report=alert_report)
    else:
        response = f"学业预警分析结果：\n\n{alert_report}"
    
    return {
        **state,
        'response': response,
        'agent_type': 'academic_alert',
        'analysis': analysis
    }