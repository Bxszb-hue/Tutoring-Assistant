-- 创建数据库
CREATE DATABASE IF NOT EXISTS counselor_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE counselor_agent;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    user_type VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建对话表
CREATE TABLE IF NOT EXISTS conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_agent_type (agent_type),
    INDEX idx_role (role),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建任务表
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    task_status VARCHAR(20) NOT NULL,
    task_data TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_task_type (task_type),
    INDEX idx_task_status (task_status),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建预警表
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    alert_level VARCHAR(20) NOT NULL,
    alert_message TEXT NOT NULL,
    is_processed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    INDEX idx_student_id (student_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_alert_level (alert_level),
    INDEX idx_is_processed (is_processed),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建学生详细信息表
CREATE TABLE IF NOT EXISTS student_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL UNIQUE,
    class_name VARCHAR(50),
    major VARCHAR(100),
    grade VARCHAR(10),
    department VARCHAR(100),
    enrollment_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_student_id (student_id),
    INDEX idx_class_name (class_name),
    INDEX idx_major (major),
    INDEX idx_grade (grade),
    INDEX idx_department (department),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建课程信息表
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id VARCHAR(50) NOT NULL UNIQUE,
    course_name VARCHAR(200) NOT NULL,
    course_type VARCHAR(20) NOT NULL,
    credits INT NOT NULL,
    teacher VARCHAR(100),
    department VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_course_id (course_id),
    INDEX idx_course_name (course_name),
    INDEX idx_course_type (course_type),
    INDEX idx_department (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建选课记录表
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_student_id (student_id),
    INDEX idx_course_id (course_id),
    INDEX idx_semester (semester),
    INDEX idx_status (status),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建成绩表
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    course_id VARCHAR(50) NOT NULL,
    score FLOAT,
    grade_point FLOAT,
    semester VARCHAR(20) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_student_id (student_id),
    INDEX idx_course_id (course_id),
    INDEX idx_semester (semester),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建事务申请表
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    transaction_data TEXT,
    status VARCHAR(20) NOT NULL,
    approver VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    INDEX idx_student_id (student_id),
    INDEX idx_transaction_type (transaction_type),
    INDEX idx_status (status),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入测试数据
INSERT INTO users (user_id, user_type, name, email, phone) VALUES
('student_001', 'student', '张三', 'zhangsan@example.com', '13800138001'),
('student_002', 'student', '李四', 'lisi@example.com', '13800138002'),
('counselor_001', 'counselor', '王老师', 'wanglaoshi@example.com', '13800138003');

-- 插入学生详细信息
INSERT INTO student_info (student_id, class_name, major, grade, department, enrollment_date) VALUES
('student_001', '计算机科学与技术1班', '计算机科学与技术', '2022级', '计算机学院', '2022-09-01'),
('student_002', '软件工程1班', '软件工程', '2022级', '计算机学院', '2022-09-01');

-- 插入课程信息
INSERT INTO courses (course_id, course_name, course_type, credits, teacher, department) VALUES
('CS101', '数据结构', '必修', 4, '李教授', '计算机学院'),
('CS102', '算法分析', '必修', 3, '王教授', '计算机学院'),
('CS103', '数据库原理', '必修', 3, '张教授', '计算机学院'),
('CS104', '操作系统', '必修', 4, '刘教授', '计算机学院'),
('CS105', '计算机网络', '必修', 3, '陈教授', '计算机学院'),
('CS106', '人工智能导论', '选修', 2, '赵教授', '计算机学院'),
('CS107', '机器学习', '选修', 3, '孙教授', '计算机学院'),
('CS108', '软件工程', '必修', 3, '周教授', '计算机学院'),
('CS109', '编译原理', '选修', 3, '吴教授', '计算机学院'),
('CS110', '分布式系统', '选修', 2, '郑教授', '计算机学院');

-- 插入选课记录
INSERT INTO enrollments (student_id, course_id, semester, status) VALUES
('student_001', 'CS101', '2022-2023-1', '已选'),
('student_001', 'CS102', '2022-2023-1', '已选'),
('student_001', 'CS103', '2022-2023-2', '已选'),
('student_001', 'CS104', '2023-2024-1', '已选'),
('student_001', 'CS105', '2023-2024-2', '已选'),
('student_001', 'CS106', '2024-2025-1', '已选'),
('student_002', 'CS101', '2022-2023-1', '已选'),
('student_002', 'CS102', '2022-2023-1', '已选'),
('student_002', 'CS103', '2022-2023-2', '已选'),
('student_002', 'CS104', '2023-2024-1', '已选'),
('student_002', 'CS105', '2023-2024-2', '已选'),
('student_002', 'CS107', '2024-2025-1', '已选');

-- 插入成绩
INSERT INTO grades (student_id, course_id, score, grade_point, semester) VALUES
('student_001', 'CS101', 85.5, 3.5, '2022-2023-1'),
('student_001', 'CS102', 78.0, 2.8, '2022-2023-1'),
('student_001', 'CS103', 92.0, 4.0, '2022-2023-2'),
('student_001', 'CS104', 88.0, 3.7, '2023-2024-1'),
('student_001', 'CS105', 76.5, 2.7, '2023-2024-2'),
('student_002', 'CS101', 90.0, 4.0, '2022-2023-1'),
('student_002', 'CS102', 82.0, 3.3, '2022-2023-1'),
('student_002', 'CS103', 87.5, 3.5, '2022-2023-2'),
('student_002', 'CS104', 79.0, 2.9, '2023-2024-1'),
('student_002', 'CS105', 85.0, 3.5, '2023-2024-2');

-- 插入事务申请
INSERT INTO transactions (student_id, transaction_type, transaction_data, status, approver) VALUES
('student_001', '选课申请', '{"course_id": "CS106", "reason": "对人工智能感兴趣"}', 'approved', 'counselor_001'),
('student_001', '退课申请', '{"course_id": "CS109", "reason": "课程时间冲突"}', 'pending', NULL),
('student_002', '选课申请', '{"course_id": "CS107", "reason": "专业方向相关"}', 'approved', 'counselor_001'),
('student_002', '成绩复查申请', '{"course_id": "CS104", "reason": "认为成绩有误"}', 'pending', NULL);

-- 创建请假申请表
CREATE TABLE IF NOT EXISTS leaves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    leave_type VARCHAR(20) NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    approver VARCHAR(50),
    approver_comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    processed_at DATETIME NULL,
    INDEX idx_student_id (student_id),
    INDEX idx_leave_type (leave_type),
    INDEX idx_status (status),
    FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入请假模拟数据
INSERT INTO leaves (student_id, leave_type, start_date, end_date, reason, status, approver, approver_comment) VALUES
('student_001', '事假', '2025-03-15 00:00:00', '2025-03-16 23:59:59', '家里有重要事情需要处理', 'approved', 'counselor_001', '情况属实，同意请假'),
('student_001', '病假', '2025-04-10 00:00:00', '2025-04-12 23:59:59', '感冒发烧需要休息', 'approved', 'counselor_001', '注意身体健康'),
('student_002', '公假', '2025-04-18 00:00:00', '2025-04-18 23:59:59', '参加学校组织的竞赛活动', 'pending', NULL, NULL),
('student_002', '事假', '2025-04-25 00:00:00', '2025-04-26 23:59:59', '需要参加亲戚婚礼', 'pending', NULL, NULL);
