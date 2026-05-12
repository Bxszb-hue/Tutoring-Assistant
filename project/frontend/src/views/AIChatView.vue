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
            ref="aiChatRef"
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
                class="w-full text-left px-3 py-2 rounded-lg text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center gap-2 cursor-pointer"
                style="cursor: pointer;"
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

  <div v-if="showLeaveModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4">
      <div class="flex items-center justify-between p-4 border-b">
        <h3 class="text-lg font-semibold text-gray-900">请假申请</h3>
        <button @click="showLeaveModal = false" class="text-gray-400 hover:text-gray-600">
          <span class="text-xl">&times;</span>
        </button>
      </div>
      <div class="p-4 space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">请假类型</label>
          <select
            v-model="leaveForm.type"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择</option>
            <option value="病假">病假</option>
            <option value="事假">事假</option>
            <option value="公假">公假</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">开始日期</label>
            <input
              v-model="leaveForm.startDate"
              type="date"
              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
            <input
              v-model="leaveForm.endDate"
              type="date"
              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">请假原因</label>
          <textarea
            v-model="leaveForm.reason"
            rows="3"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请输入请假原因..."
          ></textarea>
        </div>
      </div>
      <div class="flex gap-3 p-4 border-t">
        <button
          @click="showLeaveModal = false"
          class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
        >
          取消
        </button>
        <button
          @click="submitLeaveRequest"
          :disabled="!isLeaveFormValid"
          class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 transition-colors"
        >
          提交申请
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { FileText, Users, AlertTriangle, BarChart3, BookOpen, HelpCircle, Heart, Calendar } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useAffairsStore } from '@/stores/affairs'
import AIChat from '@/components/AIChat.vue'
import { exportToExcel, generateStudentReport } from '@/utils/excel'
import { generateWarningWordReport, generateWorkWordReport, downloadBlob } from '@/utils/word'
import { useStudentsStore } from '@/stores/students'

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const affairsStore = useAffairsStore()
const aiChatRef = ref<InstanceType<typeof AIChat> | null>(null)

const showLeaveModal = ref(false)
const leaveForm = ref({
  type: '',
  startDate: '',
  endDate: '',
  reason: ''
})

const isLeaveFormValid = computed(() => {
  return leaveForm.value.type && leaveForm.value.startDate && leaveForm.value.endDate && leaveForm.value.reason
})

const submitLeaveRequest = () => {
  if (!isLeaveFormValid.value) return
  
  affairsStore.submitAffair({
    studentId: authStore.currentUser?.id || '',
    studentName: authStore.currentUser?.name || '',
    type: '请假',
    typeDetail: leaveForm.value.type,
    details: `${leaveForm.value.startDate} 至 ${leaveForm.value.endDate}，${leaveForm.value.reason}`
  })
  
  aiChatRef.value?.addMessage(
    `申请请假：${leaveForm.value.type}，${leaveForm.value.startDate} 至 ${leaveForm.value.endDate}`,
    `✅ 请假申请提交成功！\n\n📋 **申请详情**\n类型：${leaveForm.value.type}\n时间：${leaveForm.value.startDate} 至 ${leaveForm.value.endDate}\n原因：${leaveForm.value.reason}\n\n⏳ 等待辅导员审批中...`
  )
  
  showLeaveModal.value = false
  leaveForm.value = {
    type: '',
    startDate: '',
    endDate: '',
    reason: ''
  }
}

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
      '发布通知',
      '报表生成',
      '预警统计',
      '工作报告生成'
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
      { id: 'notification', label: '发布通知', icon: FileText },
      { id: 'report', label: '报表生成', icon: BarChart3 },
      { id: 'warnings', label: '预警统计', icon: AlertTriangle },
      { id: 'work_report', label: '工作报告生成', icon: FileText }
    ]
  } else {
    return [
      { id: 'grades', label: '查询成绩', icon: BookOpen },
      { id: 'leave', label: '请假申请', icon: Calendar },
      { id: 'help', label: '常见问题', icon: HelpCircle },
      { id: 'psychology', label: '心理支持', icon: Heart }
    ]
  }
})

const executeQuickAction = async (action: any) => {
  if (!studentsStore.students.length) {
    studentsStore.loadStudents()
  }
  
  if (action.id === 'notification') {
    aiChatRef.value?.showNotificationForm()
  } else if (action.id === 'report') {
    const reportData = generateStudentReport()
    exportToExcel(reportData)
    
    aiChatRef.value?.addMessage(
      '请帮我生成报表',
      '✅ 学生综合统计报表已生成！\n\n报表包含以下内容：\n- 学生概况（总数、男女比例、平均GPA等）\n- 风险等级分布\n- 班级统计\n- 挂科统计\n\n📥 已为您下载Excel文件。'
    )
  } else if (action.id === 'warnings') {
    const warningBlob = await generateWarningWordReport()
    downloadBlob(warningBlob, `学业预警报告_${new Date().toISOString().split('T')[0]}.docx`)
    
    aiChatRef.value?.addMessage(
      '请帮我查看预警统计',
      '✅ 学业预警报告已生成！\n\n报告包含以下内容：\n- 预警类型分布（学业/心理/日常）\n- 预警等级分布（轻度/中度/重度）\n- 预警学生名单及原因\n- 预警处理情况统计\n- 建议措施\n\n📥 已为您下载Word文档。'
    )
  } else if (action.id === 'work_report') {
    const warningBlob = await generateWarningWordReport()
    downloadBlob(warningBlob, `学业预警报告_${new Date().toISOString().split('T')[0]}.docx`)
    
    const workBlob = await generateWorkWordReport()
    downloadBlob(workBlob, `辅导员工作报告_${new Date().toISOString().split('T')[0]}.docx`)
    
    aiChatRef.value?.addMessage(
      '请帮我生成工作报告',
      '✅ 辅导员工作报告已生成！\n\n已调用预警统计智能体获取预警数据，并生成以下报告：\n\n📄 辅导员工作报告包含：\n- 工作概况（谈心谈话、家访等）\n- 预警管理情况\n- 事务办理统计\n- 活动组织记录\n- 月度总结\n\n📄 学业预警报告包含：\n- 预警类型分布\n- 预警等级分布\n- 预警学生名单\n- 预警处理情况\n\n📥 已为您下载两份Word文档。'
    )
  } else if (action.id === 'leave') {
    showLeaveModal.value = true
  } else {
    const messages: Record<string, string> = {
      grades: '请帮我查询我的成绩',
      help: '我想咨询一些常见问题',
      psychology: '我需要一些心理支持'
    }
    
    if (messages[action.id]) {
      const event = new CustomEvent('quickAction', { detail: messages[action.id] })
      window.dispatchEvent(event)
    }
  }
}
</script>
