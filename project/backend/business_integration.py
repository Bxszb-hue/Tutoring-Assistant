from sqlalchemy.orm import Session
from sqlalchemy import and_
import json
from typing import List, Dict, Optional, Any
from .models import User, StudentInfo, Course, Enrollment, Grade, Transaction, Leave
from datetime import datetime, timedelta

class BusinessSystemIntegration:
    """业务系统集成工具类"""
    
    def __init__(self, db: Session):
        """初始化业务系统集成工具"""
        self.db = db
    
    def get_student_info(self, student_id: str) -> Optional[Dict[str, Any]]:
        """获取学生详细信息"""
        try:
            student = self.db.query(StudentInfo).filter(
                StudentInfo.student_id == student_id
            ).first()
            
            if not student:
                return None
            
            return {
                "student_id": student.student_id,
                "class_name": student.class_name,
                "major": student.major,
                "grade": student.grade,
                "department": student.department,
                "enrollment_date": student.enrollment_date.isoformat() if student.enrollment_date else None
            }
        except Exception as e:
            print(f"Error getting student info: {str(e)}")
            return None
    
    def get_courses(self, department: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取课程列表"""
        try:
            query = self.db.query(Course)
            if department:
                query = query.filter(Course.department == department)
            
            courses = query.all()
            return [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "course_type": course.course_type,
                    "credits": course.credits,
                    "teacher": course.teacher,
                    "department": course.department
                }
                for course in courses
            ]
        except Exception as e:
            print(f"Error getting courses: {str(e)}")
            return []
    
    def get_student_courses(self, student_id: str, semester: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取学生已选课程"""
        try:
            query = self.db.query(Enrollment, Course).join(
                Course, Enrollment.course_id == Course.course_id
            ).filter(Enrollment.student_id == student_id)
            
            if semester:
                query = query.filter(Enrollment.semester == semester)
            
            enrollments = query.all()
            return [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "course_type": course.course_type,
                    "credits": course.credits,
                    "teacher": course.teacher,
                    "semester": enrollment.semester,
                    "status": enrollment.status
                }
                for enrollment, course in enrollments
            ]
        except Exception as e:
            print(f"Error getting student courses: {str(e)}")
            return []
    
    def get_student_grades(self, student_id: str, semester: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取学生成绩"""
        try:
            query = self.db.query(Grade, Course).join(
                Course, Grade.course_id == Course.course_id
            ).filter(Grade.student_id == student_id)
            
            if semester:
                query = query.filter(Grade.semester == semester)
            
            grades = query.all()
            return [
                {
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "score": grade.score,
                    "grade_point": grade.grade_point,
                    "semester": grade.semester
                }
                for grade, course in grades
            ]
        except Exception as e:
            print(f"Error getting student grades: {str(e)}")
            return []
    
    def submit_transaction(self, student_id: str, transaction_type: str, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """提交事务申请"""
        try:
            # 验证学生是否存在
            student = self.db.query(User).filter(
                and_(User.user_id == student_id, User.user_type == "student")
            ).first()
            
            if not student:
                return {"success": False, "message": "学生不存在"}
            
            # 创建事务记录
            transaction = Transaction(
                student_id=student_id,
                transaction_type=transaction_type,
                transaction_data=json.dumps(transaction_data),
                status="pending"
            )
            
            self.db.add(transaction)
            self.db.commit()
            self.db.refresh(transaction)
            
            return {
                "success": True,
                "transaction_id": transaction.id,
                "message": "事务申请已提交"
            }
        except Exception as e:
            self.db.rollback()
            print(f"Error submitting transaction: {str(e)}")
            return {"success": False, "message": f"提交失败: {str(e)}"}
    
    def get_transactions(self, student_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取学生的事务申请"""
        try:
            query = self.db.query(Transaction).filter(
                Transaction.student_id == student_id
            )
            
            if status:
                query = query.filter(Transaction.status == status)
            
            transactions = query.order_by(Transaction.created_at.desc()).all()
            return [
                {
                    "transaction_id": transaction.id,
                    "transaction_type": transaction.transaction_type,
                    "transaction_data": json.loads(transaction.transaction_data) if transaction.transaction_data else {},
                    "status": transaction.status,
                    "approver": transaction.approver,
                    "created_at": transaction.created_at.isoformat(),
                    "processed_at": transaction.processed_at.isoformat() if transaction.processed_at else None
                }
                for transaction in transactions
            ]
        except Exception as e:
            print(f"Error getting transactions: {str(e)}")
            return []
    
    def process_transaction(self, transaction_id: int, status: str, approver: str) -> Dict[str, Any]:
        """处理事务申请"""
        try:
            transaction = self.db.query(Transaction).filter(
                Transaction.id == transaction_id
            ).first()
            
            if not transaction:
                return {"success": False, "message": "事务不存在"}
            
            transaction.status = status
            transaction.approver = approver
            transaction.processed_at = datetime.utcnow()
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "事务已处理"
            }
        except Exception as e:
            self.db.rollback()
            print(f"Error processing transaction: {str(e)}")
            return {"success": False, "message": f"处理失败: {str(e)}"}
    
    def get_all_transactions(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取所有事务申请（用于辅导员）"""
        try:
            query = self.db.query(Transaction, User).join(
                User, Transaction.student_id == User.user_id
            )
            
            if status:
                query = query.filter(Transaction.status == status)
            
            transactions = query.order_by(Transaction.created_at.desc()).all()
            return [
                {
                    "transaction_id": transaction.id,
                    "student_id": transaction.student_id,
                    "student_name": user.name,
                    "transaction_type": transaction.transaction_type,
                    "transaction_data": json.loads(transaction.transaction_data) if transaction.transaction_data else {},
                    "status": transaction.status,
                    "approver": transaction.approver,
                    "created_at": transaction.created_at.isoformat(),
                    "processed_at": transaction.processed_at.isoformat() if transaction.processed_at else None
                }
                for transaction, user in transactions
            ]
        except Exception as e:
            print(f"Error getting all transactions: {str(e)}")
            return []
    
    def validate_leave(self, student_id: str, leave_type: str, start_date: datetime, 
                      end_date: datetime, reason: str) -> Dict[str, Any]:
        """验证请假申请的合法性"""
        errors = []
        
        if not student_id:
            errors.append("学生ID不能为空")
        
        if leave_type not in ["事假", "病假", "公假"]:
            errors.append("请假类型必须是事假、病假或公假")
        
        if start_date >= end_date:
            errors.append("结束日期必须晚于开始日期")
        
        if start_date < datetime.now():
            errors.append("开始日期不能早于当前日期")
        
        leave_days = (end_date - start_date).days + 1
        if leave_days > 30:
            errors.append("单次请假不能超过30天")
        
        if not reason or len(reason.strip()) < 5:
            errors.append("请假理由不能少于5个字符")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def submit_leave(self, student_id: str, leave_type: str, start_date: datetime,
                    end_date: datetime, reason: str) -> Dict[str, Any]:
        """提交请假申请"""
        try:
            validation = self.validate_leave(student_id, leave_type, start_date, end_date, reason)
            if not validation["valid"]:
                return {
                    "success": False,
                    "message": "; ".join(validation["errors"])
                }
            
            student = self.db.query(User).filter(
                and_(User.user_id == student_id, User.user_type == "student")
            ).first()
            
            if not student:
                return {"success": False, "message": "学生不存在"}
            
            leave = Leave(
                student_id=student_id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                status="pending"
            )
            
            self.db.add(leave)
            self.db.commit()
            self.db.refresh(leave)
            
            return {
                "success": True,
                "leave_id": leave.id,
                "message": "请假申请已提交"
            }
        except Exception as e:
            self.db.rollback()
            print(f"Error submitting leave: {str(e)}")
            return {"success": False, "message": f"提交失败: {str(e)}"}
    
    def get_student_leaves(self, student_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取学生的请假记录"""
        try:
            query = self.db.query(Leave).filter(Leave.student_id == student_id)
            
            if status:
                query = query.filter(Leave.status == status)
            
            leaves = query.order_by(Leave.created_at.desc()).all()
            return [
                {
                    "leave_id": leave.id,
                    "leave_type": leave.leave_type,
                    "start_date": leave.start_date.isoformat(),
                    "end_date": leave.end_date.isoformat(),
                    "duration_days": (leave.end_date - leave.start_date).days + 1,
                    "reason": leave.reason,
                    "status": leave.status,
                    "approver": leave.approver,
                    "approver_comment": leave.approver_comment,
                    "created_at": leave.created_at.isoformat(),
                    "processed_at": leave.processed_at.isoformat() if leave.processed_at else None
                }
                for leave in leaves
            ]
        except Exception as e:
            print(f"Error getting student leaves: {str(e)}")
            return []
    
    def get_all_leaves(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取所有请假申请（用于辅导员）"""
        try:
            query = self.db.query(Leave, User).join(
                User, Leave.student_id == User.user_id
            )
            
            if status:
                query = query.filter(Leave.status == status)
            
            leaves = query.order_by(Leave.created_at.desc()).all()
            return [
                {
                    "leave_id": leave.id,
                    "student_id": leave.student_id,
                    "student_name": user.name,
                    "class_name": self.get_student_info(leave.student_id).get("class_name") if self.get_student_info(leave.student_id) else None,
                    "leave_type": leave.leave_type,
                    "start_date": leave.start_date.isoformat(),
                    "end_date": leave.end_date.isoformat(),
                    "duration_days": (leave.end_date - leave.start_date).days + 1,
                    "reason": leave.reason,
                    "status": leave.status,
                    "approver": leave.approver,
                    "approver_comment": leave.approver_comment,
                    "created_at": leave.created_at.isoformat(),
                    "processed_at": leave.processed_at.isoformat() if leave.processed_at else None
                }
                for leave, user in leaves
            ]
        except Exception as e:
            print(f"Error getting all leaves: {str(e)}")
            return []
    
    def process_leave(self, leave_id: int, status: str, approver: str, 
                     approver_comment: Optional[str] = None) -> Dict[str, Any]:
        """处理请假申请"""
        try:
            if status not in ["approved", "rejected"]:
                return {"success": False, "message": "审批状态必须是approved或rejected"}
            
            leave = self.db.query(Leave).filter(Leave.id == leave_id).first()
            
            if not leave:
                return {"success": False, "message": "请假申请不存在"}
            
            if leave.status != "pending":
                return {"success": False, "message": "该请假申请已被处理"}
            
            leave.status = status
            leave.approver = approver
            leave.approver_comment = approver_comment
            leave.processed_at = datetime.utcnow()
            
            self.db.commit()
            
            return {
                "success": True,
                "message": f"请假申请已{'批准' if status == 'approved' else '驳回'}"
            }
        except Exception as e:
            self.db.rollback()
            print(f"Error processing leave: {str(e)}")
            return {"success": False, "message": f"处理失败: {str(e)}"}
