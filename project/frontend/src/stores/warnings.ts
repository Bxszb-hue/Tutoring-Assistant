import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Warning {
  id: string
  studentId: string
  studentName: string
  type: '学业预警' | '心理预警' | '日常预警'
  level: '轻度' | '中度' | '重度'
  reason: string
  status: '待处理' | '处理中' | '已解决'
  createdAt: string
  updatedAt: string
  handler?: string
  notes?: string
}

export const useWarningsStore = defineStore('warnings', () => {
  const warnings = ref<Warning[]>([])
  const loading = ref(false)

  const loadWarnings = () => {
    warnings.value = [
      {
        id: 'warning_1',
        studentId: 'student_2',
        studentName: '李娜',
        type: '学业预警',
        level: '轻度',
        reason: '成绩下降，出勤率低',
        status: '待处理',
        createdAt: '2024-01-15 10:00:00',
        updatedAt: '2024-01-15 10:00:00'
      },
      {
        id: 'warning_2',
        studentId: 'student_3',
        studentName: '王磊',
        type: '学业预警',
        level: '中度',
        reason: '连续挂科，学分不足',
        status: '处理中',
        createdAt: '2024-01-14 09:00:00',
        updatedAt: '2024-01-14 15:00:00',
        handler: '王辅导员',
        notes: '已安排一对一辅导'
      },
      {
        id: 'warning_3',
        studentId: 'student_3',
        studentName: '王磊',
        type: '日常预警',
        level: '重度',
        reason: '多次违纪，晚归',
        status: '待处理',
        createdAt: '2024-01-13 16:00:00',
        updatedAt: '2024-01-13 16:00:00'
      }
    ]
  }

  const statistics = computed(() => {
    const total = warnings.value.length
    const pending = warnings.value.filter(w => w.status === '待处理').length
    const processing = warnings.value.filter(w => w.status === '处理中').length
    const resolved = warnings.value.filter(w => w.status === '已解决').length
    
    const byType = {
      academic: warnings.value.filter(w => w.type === '学业预警').length,
      psychological: warnings.value.filter(w => w.type === '心理预警').length,
      daily: warnings.value.filter(w => w.type === '日常预警').length
    }
    
    const byLevel = {
      mild: warnings.value.filter(w => w.level === '轻度').length,
      moderate: warnings.value.filter(w => w.level === '中度').length,
      severe: warnings.value.filter(w => w.level === '重度').length
    }
    
    return {
      total,
      pending,
      processing,
      resolved,
      byType,
      byLevel
    }
  })

  const updateWarningStatus = (id: string, status: Warning['status'], notes?: string) => {
    const warning = warnings.value.find(w => w.id === id)
    if (warning) {
      warning.status = status
      warning.updatedAt = new Date().toISOString()
      if (notes) {
        warning.notes = notes
      }
    }
  }

  return {
    warnings,
    loading,
    loadWarnings,
    statistics,
    updateWarningStatus
  }
})
