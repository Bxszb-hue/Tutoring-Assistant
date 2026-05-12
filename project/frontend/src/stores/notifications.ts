import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Notification {
  id: string
  title: string
  content: string
  type: 'system' | 'leave' | 'warning' | 'message'
  priority: 'low' | 'normal' | 'high'
  read: boolean
  createdAt: string
  targetClasses?: string[]
}

const STORAGE_KEY = 'counselor_notifications'

const defaultNotifications: Notification[] = [
  {
    id: 'notif_1',
    title: '系统维护通知',
    content: '系统将于今晚22:00-24:00进行维护，届时系统将无法访问。',
    type: 'system',
    priority: 'high',
    read: false,
    createdAt: '2024-01-15 08:00:00'
  },
  {
    id: 'notif_2',
    title: '期末考试安排',
    content: '期末考试将于2024年1月20日开始，请查看具体考试安排表。',
    type: 'system',
    priority: 'normal',
    read: false,
    createdAt: '2024-01-14 10:00:00'
  },
  {
    id: 'notif_3',
    title: '请假申请已批准',
    content: '您提交的病假申请（2024-01-10 至 2024-01-12）已批准。',
    type: 'leave',
    priority: 'normal',
    read: false,
    createdAt: '2024-01-10 09:00:00'
  },
  {
    id: 'notif_4',
    title: '心理测评提醒',
    content: '您有一份心理测评待完成，请在本周内完成测评。',
    type: 'system',
    priority: 'normal',
    read: false,
    createdAt: '2024-01-13 14:00:00'
  }
]

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])
  const loading = ref(false)

  const saveToStorage = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(notifications.value))
  }

  const loadData = () => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      notifications.value = JSON.parse(saved)
    } else {
      notifications.value = [...defaultNotifications]
      saveToStorage()
    }
  }

  const unreadCount = computed(() => {
    return {
      total: notifications.value.filter(n => !n.read).length,
      notifications: notifications.value.filter(n => !n.read && n.type === 'system').length,
      leaves: notifications.value.filter(n => !n.read && n.type === 'leave').length,
      warnings: notifications.value.filter(n => !n.read && n.type === 'warning').length
    }
  })

  const markAsRead = (id: string) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1, {
        ...notifications.value[index],
        read: true
      })
      saveToStorage()
    }
  }

  const markAllAsRead = () => {
    notifications.value = notifications.value.map(n => ({
      ...n,
      read: true
    }))
    saveToStorage()
  }

  const addNotification = (title: string, content: string, type: string, targetClasses: string[]) => {
    const priority = type === '紧急通知' ? 'high' : type === '重要通知' ? 'normal' : 'low'
    const notificationType = type === '紧急通知' || type === '重要通知' ? 'system' : 'message'
    
    const newNotification: Notification = {
      id: `notif_${Date.now()}`,
      title,
      content,
      type: notificationType,
      priority,
      read: false,
      createdAt: new Date().toLocaleString('zh-CN'),
      targetClasses
    }
    
    notifications.value.unshift(newNotification)
    saveToStorage()
    return newNotification
  }

  return {
    notifications,
    loading,
    loadData,
    unreadCount,
    markAsRead,
    markAllAsRead,
    addNotification
  }
})