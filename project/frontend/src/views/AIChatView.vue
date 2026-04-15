<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold text-gray-900">AI 智能助手</h1>
            <span :class="[
              'px-3 py-1 rounded-lg text-sm',
              authStore.isCounselor ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'
            ]">
              {{ authStore.isCounselor ? '辅导员工作助手' : '学生学习助手' }}
            </span>
          </div>
          <div class="flex items-center gap-2">
            <button
              @click="clearChat"
              class="px-3 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg text-sm transition-colors"
            >
              清空对话
            </button>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-hidden flex">
        <div class="flex-1 flex flex-col">
          <AIChat
            :title="chatTitle"
            :subtitle="chatSubtitle"
            :role="authStore.isCounselor ? 'counselor' : 'student'"
            :welcome-message="welcomeMessage"
            :suggestions="suggestions"
            :input-placeholder="inputPlaceholder"
          />
        </div>

        <div class="w-80 border-l border-gray-200 bg-white flex flex-col">
          <div class="p-4 border-b border-gray-100">
            <h3 class="font-semibold text-gray-900 mb-3">快捷功能</h3>
            <div class="space-y-2">
              <button
                v-for="action in quickActions"
                :key="action.id"
                @click="executeQuickAction(action)"
                class="w-full text-left px-3 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center gap-2"
              >
                <component :is="action.icon" class="w-4 h-4 text-gray-400" />
                <span>{{ action.label }}</span>
              </button>
            </div>
          </div>

          <div class="p-4 border-t border-gray-100">
            <h3 class="font-semibold text-gray-900 mb-3">能力说明</h3>
            <div class="space-y-2 text-xs text-gray-600">
              <div class="flex items-start gap-2">
                <span class="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-medium">1</span>
                <span>{{ authStore.isCounselor ? '智能分析学生数据，生成个性化报告' : '智能解答学业和生活问题' }}</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-medium">2</span>
                <span>{{ authStore.isCounselor ? '提供预警干预建议和沟通策略' : '提供学习方法和心理调节建议' }}</span>
              </div>
              <div class="flex items-start gap-2">
                <span class="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-medium">3</span>
                <span>{{ authStore.isCounselor ? '自动生成工作报告和管理台账' : '24小时在线，随时解答疑问' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { FileText, Users, AlertTriangle, BarChart3, BookOpen, HelpCircle, Heart, Calendar } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import AIChat from '@/components/AIChat.vue'

const authStore = useAuthStore()

const clearChat = () => {
  const confirmed = window.confirm('确定要清空当前对话吗？')
  if (confirmed) {
    window.location.reload()
  }
}

const chatTitle = computed(() => {
  return authStore.isCounselor ? 'AI 工作助手' : 'AI 学习助手'
})

const chatSubtitle = computed(() => {
  return authStore.isCounselor ? '智能辅助 · 精准育人' : '智能陪伴 · 快乐学习'
})

const welcomeMessage = computed(() => {
  if (authStore.isCounselor) {
    return `你好！我是您的AI工作助手。我可以帮您分析学生情况、生成工作报告、提供干预建议、管理班级台账等。有什么我可以帮您的吗？`
  } else {
    return `你好！我是你的AI学习助手。我可以帮你查询成绩、解答学业问题、提供心理支持、解答常见问题等。有什么我可以帮你的吗？`
  }
})

const suggestions = computed(() => {
  if (authStore.isCounselor) {
    return [
      '分析学生整体情况',
      '生成本月工作报告',
      '查看预警统计',
      '生成班级管理台账'
    ]
  } else {
    return [
      '查询我的成绩',
      '如何申请请假？',
      '最近学习压力有点大',
      '选课相关问题'
    ]
  }
})

const inputPlaceholder = computed(() => {
  return authStore.isCounselor ? '输入您的需求...' : '输入你的问题...'
})

const quickActions = computed(() => {
  if (authStore.isCounselor) {
    return [
      { id: 'report', label: '生成工作报告', icon: FileText },
      { id: 'students', label: '分析学生数据', icon: Users },
      { id: 'warnings', label: '预警统计分析', icon: AlertTriangle },
      { id: 'statistics', label: '查看数据报表', icon: BarChart3 }
    ]
  } else {
    return [
      { id: 'grades', label: '查询成绩', icon: BookOpen },
      { id: 'help', label: '常见问题', icon: HelpCircle },
      { id: 'psychology', label: '心理支持', icon: Heart },
      { id: 'schedule', label: '事务办理', icon: Calendar }
    ]
  }
})

const executeQuickAction = (action: any) => {
  const messages: Record<string, string> = {
    report: '请帮我生成一份工作报告',
    students: '请帮我分析学生整体情况',
    warnings: '请帮我查看预警统计',
    statistics: '请帮我查看数据报表',
    grades: '请帮我查询我的成绩',
    help: '我想咨询一些常见问题',
    psychology: '我需要一些心理支持',
    schedule: '我想了解事务办理相关问题'
  }
  
  if (messages[action.id]) {
    const event = new CustomEvent('quickAction', { detail: messages[action.id] })
    window.dispatchEvent(event)
  }
}
</script>
