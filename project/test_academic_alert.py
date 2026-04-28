import sys
sys.path.insert(0, '.')

from backend.database import SessionLocal
from ai.academic_alert_tool import AcademicAlertTool

# 创建数据库会话
db = SessionLocal()

# 创建预警工具
alert_tool = AcademicAlertTool(db)

print("=== 学业预警智能体测试 ===")

# 测试1：分析学生学业状况
print("\n1. 测试分析学生学业状况")
student_id = "2021001"  # 假设的学生ID
analysis = alert_tool.analyze_student(student_id)
print(f"学生ID: {analysis['student_id']}")
print(f"预警数量: {len(analysis['alerts'])}")
print(f"不及格课程: {len(analysis['failed_courses'])}门")
print(f"绩点状态: {analysis['gpa_status']}")
print(f"学分状态: {analysis['credit_status']}")
print(f"出勤状态: {analysis['attendance_status']}")

if analysis['alerts']:
    print("\n预警详情:")
    for alert in analysis['alerts']:
        print(f"  - 【{alert['level']}】{alert['type']}: {alert['message']}")

# 测试2：检查不及格课程
print("\n2. 测试检查不及格课程")
failed_courses = alert_tool.check_failed_courses(student_id)
print(f"不及格课程数量: {len(failed_courses)}")
for course in failed_courses[:3]:
    print(f"  - {course['course_name']}: {course['score']}分")

# 测试3：检查绩点
print("\n3. 测试检查绩点")
gpa_info = alert_tool.check_low_gpa(student_id)
if gpa_info:
    print(f"平均绩点: {gpa_info['avg_gpa']}，低于阈值{gpa_info['threshold']}")
else:
    print("绩点正常")

# 测试4：检查学分
print("\n4. 测试检查学分")
credit_info = alert_tool.check_missing_courses(student_id)
if credit_info:
    print(f"已修学分: {credit_info['earned_credits']}，还需修{credit_info['remaining_credits']}学分")
else:
    print("学分已达标")

# 测试5：生成预警
print("\n5. 测试生成预警")
result = alert_tool.generate_alert(
    student_id=student_id,
    alert_type="test",
    alert_level="medium",
    message="测试预警消息"
)
print(f"生成预警结果: {'成功' if result else '失败'}")

# 测试6：获取预警记录
print("\n6. 测试获取预警记录")
alerts = alert_tool.get_student_alerts(student_id)
print(f"预警记录数量: {len(alerts)}")
for alert in alerts[:3]:
    print(f"  - ID:{alert['id']} 类型:{alert['alert_type']} 级别:{alert['alert_level']}")

# 关闭数据库连接
db.close()

print("\n=== 测试完成 ===")