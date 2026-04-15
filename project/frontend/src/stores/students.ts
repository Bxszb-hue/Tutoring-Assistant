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
