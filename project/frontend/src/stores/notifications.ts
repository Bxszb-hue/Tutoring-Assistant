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
}

export const useNotificationsStore = defineStore('notifications', () => {
  const notifications = ref<Notification[]>([])
  const loading = ref(false)

  const loadData = () => {
    notifications.value = [
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
        title: '请假申请待审批',
        content: '张伟同学提交了请假申请，请及时审批。',
        type: 'leave',
        priority: 'normal',
        read: false,
        createdAt: '2024-01-14 15:30:00'
      },
      {
        id: 'notif_3',
        title: '预警提醒',
        content: '王磊同学出现新的预警信息，请及时处理。',
        type: 'warning',
        priority: 'high',
        read: true,
        createdAt: '2024-01-13 16:00:00'
      }
    ]
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
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.read = true
    }
  }

  const markAllAsRead = () => {
    notifications.value.forEach(n => {
      n.read = true
    })
  }

  return {
    notifications,
    loading,
    loadData,
    unreadCount,
    markAsRead,
    markAllAsRead
  }
})
