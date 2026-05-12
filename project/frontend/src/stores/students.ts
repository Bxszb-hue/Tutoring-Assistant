import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Student {
  id: string
  name: string
  studentId: string
  className: string
  major: string
  riskLevel: '安全' | '关注' | '预警' | '紧急'
  tags: string[]
  grades: {
    gpa: number
    attendanceRate: number
    failedCourses: number
  }
  psychology: {
    status: '正常' | '轻度焦虑' | '中度焦虑' | '重度焦虑'
    lastAssessment?: string
  }
  contact: {
    phone: string
    email: string
  }
}

export const useStudentsStore = defineStore('students', () => {
  const students = ref<Student[]>([])
  const selectedStudent = ref<Student | null>(null)
  const loading = ref(false)

  const loadStudents = () => {
    students.value = [
      {
        id: 'student_1',
        name: '张伟',
        studentId: '20210001',
        className: '2021级1班',
        major: '计算机科学与技术',
        riskLevel: '安全',
        tags: ['学习优秀', '积极分子'],
        grades: {
          gpa: 3.5,
          attendanceRate: 95,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345678',
          email: 'zhangwei@university.edu'
        }
      },
      {
        id: 'student_2',
        name: '李娜',
        studentId: '20210002',
        className: '2021级1班',
        major: '计算机科学与技术',
        riskLevel: '关注',
        tags: ['成绩下降', '出勤率低'],
        grades: {
          gpa: 2.8,
          attendanceRate: 78,
          failedCourses: 1
        },
        psychology: {
          status: '轻度焦虑'
        },
        contact: {
          phone: '13812345679',
          email: 'lina@university.edu'
        }
      },
      {
        id: 'student_3',
        name: '王磊',
        studentId: '20210003',
        className: '2021级1班',
        major: '软件工程',
        riskLevel: '预警',
        tags: ['挂科', '违纪', '晚归'],
        grades: {
          gpa: 2.2,
          attendanceRate: 65,
          failedCourses: 3
        },
        psychology: {
          status: '中度焦虑'
        },
        contact: {
          phone: '13812345680',
          email: 'wanglei@university.edu'
        }
      },
      {
        id: 'student_4',
        name: '刘洋',
        studentId: '20210004',
        className: '2021级2班',
        major: '计算机科学与技术',
        riskLevel: '安全',
        tags: ['学生会成员'],
        grades: {
          gpa: 3.2,
          attendanceRate: 92,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345681',
          email: 'liuyang@university.edu'
        }
      },
      {
        id: 'student_5',
        name: '陈静',
        studentId: '20210005',
        className: '2021级2班',
        major: '软件工程',
        riskLevel: '关注',
        tags: ['家庭困难', '勤工助学'],
        grades: {
          gpa: 3.0,
          attendanceRate: 85,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345682',
          email: 'chenjing@university.edu'
        }
      },
      {
        id: 'student_6',
        name: '赵强',
        studentId: '20210006',
        className: '2021级2班',
        major: '计算机科学与技术',
        riskLevel: '安全',
        tags: ['体育特长', '奖学金获得者'],
        grades: {
          gpa: 3.8,
          attendanceRate: 98,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345683',
          email: 'zhaoqiang@university.edu'
        }
      },
      {
        id: 'student_7',
        name: '孙丽',
        studentId: '20220001',
        className: '2022级1班',
        major: '人工智能',
        riskLevel: '安全',
        tags: ['学习优秀'],
        grades: {
          gpa: 3.6,
          attendanceRate: 96,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345684',
          email: 'sunli@university.edu'
        }
      },
      {
        id: 'student_8',
        name: '周杰',
        studentId: '20220002',
        className: '2022级1班',
        major: '人工智能',
        riskLevel: '预警',
        tags: ['连续挂科', '心理问题'],
        grades: {
          gpa: 2.1,
          attendanceRate: 58,
          failedCourses: 4
        },
        psychology: {
          status: '重度焦虑'
        },
        contact: {
          phone: '13812345685',
          email: 'zhoujie@university.edu'
        }
      },
      {
        id: 'student_9',
        name: '吴敏',
        studentId: '20220003',
        className: '2022级2班',
        major: '数据科学',
        riskLevel: '安全',
        tags: ['优秀团员'],
        grades: {
          gpa: 3.4,
          attendanceRate: 94,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345686',
          email: 'wumin@university.edu'
        }
      },
      {
        id: 'student_10',
        name: '郑凯',
        studentId: '20220004',
        className: '2022级2班',
        major: '数据科学',
        riskLevel: '关注',
        tags: ['成绩波动'],
        grades: {
          gpa: 2.7,
          attendanceRate: 82,
          failedCourses: 1
        },
        psychology: {
          status: '轻度焦虑'
        },
        contact: {
          phone: '13812345687',
          email: 'zhengkai@university.edu'
        }
      },
      {
        id: 'student_11',
        name: '黄芳',
        studentId: '20230001',
        className: '2023级1班',
        major: '计算机科学与技术',
        riskLevel: '安全',
        tags: ['新生优秀'],
        grades: {
          gpa: 3.7,
          attendanceRate: 97,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345688',
          email: 'huangfang@university.edu'
        }
      },
      {
        id: 'student_12',
        name: '林涛',
        studentId: '20230002',
        className: '2023级1班',
        major: '计算机科学与技术',
        riskLevel: '关注',
        tags: ['适应困难'],
        grades: {
          gpa: 2.5,
          attendanceRate: 75,
          failedCourses: 1
        },
        psychology: {
          status: '轻度焦虑'
        },
        contact: {
          phone: '13812345689',
          email: 'lintao@university.edu'
        }
      },
      {
        id: 'student_13',
        name: '何欣',
        studentId: '20230003',
        className: '2023级2班',
        major: '软件工程',
        riskLevel: '安全',
        tags: ['社团骨干'],
        grades: {
          gpa: 3.3,
          attendanceRate: 90,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345690',
          email: 'hexin@university.edu'
        }
      },
      {
        id: 'student_14',
        name: '马涛',
        studentId: '20230004',
        className: '2023级2班',
        major: '软件工程',
        riskLevel: '安全',
        tags: ['科技竞赛获奖'],
        grades: {
          gpa: 3.9,
          attendanceRate: 99,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345691',
          email: 'matao@university.edu'
        }
      },
      {
        id: 'student_15',
        name: '罗雪',
        studentId: '20240001',
        className: '2024级1班',
        major: '人工智能',
        riskLevel: '安全',
        tags: ['新生'],
        grades: {
          gpa: 3.2,
          attendanceRate: 93,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345692',
          email: 'luoxue@university.edu'
        }
      },
      {
        id: 'student_16',
        name: '梁宇',
        studentId: '20240002',
        className: '2024级1班',
        major: '人工智能',
        riskLevel: '关注',
        tags: ['军训表现不佳'],
        grades: {
          gpa: 2.6,
          attendanceRate: 80,
          failedCourses: 0
        },
        psychology: {
          status: '轻度焦虑'
        },
        contact: {
          phone: '13812345693',
          email: 'liangyu@university.edu'
        }
      },
      {
        id: 'student_17',
        name: '谢婷',
        studentId: '20240003',
        className: '2024级2班',
        major: '数据科学',
        riskLevel: '安全',
        tags: ['新生干部'],
        grades: {
          gpa: 3.5,
          attendanceRate: 96,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345694',
          email: 'xieting@university.edu'
        }
      },
      {
        id: 'student_18',
        name: '韩鹏',
        studentId: '20240004',
        className: '2024级2班',
        major: '数据科学',
        riskLevel: '安全',
        tags: ['体育特长'],
        grades: {
          gpa: 3.1,
          attendanceRate: 91,
          failedCourses: 0
        },
        psychology: {
          status: '正常'
        },
        contact: {
          phone: '13812345695',
          email: 'hanpeng@university.edu'
        }
      }
    ]
  }

  const searchStudents = (keyword: string) => {
    return students.value.filter(s => 
      s.name.includes(keyword) || 
      s.studentId.includes(keyword) ||
      s.className.includes(keyword)
    )
  }

  const statistics = computed(() => {
    const total = students.value.length
    const byRiskLevel = {
      safe: students.value.filter(s => s.riskLevel === '安全').length,
      attention: students.value.filter(s => s.riskLevel === '关注').length,
      warning: students.value.filter(s => s.riskLevel === '预警').length,
      urgent: students.value.filter(s => s.riskLevel === '紧急').length
    }
    const averageGPA = students.value.reduce((sum, s) => sum + s.grades.gpa, 0) / total || 0
    const averageAttendance = students.value.reduce((sum, s) => sum + s.grades.attendanceRate, 0) / total || 0
    
    return {
      total,
      byRiskLevel,
      averageGPA: averageGPA.toFixed(2),
      averageAttendance: averageAttendance.toFixed(1)
    }
  })

  const classes = computed(() => {
    return [...new Set(students.value.map(s => s.className))]
  })

  const majors = computed(() => {
    return [...new Set(students.value.map(s => s.major))]
  })

  return {
    students,
    selectedStudent,
    loading,
    loadStudents,
    searchStudents,
    statistics,
    classes,
    majors
  }
})
