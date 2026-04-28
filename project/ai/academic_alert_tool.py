from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import json

class AcademicAlertTool:
    """学业预警工具类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_failed_courses(self, student_id: str, semester: str = None) -> List[Dict]:
        """
        检查不及格课程
        
        Args:
            student_id: 学生ID
            semester: 学期（可选）
        
        Returns:
            List[Dict]: 不及格课程列表
        """
        from backend.models import Grade, Course
        
        query = self.db.query(Grade, Course).join(Course, Grade.course_id == Course.course_id)
        query = query.filter(Grade.student_id == student_id)
        
        if semester:
            query = query.filter(Grade.semester == semester)
        
        # 筛选不及格课程（分数 < 60）
        results = query.filter(Grade.score < 60).all()
        
        failed_courses = []
        for grade, course in results:
            failed_courses.append({
                'course_id': course.course_id,
                'course_name': course.course_name,
                'score': grade.score,
                'semester': grade.semester,
                'credits': course.credits
            })
        
        return failed_courses
    
    def check_low_gpa(self, student_id: str, threshold: float = 2.0) -> Optional[Dict]:
        """
        检查绩点是否过低
        
        Args:
            student_id: 学生ID
            threshold: 绩点阈值（默认2.0）
        
        Returns:
            Dict: 绩点信息或None
        """
        from backend.models import Grade
        
        grades = self.db.query(Grade).filter(Grade.student_id == student_id).all()
        
        if not grades:
            return None
        
        total_gpa = sum(g.grade_point for g in grades if g.grade_point)
        avg_gpa = total_gpa / len(grades)
        
        if avg_gpa < threshold:
            return {
                'avg_gpa': round(avg_gpa, 2),
                'threshold': threshold,
                'course_count': len(grades)
            }
        
        return None
    
    def check_missing_courses(self, student_id: str, required_credits: int = 120) -> Optional[Dict]:
        """
        检查毕业学分是否达标
        
        Args:
            student_id: 学生ID
            required_credits: 毕业所需学分（默认120）
        
        Returns:
            Dict: 学分信息或None
        """
        from backend.models import Grade, Course
        
        completed_courses = self.db.query(Grade, Course).join(
            Course, Grade.course_id == Course.course_id
        ).filter(Grade.student_id == student_id).filter(Grade.score >= 60).all()
        
        earned_credits = sum(course.credits for _, course in completed_courses)
        
        if earned_credits < required_credits:
            return {
                'earned_credits': earned_credits,
                'required_credits': required_credits,
                'remaining_credits': required_credits - earned_credits,
                'completed_courses': len(completed_courses)
            }
        
        return None
    
    def check_attendance_rate(self, student_id: str, threshold: float = 0.8) -> Optional[Dict]:
        """
        检查出勤率（模拟数据）
        
        Args:
            student_id: 学生ID
            threshold: 出勤率阈值（默认80%）
        
        Returns:
            Dict: 出勤信息或None
        """
        # 模拟出勤数据（实际应用中应从教务系统获取）
        import random
        attendance_rate = random.uniform(0.6, 0.95)
        
        if attendance_rate < threshold:
            return {
                'attendance_rate': round(attendance_rate * 100, 1),
                'threshold': round(threshold * 100, 1),
                'warning': '出勤率低于要求'
            }
        
        return None
    
    def generate_alert(self, student_id: str, alert_type: str, alert_level: str, message: str) -> bool:
        """
        生成预警记录
        
        Args:
            student_id: 学生ID
            alert_type: 预警类型
            alert_level: 预警级别（low, medium, high）
            message: 预警消息
        
        Returns:
            bool: 是否成功
        """
        from backend.models import Alert
        
        try:
            alert = Alert(
                student_id=student_id,
                alert_type=alert_type,
                alert_level=alert_level,
                alert_message=message,
                is_processed=False,
                created_at=datetime.now()
            )
            self.db.add(alert)
            self.db.commit()
            return True
        except Exception as e:
            print(f"生成预警失败: {e}")
            self.db.rollback()
            return False
    
    def get_student_alerts(self, student_id: str, include_processed: bool = False) -> List[Dict]:
        """
        获取学生的预警记录
        
        Args:
            student_id: 学生ID
            include_processed: 是否包含已处理的预警
        
        Returns:
            List[Dict]: 预警记录列表
        """
        from backend.models import Alert
        
        query = self.db.query(Alert).filter(Alert.student_id == student_id)
        
        if not include_processed:
            query = query.filter(Alert.is_processed == False)
        
        alerts = query.all()
        
        return [{
            'id': alert.id,
            'alert_type': alert.alert_type,
            'alert_level': alert.alert_level,
            'alert_message': alert.alert_message,
            'is_processed': alert.is_processed,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for alert in alerts]
    
    def process_alert(self, alert_id: int) -> bool:
        """
        处理预警（标记为已处理）
        
        Args:
            alert_id: 预警ID
        
        Returns:
            bool: 是否成功
        """
        from backend.models import Alert
        
        alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
        
        if alert:
            alert.is_processed = True
            alert.processed_at = datetime.now()
            self.db.commit()
            return True
        
        return False
    
    def analyze_student(self, student_id: str) -> Dict[str, Any]:
        """
        全面分析学生学业状况
        
        Args:
            student_id: 学生ID
        
        Returns:
            Dict: 分析结果
        """
        results = {
            'student_id': student_id,
            'alerts': [],
            'warnings': [],
            'failed_courses': [],
            'gpa_status': 'normal',
            'credit_status': 'normal',
            'attendance_status': 'normal'
        }
        
        # 检查不及格课程
        failed_courses = self.check_failed_courses(student_id)
        if failed_courses:
            results['failed_courses'] = failed_courses
            results['alerts'].append({
                'level': 'high',
                'type': 'failed_courses',
                'message': f'有{len(failed_courses)}门课程不及格'
            })
        
        # 检查绩点
        gpa_info = self.check_low_gpa(student_id)
        if gpa_info:
            results['gpa_status'] = 'warning'
            results['gpa'] = gpa_info
            results['alerts'].append({
                'level': 'medium',
                'type': 'low_gpa',
                'message': f'平均绩点{ gpa_info["avg_gpa"]}，低于预警阈值{ gpa_info["threshold"]}'
            })
        
        # 检查学分
        credit_info = self.check_missing_courses(student_id)
        if credit_info:
            results['credit_status'] = 'warning'
            results['credits'] = credit_info
            remaining = credit_info['remaining_credits']
            if remaining > 40:
                results['alerts'].append({
                    'level': 'high',
                    'type': 'credit_shortage',
                    'message': f'学分差距较大，还需修读{remaining}学分'
                })
            else:
                results['alerts'].append({
                    'level': 'low',
                    'type': 'credit_shortage',
                    'message': f'还需修读{remaining}学分才能毕业'
                })
        
        # 检查出勤率
        attendance_info = self.check_attendance_rate(student_id)
        if attendance_info:
            results['attendance_status'] = 'warning'
            results['attendance'] = attendance_info
            results['alerts'].append({
                'level': 'medium',
                'type': 'low_attendance',
                'message': f'出勤率{attendance_info["attendance_rate"]}%，低于要求的{attendance_info["threshold"]}%'
            })
        
        return results