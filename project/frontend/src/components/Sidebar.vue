<template>
  <aside class="w-16 bg-white border-r border-gray-100 flex flex-col h-full shadow-sm">
    <div class="p-3 border-b border-gray-50">
      <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto">
        <span class="text-white font-bold text-lg">🎓</span>
      </div>
    </div>

    <nav class="flex-1 p-3 space-y-2 overflow-y-auto">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center justify-center w-10 h-10 rounded-xl transition-all duration-200 group relative"
        :class="{
          'bg-blue-50 text-blue-600': $route.path === item.path,
          'text-gray-400 hover:text-gray-600 hover:bg-gray-50': $route.path !== item.path
        }"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <div class="absolute left-14 px-2 py-1 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
          {{ item.name }}
        </div>
        <span v-if="item.badge" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
          {{ item.badge }}
        </span>
      </router-link>
    </nav>

    <div class="p-3 border-t border-gray-50 space-y-2">
      <button
        @click="handleLogout"
        class="flex items-center justify-center w-10 h-10 rounded-xl text-gray-400 hover:text-red-600 hover:bg-red-50 transition-all duration-200 group relative"
      >
        <LogOut class="w-5 h-5" />
        <div class="absolute left-14 px-2 py-1 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50">
          退出登录
        </div>
      </button>
      
      <div class="w-10 h-10 mx-auto rounded-xl overflow-hidden border-2 border-gray-100">
        <div class="w-full h-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
          <span class="text-white text-sm font-medium">{{ userInitial }}</span>
        </div>
      </div>
    </div>

    <div class="p-2 border-t border-gray-50">
      <div class="flex flex-col items-center gap-1">
        <div class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-green-500"></span>
          <span class="text-[10px] text-gray-500">系统就绪</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Users, 
  AlertTriangle, 
  FileText, 
  BarChart3, 
  User, 
  ClipboardList, 
  MessageSquare, 
  Bell, 
  Activity,
  LogOut,
  Sparkles
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useWarningsStore } from '@/stores/warnings'
import { useNotificationsStore } from '@/stores/notifications'

const router = useRouter()
const authStore = useAuthStore()
const warningsStore = useWarningsStore()
const notificationsStore = useNotificationsStore()

const userInitial = computed(() => {
  return authStore.currentUser?.name?.charAt(0) || 'U'
})

const menuItems = computed(() => {
  if (authStore.isCounselor) {
    return [
      { name: '学生画像', path: '/counselor/students', icon: Users },
      { name: '智能预警', path: '/counselor/warnings', icon: AlertTriangle, badge: warningsStore.statistics.pending || undefined },
      { name: '事务处理', path: '/counselor/affairs', icon: FileText, badge: notificationsStore.unreadCount.leaves || undefined },
      { name: '数据统计', path: '/counselor/statistics', icon: BarChart3 },
      { name: 'AI 助手', path: '/counselor/ai-chat', icon: Sparkles }
    ]
  } else {
    return [
      { name: '个人中心', path: '/student/profile', icon: User },
      { name: '事务办理', path: '/student/affairs', icon: ClipboardList },
      { name: '沟通倾诉', path: '/student/communication', icon: MessageSquare },
      { name: '通知查看', path: '/student/notifications', icon: Bell, badge: notificationsStore.unreadCount.notifications || undefined },
      { name: '自我测评', path: '/student/assessment', icon: Activity },
      { name: 'AI 助手', path: '/student/ai-chat', icon: Sparkles }
    ]
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
