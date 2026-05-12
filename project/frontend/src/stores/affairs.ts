import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type AffairType = '请假' | '证明' | '咨询预约' | '其他'
export type AffairStatus = '待审批' | '已批准' | '已拒绝' | '已完成'

export interface AffairAttachment {
  name: string
  size: number
  type: string
  url?: string
  blob?: Blob
}

export interface Affair {
  id: string
  studentId: string
  studentName: string
  type: AffairType
  typeDetail: string
  details: string
  attachments?: AffairAttachment[]
  submitTime: string
  status: AffairStatus
  processedAt?: string
  handler?: string
  remark?: string
}

export interface LeaveDetail {
  leaveType: '病假' | '事假' | '公假' | '其他'
  startDate: string
  endDate: string
  reason: string
}

export interface CertificateDetail {
  certificateType: '在读证明' | '成绩证明' | '学籍证明' | '其他证明'
  purpose: string
}

const STORAGE_KEY = 'affairs_data'

export const useAffairsStore = defineStore('affairs', () => {
  const affairs = ref<Affair[]>([])
  const loading = ref(false)

  const saveToStorage = () => {
    const dataToSave = affairs.value.map(a => ({
      ...a,
      attachments: a.attachments?.map(att => ({
        name: att.name,
        size: att.size,
        type: att.type
      }))
    }))
    localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToSave))
  }

  const loadFromStorage = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        affairs.value = JSON.parse(saved)
        return true
      } catch {
        return false
      }
    }
    return false
  }

  const loadData = () => {
    if (loadFromStorage()) {
      return
    }
    
    affairs.value = [
      {
        id: 'affair_1',
        studentId: 'student_1',
        studentName: '张伟',
        type: '请假',
        typeDetail: '病假',
        details: '2024-01-15 至 2024-01-17，感冒发烧，需要休息',
        submitTime: '2024-01-14 20:00:00',
        status: '待审批'
      },
      {
        id: 'affair_2',
        studentId: 'student_2',
        studentName: '李娜',
        type: '证明',
        typeDetail: '在读证明',
        details: '用于实习申请',
        submitTime: '2024-01-13 15:30:00',
        status: '已批准',
        processedAt: '2024-01-13 16:00:00',
        handler: '王辅导员'
      },
      {
        id: 'affair_3',
        studentId: 'student_3',
        studentName: '王磊',
        type: '请假',
        typeDetail: '事假',
        details: '2024-01-20 至 2024-01-22，家庭事务',
        submitTime: '2024-01-12 10:00:00',
        status: '待审批'
      },
      {
        id: 'affair_4',
        studentId: 'student_1',
        studentName: '张伟',
        type: '证明',
        typeDetail: '成绩证明',
        details: '用于奖学金申请',
        submitTime: '2024-01-10 09:00:00',
        status: '已完成',
        processedAt: '2024-01-10 10:00:00',
        handler: '王辅导员'
      }
    ]
    saveToStorage()
  }

  const pendingCount = computed(() => 
    affairs.value.filter(a => a.status === '待审批').length
  )

  const approvedCount = computed(() => 
    affairs.value.filter(a => a.status === '已批准').length
  )

  const rejectedCount = computed(() => 
    affairs.value.filter(a => a.status === '已拒绝').length
  )

  const completedCount = computed(() => 
    affairs.value.filter(a => a.status === '已完成').length
  )

  const getAffairsByType = (type: AffairType) => {
    return affairs.value.filter(a => a.type === type)
  }

  const getAffairsByStatus = (status: AffairStatus) => {
    return affairs.value.filter(a => a.status === status)
  }

  const submitAffair = (affair: Omit<Affair, 'id' | 'submitTime' | 'status'>) => {
    const newAffair: Affair = {
      ...affair,
      id: `affair_${Date.now()}`,
      submitTime: new Date().toISOString(),
      status: '待审批'
    }
    affairs.value.unshift(newAffair)
    saveToStorage()
    return newAffair
  }

  const approveAffair = (id: string, remark?: string) => {
    const affair = affairs.value.find(a => a.id === id)
    if (affair) {
      affair.status = '已批准'
      affair.processedAt = new Date().toISOString()
      affair.handler = '王辅导员'
      affair.remark = remark
      saveToStorage()
    }
  }

  const rejectAffair = (id: string, remark?: string) => {
    const affair = affairs.value.find(a => a.id === id)
    if (affair) {
      affair.status = '已拒绝'
      affair.processedAt = new Date().toISOString()
      affair.handler = '王辅导员'
      affair.remark = remark
      saveToStorage()
    }
  }

  const completeAffair = (id: string) => {
    const affair = affairs.value.find(a => a.id === id)
    if (affair) {
      affair.status = '已完成'
      affair.processedAt = new Date().toISOString()
      saveToStorage()
    }
  }

  return {
    affairs,
    loading,
    loadData,
    pendingCount,
    approvedCount,
    rejectedCount,
    completedCount,
    getAffairsByType,
    getAffairsByStatus,
    submitAffair,
    approveAffair,
    rejectAffair,
    completeAffair
  }
})