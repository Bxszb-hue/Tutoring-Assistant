import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserRole = 'counselor' | 'student'

export interface User {
  id: string
  name: string
  role: UserRole
  avatar?: string
  email: string
  phone?: string
  department?: string
  counselorId?: string
  className?: string
  studentId?: string
}

export const useAuthStore = defineStore('auth', () => {
  const currentUser = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)

  const loadUser = () => {
    const saved = localStorage.getItem('currentUser')
    if (saved) {
      currentUser.value = JSON.parse(saved)
      isAuthenticated.value = true
    }
  }

  const saveUser = () => {
    if (currentUser.value) {
      localStorage.setItem('currentUser', JSON.stringify(currentUser.value))
    } else {
      localStorage.removeItem('currentUser')
    }
  }

  const login = async (username: string, password: string, role: UserRole): Promise<boolean> => {
    loading.value = true
    
    await new Promise(resolve => setTimeout(resolve, 800))
    
    if (role === 'counselor') {
      if (username === 'counselor' && password === '123456') {
        currentUser.value = {
          id: 'counselor_1',
          name: '王辅导员',
          role: 'counselor',
          email: 'wang@university.edu',
          phone: '13800138000',
          department: '计算机学院'
        }
        isAuthenticated.value = true
        saveUser()
        loading.value = false
        return true
      }
    } else {
      if (username === 'student' && password === '123456') {
        currentUser.value = {
          id: 'student_1',
          name: '张伟',
          role: 'student',
          email: 'zhangwei@university.edu',
          phone: '13812345678',
          className: '2021级1班',
          studentId: '20210001',
          counselorId: 'counselor_1'
        }
        isAuthenticated.value = true
        saveUser()
        loading.value = false
        return true
      }
    }
    
    loading.value = false
    return false
  }

  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    saveUser()
  }

  const isCounselor = computed(() => currentUser.value?.role === 'counselor')
  const isStudent = computed(() => currentUser.value?.role === 'student')

  return {
    currentUser,
    isAuthenticated,
    loading,
    loadUser,
    login,
    logout,
    isCounselor,
    isStudent
  }
})
