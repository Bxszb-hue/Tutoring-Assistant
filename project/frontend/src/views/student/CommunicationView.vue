<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">沟通倾诉</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">快速入口</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                v-for="channel in channels"
                :key="channel.id"
                class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                @click="handleChannelClick(channel)"
              >
                <div class="flex items-center gap-3 mb-2">
                  <component :is="channel.icon" :class="['w-5 h-5', channel.iconColor]" />
                  <h4 class="font-medium text-gray-900">{{ channel.name }}</h4>
                </div>
                <p class="text-sm text-gray-500">{{ channel.description }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">心理健康资源</h3>
            <div class="space-y-4">
              <div class="flex items-start gap-4 p-4 bg-blue-50 rounded-lg">
                <Phone class="w-6 h-6 text-blue-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">24小时心理热线</h4>
                  <p class="text-lg font-bold text-blue-600 mt-1">400-161-9995</p>
                  <p class="text-sm text-gray-600 mt-1">全国心理援助热线，24小时免费服务</p>
                </div>
              </div>
              
              <div class="flex items-start gap-4 p-4 bg-purple-50 rounded-lg">
                <Building class="w-6 h-6 text-purple-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">学校心理咨询中心</h4>
                  <p class="text-sm text-gray-600 mt-1">地址：学生活动中心3楼</p>
                  <p class="text-sm text-gray-600">时间：工作日 8:00-17:00</p>
                  <p class="text-sm text-gray-600">预约电话：0123-4567890</p>
                </div>
              </div>
              
              <div class="flex items-start gap-4 p-4 bg-green-50 rounded-lg">
                <Heart class="w-6 h-6 text-green-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">自我调节建议</h4>
                  <ul class="text-sm text-gray-600 mt-1 space-y-1">
                    <li>• 保持规律作息，充足睡眠</li>
                    <li>• 适度运动，释放压力</li>
                    <li>• 与朋友家人倾诉交流</li>
                    <li>• 培养兴趣爱好，放松心情</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">我的辅导员</h3>
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span class="text-white text-2xl font-bold">王</span>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">王辅导员</h4>
                <p class="text-sm text-gray-500">计算机学院</p>
                <div class="flex items-center gap-4 mt-2">
                  <div class="flex items-center gap-1 text-sm text-gray-600">
                    <Phone class="w-4 h-4" />
                    <span>13800138000</span>
                  </div>
                  <div class="flex items-center gap-1 text-sm text-gray-600">
                    <Mail class="w-4 h-4" />
                    <span>wang@university.edu</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">我的预约记录</h3>
            <div class="space-y-3">
              <div
                v-for="record in myAppointments"
                :key="record.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div>
                  <div class="flex items-center gap-2">
                    <component :is="getTypeIcon(record.type)" class="w-5 h-5 text-gray-400" />
                    <span class="font-medium text-gray-900">{{ record.type }}</span>
                  </div>
                  <p class="text-sm text-gray-500 mt-1">{{ record.date }} {{ record.timeSlot }}</p>
                </div>
                <span :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  record.status === '待确认' ? 'bg-yellow-100 text-yellow-700' :
                  record.status === '已确认' ? 'bg-blue-100 text-blue-700' :
                  record.status === '已完成' ? 'bg-green-100 text-green-700' :
                  'bg-red-100 text-red-700'
                ]">
                  {{ record.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showChat" class="w-96 border-l border-gray-200 bg-white flex flex-col">
      <div class="p-4 border-b border-gray-100 bg-gray-50">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span class="text-white text-sm font-medium">王</span>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">王辅导员</h3>
              <p class="text-sm text-gray-500">在线</p>
            </div>
          </div>
          <button
            @click="showChat = false"
            class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>
      </div>

      <div ref="chatContainerRef" class="flex-1 overflow-y-auto p-4 space-y-4">
        <div
          v-for="message in currentChatMessages"
          :key="message.id"
          :class="[
            'flex gap-3',
            message.senderRole === 'student' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            v-if="message.senderRole === 'counselor'"
            class="w-8 h-8 bg-gradient-to-br from-green-500 to-teal-600 rounded-lg flex items-center justify-center flex-shrink-0"
          >
            <span class="text-white text-xs font-medium">王</span>
          </div>
          <div
            :class="[
              'max-w-[80%]',
              message.senderRole === 'student' ? 'order-2' : 'order-1'
            ]"
          >
            <div
              :class="[
                'px-4 py-2 rounded-xl',
                message.senderRole === 'student'
                  ? 'bg-blue-600 text-white rounded-tr-sm'
                  : 'bg-gray-100 text-gray-900 rounded-tl-sm'
              ]"
            >
              <p class="text-sm">{{ message.content }}</p>
            </div>
            <p class="text-xs text-gray-400 mt-1">{{ formatTime(message.timestamp) }}</p>
          </div>
          <div
            v-if="message.senderRole === 'student'"
            class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0 order-1"
          >
            <span class="text-white text-xs font-medium">{{ userInitial }}</span>
          </div>
        </div>
      </div>

      <div class="p-4 border-t border-gray-100">
        <div class="flex gap-2">
          <input
            v-model="chatInput"
            @keydown.enter.prevent="sendChatMessage"
            type="text"
            placeholder="输入消息..."
            class="flex-1 px-4 py-2 bg-gray-100 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            @click="sendChatMessage"
            :disabled="!chatInput.trim()"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-xl transition-colors"
          >
            <Send class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <Modal
      v-if="modalVisible"
      :visible="modalVisible"
      :title="modalTitle"
      :show-footer="true"
      :show-cancel="true"
      :confirm-text="modalConfirmText"
      :disabled="!isFormValid"
      @close="handleModalClose"
      @confirm="handleModalConfirm"
    >
      <div v-if="modalType === 'appointment'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">咨询类型</label>
          <select
            v-model="formData.type"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择</option>
            <option value="心理辅导">心理辅导</option>
            <option value="学业指导">学业指导</option>
            <option value="职业规划">职业规划</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">选择日期</label>
          <input
            v-model="formData.date"
            type="date"
            @change="updateAvailableSlots"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">选择时间段</label>
          <select
            v-model="formData.timeSlot"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请先选择日期</option>
            <option v-for="slot in availableSlots" :key="slot" :value="slot">{{ slot }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">咨询原因</label>
          <textarea
            v-model="formData.reason"
            rows="3"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请简要说明咨询原因..."
          ></textarea>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { MessageSquare, Phone, Heart, Building, Calendar, Mail, X, Send, Sparkles } from 'lucide-vue-next'
import { useAppointmentsStore } from '@/stores/appointments'
import { useCounselorChatStore } from '@/stores/counselorChat'
import { useAuthStore } from '@/stores/auth'
import Modal from '@/components/Modal.vue'

const appointmentsStore = useAppointmentsStore()
const chatStore = useCounselorChatStore()
const authStore = useAuthStore()

const channels = ref([
  {
    id: 'counselor',
    name: '联系辅导员',
    description: '与辅导员一对一沟通',
    icon: MessageSquare,
    iconColor: 'text-blue-600'
  },
  {
    id: 'appointment',
    name: '预约咨询',
    description: '预约心理咨询服务',
    icon: Calendar,
    iconColor: 'text-purple-600'
  },
  {
    id: 'ai-chat',
    name: 'AI倾诉',
    description: '24小时在线倾听',
    icon: Heart,
    iconColor: 'text-pink-600'
  }
])

const showChat = ref(false)
const chatInput = ref('')

const modalVisible = ref(false)
const modalTitle = ref('')
const modalConfirmText = ref('')
const modalType = ref('')

const formData = ref({
  type: '',
  date: '',
  timeSlot: '',
  reason: ''
})

const availableSlots = ref<string[]>([])

const userInitial = computed(() => {
  return authStore.currentUser?.name?.charAt(0) || 'U'
})

const myAppointments = computed(() => {
  return appointmentsStore.appointments.filter(a => a.studentId === authStore.currentUser?.id)
})

const currentChatMessages = computed(() => {
  const session = chatStore.sessions.find(s => s.studentId === authStore.currentUser?.id)
  return session?.messages || []
})

const isFormValid = computed(() => {
  return formData.value.type && formData.value.date && formData.value.timeSlot && formData.value.reason
})

const getTypeIcon = (type: string) => {
  const icons: Record<string, any> = {
    '心理辅导': Heart,
    '学业指导': Sparkles,
    '职业规划': Building
  }
  return icons[type] || Calendar
}

const formatTime = (timestamp?: string) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const updateAvailableSlots = () => {
  if (formData.value.date) {
    availableSlots.value = appointmentsStore.getAvailableSlots(formData.value.date)
  } else {
    availableSlots.value = []
  }
}

const handleChannelClick = async (channel: any) => {
  if (channel.id === 'counselor') {
    showChat.value = true
    let session = chatStore.sessions.find(s => s.studentId === authStore.currentUser?.id)
    if (!session) {
      session = await chatStore.createSession(
        authStore.currentUser?.id || '',
        authStore.currentUser?.name || '',
        'counselor_1',
        '王辅导员'
      )
    }
    await chatStore.selectSession(session.id)
    chatStore.startPolling()
  } else if (channel.id === 'appointment') {
    modalTitle.value = '预约咨询'
    modalConfirmText.value = '提交预约'
    modalType.value = 'appointment'
    modalVisible.value = true
    formData.value = { type: '', date: '', timeSlot: '', reason: '' }
    availableSlots.value = []
  } else if (channel.id === 'ai-chat') {
    window.location.href = '/student/ai-chat'
  }
}

const sendChatMessage = async () => {
  if (!chatInput.value.trim()) return
  
  const session = chatStore.sessions.find(s => s.studentId === authStore.currentUser?.id)
  if (session) {
    await chatStore.sendMessage(
      session.id,
      chatInput.value,
      authStore.currentUser?.id || '',
      authStore.currentUser?.name || '',
      'student'
    )
    chatInput.value = ''
  }
}

const handleModalClose = () => {
  modalVisible.value = false
  formData.value = { type: '', date: '', timeSlot: '', reason: '' }
  availableSlots.value = []
}

const handleModalConfirm = () => {
  if (modalType.value === 'appointment') {
    appointmentsStore.createAppointment({
      studentId: authStore.currentUser?.id || '',
      studentName: authStore.currentUser?.name || '',
      counselorId: 'counselor_1',
      counselorName: '王辅导员',
      type: formData.value.type as any,
      date: formData.value.date,
      timeSlot: formData.value.timeSlot,
      reason: formData.value.reason
    })
  }
  handleModalClose()
}

const chatContainerRef = ref<HTMLElement | null>(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainerRef.value) {
      chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight
    }
  })
}

watch(currentChatMessages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(async () => {
  appointmentsStore.loadData()
  await chatStore.loadData(authStore.currentUser?.id || '', 'student')
})

onUnmounted(() => {
  chatStore.stopPolling()
})
</script>