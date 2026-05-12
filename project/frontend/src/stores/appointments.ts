import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type AppointmentStatus = '待确认' | '已确认' | '已完成' | '已取消'

export interface Appointment {
  id: string
  studentId: string
  studentName: string
  counselorId: string
  counselorName: string
  type: '心理辅导' | '学业指导' | '职业规划' | '其他'
  date: string
  timeSlot: string
  reason: string
  status: AppointmentStatus
  createdAt: string
  confirmedAt?: string
  completedAt?: string
  remark?: string
}

const STORAGE_KEY = 'appointments_data'

export const useAppointmentsStore = defineStore('appointments', () => {
  const appointments = ref<Appointment[]>([])
  const loading = ref(false)

  const saveToStorage = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(appointments.value))
  }

  const loadFromStorage = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        appointments.value = JSON.parse(saved)
        return true
      } catch {
        return false
      }
    }
    return false
  }

  const timeSlots = [
    '08:00-09:00',
    '09:00-10:00',
    '10:00-11:00',
    '11:00-12:00',
    '14:00-15:00',
    '15:00-16:00',
    '16:00-17:00',
    '17:00-18:00'
  ]

  const loadData = () => {
    if (loadFromStorage()) {
      return
    }
    
    appointments.value = [
      {
        id: 'appt_1',
        studentId: 'student_2',
        studentName: '李娜',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        type: '心理辅导',
        date: '2024-01-16',
        timeSlot: '14:00-15:00',
        reason: '近期学习压力较大，希望进行心理疏导',
        status: '待确认',
        createdAt: '2024-01-14 16:00:00'
      },
      {
        id: 'appt_2',
        studentId: 'student_3',
        studentName: '王磊',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        type: '学业指导',
        date: '2024-01-17',
        timeSlot: '10:00-11:00',
        reason: '多门课程挂科，希望制定学习计划',
        status: '已确认',
        createdAt: '2024-01-13 10:00:00',
        confirmedAt: '2024-01-13 11:00:00'
      },
      {
        id: 'appt_3',
        studentId: 'student_1',
        studentName: '张伟',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        type: '职业规划',
        date: '2024-01-15',
        timeSlot: '15:00-16:00',
        reason: '了解实习和就业方向',
        status: '已完成',
        createdAt: '2024-01-12 09:00:00',
        confirmedAt: '2024-01-12 09:30:00',
        completedAt: '2024-01-15 16:00:00'
      }
    ]
  }

  const pendingCount = computed(() => 
    appointments.value.filter(a => a.status === '待确认').length
  )

  const confirmedCount = computed(() => 
    appointments.value.filter(a => a.status === '已确认').length
  )

  const completedCount = computed(() => 
    appointments.value.filter(a => a.status === '已完成').length
  )

  const getAppointmentsByStatus = (status: AppointmentStatus) => {
    return appointments.value.filter(a => a.status === status)
  }

  const getAvailableSlots = (date: string) => {
    const bookedSlots = appointments.value
      .filter(a => a.date === date && (a.status === '待确认' || a.status === '已确认'))
      .map(a => a.timeSlot)
    
    return timeSlots.filter(slot => !bookedSlots.includes(slot))
  }

  const createAppointment = (appointment: Omit<Appointment, 'id' | 'status' | 'createdAt'>) => {
    const newAppointment: Appointment = {
      ...appointment,
      id: `appt_${Date.now()}`,
      status: '待确认',
      createdAt: new Date().toISOString()
    }
    appointments.value.unshift(newAppointment)
    saveToStorage()
    return newAppointment
  }

  const confirmAppointment = (id: string) => {
    const index = appointments.value.findIndex(a => a.id === id)
    if (index !== -1) {
      appointments.value.splice(index, 1, {
        ...appointments.value[index],
        status: '已确认' as AppointmentStatus,
        confirmedAt: new Date().toISOString()
      })
      saveToStorage()
    }
  }

  const cancelAppointment = (id: string, remark?: string) => {
    const index = appointments.value.findIndex(a => a.id === id)
    if (index !== -1) {
      appointments.value.splice(index, 1, {
        ...appointments.value[index],
        status: '已取消' as AppointmentStatus,
        remark
      })
      saveToStorage()
    }
  }

  const completeAppointment = (id: string) => {
    const index = appointments.value.findIndex(a => a.id === id)
    if (index !== -1) {
      appointments.value.splice(index, 1, {
        ...appointments.value[index],
        status: '已完成' as AppointmentStatus,
        completedAt: new Date().toISOString()
      })
      saveToStorage()
    }
  }

  return {
    appointments,
    loading,
    timeSlots,
    loadData,
    pendingCount,
    confirmedCount,
    completedCount,
    getAppointmentsByStatus,
    getAvailableSlots,
    createAppointment,
    confirmAppointment,
    cancelAppointment,
    completeAppointment
  }
})