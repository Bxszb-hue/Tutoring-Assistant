<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold text-gray-900">通知查看</h1>
          <button
            @click="markAllAsRead"
            class="px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
          >
            全部标为已读
          </button>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-4">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            :class="[
              'bg-white rounded-xl border p-6 transition-all cursor-pointer',
              notification.read ? 'border-gray-100' : 'border-blue-200 bg-blue-50'
            ]"
            @click="handleNotificationClick(notification)"
          >
            <div class="flex items-start gap-4">
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0',
                getTypeColor(notification.type)
              ]">
                <component :is="getTypeIcon(notification.type)" class="w-5 h-5 text-white" />
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <h3 class="font-semibold text-gray-900">{{ notification.title }}</h3>
                  <span v-if="!notification.read" class="w-2 h-2 bg-blue-600 rounded-full"></span>
                </div>
                <p class="text-sm text-gray-600 mb-2">{{ notification.content }}</p>
                <p class="text-xs text-gray-400">{{ notification.createdAt }}</p>
              </div>
              <span :class="[
                'px-2 py-1 rounded text-xs font-medium',
                getPriorityColor(notification.priority)
              ]">
                {{ getPriorityText(notification.priority) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Bell, AlertTriangle, FileText, MessageSquare } from 'lucide-vue-next'
import { useNotificationsStore } from '@/stores/notifications'

const notificationsStore = useNotificationsStore()

const notifications = ref([
  {
    id: '1',
    title: '系统维护通知',
    content: '系统将于今晚22:00-24:00进行维护，届时系统将无法访问。请提前做好准备。',
    type: 'system',
    priority: 'high',
    read: false,
    createdAt: '2024-01-15 08:00:00'
  },
  {
    id: '2',
    title: '期末考试安排',
    content: '期末考试将于2024年1月20日开始，请查看具体考试安排表。',
    type: 'system',
    priority: 'normal',
    read: false,
    createdAt: '2024-01-14 10:00:00'
  },
  {
    id: '3',
    title: '请假申请已批准',
    content: '您提交的病假申请（2024-01-10 至 2024-01-12）已批准。',
    type: 'leave',
    priority: 'normal',
    read: true,
    createdAt: '2024-01-10 09:00:00'
  },
  {
    id: '4',
    title: '心理测评提醒',
    content: '您有一份心理测评待完成，请在本周内完成测评。',
    type: 'warning',
    priority: 'normal',
    read: true,
    createdAt: '2024-01-13 14:00:00'
  }
])

const getTypeIcon = (type: string) => {
  const icons: Record<string, any> = {
    system: Bell,
    leave: FileText,
    warning: AlertTriangle,
    message: MessageSquare
  }
  return icons[type] || Bell
}

const getTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    system: 'bg-blue-500',
    leave: 'bg-purple-500',
    warning: 'bg-yellow-500',
    message: 'bg-green-500'
  }
  return colors[type] || 'bg-gray-500'
}

const getPriorityColor = (priority: string) => {
  const colors: Record<string, string> = {
    high: 'bg-red-100 text-red-700',
    normal: 'bg-blue-100 text-blue-700',
    low: 'bg-gray-100 text-gray-700'
  }
  return colors[priority] || 'bg-gray-100 text-gray-700'
}

const getPriorityText = (priority: string) => {
  const texts: Record<string, string> = {
    high: '重要',
    normal: '普通',
    low: '一般'
  }
  return texts[priority] || '普通'
}

const handleNotificationClick = (notification: any) => {
  notification.read = true
  notificationsStore.markAsRead(notification.id)
}

const markAllAsRead = () => {
  notifications.value.forEach(n => {
    n.read = true
  })
  notificationsStore.markAllAsRead()
}
</script>
