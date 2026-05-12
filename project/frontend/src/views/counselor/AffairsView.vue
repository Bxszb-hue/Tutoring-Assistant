<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold text-gray-900">事务处理</h1>
            <div class="flex gap-2">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                  activeTab === tab.id
                    ? 'bg-blue-50 text-blue-600'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                ]"
              >
                {{ tab.name }}
                <span v-if="tab.badge" :class="[
                  'ml-2 px-2 py-0.5 rounded-full text-xs',
                  tab.badge > 0 ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-500'
                ]">
                  {{ tab.badge }}
                </span>
              </button>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <select
              v-model="filterStatus"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部状态</option>
              <option value="待审批">待审批</option>
              <option value="已批准">已批准</option>
              <option value="已拒绝">已拒绝</option>
              <option value="已完成">已完成</option>
            </select>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <template v-if="activeTab === 'affairs'">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-yellow-50 rounded-lg flex items-center justify-center">
                    <Clock class="w-5 h-5 text-yellow-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">待审批</p>
                    <p class="text-xl font-bold text-gray-900">{{ affairsStore.pendingCount }}</p>
                  </div>
                </div>
              </div>
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center">
                    <CheckCircle class="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">已批准</p>
                    <p class="text-xl font-bold text-gray-900">{{ affairsStore.approvedCount }}</p>
                  </div>
                </div>
              </div>
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
                    <XCircle class="w-5 h-5 text-red-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">已拒绝</p>
                    <p class="text-xl font-bold text-gray-900">{{ affairsStore.rejectedCount }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
              <table class="w-full">
                <thead class="bg-gray-50 border-b border-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学生</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">类型</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">详情</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">提交时间</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr
                    v-for="affair in filteredAffairs"
                    :key="affair.id"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                          <span class="text-white text-sm font-medium">{{ affair.studentName.charAt(0) }}</span>
                        </div>
                        <div>
                          <p class="font-medium text-gray-900">{{ affair.studentName }}</p>
                          <p class="text-sm text-gray-500">{{ affair.studentId }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'px-2 py-1 rounded text-xs font-medium',
                        affair.type === '请假' ? 'bg-blue-100 text-blue-700' :
                        affair.type === '证明' ? 'bg-purple-100 text-purple-700' :
                        'bg-gray-100 text-gray-700'
                      ]">
                        {{ affair.type }}
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <p class="text-sm text-gray-900">{{ affair.details }}</p>
                      <div v-if="affair.attachments && affair.attachments.length > 0" class="mt-2 flex flex-wrap gap-1">
                        <span
                          v-for="(attachment, index) in affair.attachments"
                          :key="index"
                          @click.stop="viewAttachment(attachment)"
                          class="inline-flex items-center gap-1 px-2 py-1 bg-blue-50 text-blue-600 rounded text-xs cursor-pointer hover:bg-blue-100 transition-colors"
                          title="点击查看"
                          style="cursor: pointer;"
                        >
                          📎 {{ attachment.name }}
                        </span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <p class="text-sm text-gray-500">{{ formatTime(affair.submitTime) }}</p>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'px-2 py-1 rounded text-xs font-medium',
                        affair.status === '待审批' ? 'bg-yellow-100 text-yellow-700' :
                        affair.status === '已批准' ? 'bg-green-100 text-green-700' :
                        affair.status === '已拒绝' ? 'bg-red-100 text-red-700' :
                        'bg-gray-100 text-gray-700'
                      ]">
                        {{ affair.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div v-if="affair.status === '待审批'" class="flex gap-2">
                        <button
                          @click="handleApprove(affair)"
                          class="text-green-600 hover:text-green-700 text-sm font-medium"
                        >
                          批准
                        </button>
                        <button
                          @click="handleReject(affair)"
                          class="text-red-600 hover:text-red-700 text-sm font-medium"
                        >
                          拒绝
                        </button>
                      </div>
                      <span v-else class="text-gray-400 text-sm">已处理</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <template v-else-if="activeTab === 'appointments'">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-yellow-50 rounded-lg flex items-center justify-center">
                    <Clock class="w-5 h-5 text-yellow-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">待确认</p>
                    <p class="text-xl font-bold text-gray-900">{{ appointmentsStore.pendingCount }}</p>
                  </div>
                </div>
              </div>
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                    <Calendar class="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">已确认</p>
                    <p class="text-xl font-bold text-gray-900">{{ appointmentsStore.confirmedCount }}</p>
                  </div>
                </div>
              </div>
              <div class="bg-white rounded-xl border border-gray-100 p-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center">
                    <CheckCircle class="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">已完成</p>
                    <p class="text-xl font-bold text-gray-900">{{ appointmentsStore.completedCount }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
              <table class="w-full">
                <thead class="bg-gray-50 border-b border-gray-100">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">学生</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">类型</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">日期/时间</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">原因</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                  <tr
                    v-for="appointment in filteredAppointments"
                    :key="appointment.id"
                    class="hover:bg-gray-50"
                  >
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center gap-3">
                        <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                          <span class="text-white text-sm font-medium">{{ appointment.studentName.charAt(0) }}</span>
                        </div>
                        <div>
                          <p class="font-medium text-gray-900">{{ appointment.studentName }}</p>
                          <p class="text-sm text-gray-500">{{ appointment.studentId }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'px-2 py-1 rounded text-xs font-medium',
                        appointment.type === '心理辅导' ? 'bg-purple-100 text-purple-700' :
                        appointment.type === '学业指导' ? 'bg-blue-100 text-blue-700' :
                        appointment.type === '职业规划' ? 'bg-green-100 text-green-700' :
                        'bg-gray-100 text-gray-700'
                      ]">
                        {{ appointment.type }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <p class="text-sm text-gray-900">{{ appointment.date }}</p>
                      <p class="text-xs text-gray-500">{{ appointment.timeSlot }}</p>
                    </td>
                    <td class="px-6 py-4">
                      <p class="text-sm text-gray-900">{{ appointment.reason }}</p>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="[
                        'px-2 py-1 rounded text-xs font-medium',
                        appointment.status === '待确认' ? 'bg-yellow-100 text-yellow-700' :
                        appointment.status === '已确认' ? 'bg-blue-100 text-blue-700' :
                        appointment.status === '已完成' ? 'bg-green-100 text-green-700' :
                        'bg-red-100 text-red-700'
                      ]">
                        {{ appointment.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div v-if="appointment.status === '待确认'" class="flex gap-2">
                        <button
                          @click="handleConfirmAppointment(appointment)"
                          class="text-green-600 hover:text-green-700 text-sm font-medium"
                        >
                          确认
                        </button>
                        <button
                          @click="handleCancelAppointment(appointment)"
                          class="text-red-600 hover:text-red-700 text-sm font-medium"
                        >
                          取消
                        </button>
                      </div>
                      <button
                        v-else-if="appointment.status === '已确认'"
                        @click="handleCompleteAppointment(appointment)"
                        class="text-blue-600 hover:text-blue-700 text-sm font-medium"
                      >
                        完成
                      </button>
                      <span v-else class="text-gray-400 text-sm">已处理</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

          <template v-else-if="activeTab === 'chat'">
            <div class="flex gap-6">
              <div class="w-80 flex-shrink-0">
                <div class="bg-white rounded-xl border border-gray-100 overflow-hidden h-[calc(100vh-200px)] flex flex-col">
                  <div class="p-4 border-b border-gray-100">
                    <h3 class="font-semibold text-gray-900">学生消息</h3>
                    <p class="text-sm text-gray-500 mt-1">{{ chatStore.unreadTotal }} 条未读</p>
                  </div>
                  <div class="flex-1 overflow-y-auto">
                    <div
                      v-for="session in chatStore.sessions"
                      :key="session.id"
                      @click="handleSelectSession(session.id)"
                      :class="[
                        'p-4 cursor-pointer transition-colors',
                        chatStore.activeSessionId === session.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                      ]"
                    >
                      <div class="flex items-center gap-3">
                        <div class="relative">
                          <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                            <span class="text-white text-sm font-medium">{{ session.studentName.charAt(0) }}</span>
                          </div>
                          <span v-if="session.unreadCount > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                            {{ session.unreadCount }}
                          </span>
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="font-medium text-gray-900 truncate">{{ session.studentName }}</p>
                          <p class="text-sm text-gray-500 truncate">{{ session.lastMessage }}</p>
                        </div>
                        <p class="text-xs text-gray-400">{{ formatTime(session.lastMessageTime) }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex-1">
                <div v-if="chatStore.activeSession" class="bg-white rounded-xl border border-gray-100 overflow-hidden h-[calc(100vh-200px)] flex flex-col">
                  <div class="p-4 border-b border-gray-100 bg-gray-50">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                        <span class="text-white text-sm font-medium">{{ chatStore.activeSession.studentName.charAt(0) }}</span>
                      </div>
                      <div>
                        <h3 class="font-semibold text-gray-900">{{ chatStore.activeSession.studentName }}</h3>
                        <p class="text-sm text-gray-500">{{ chatStore.activeSession.studentId }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="flex-1 overflow-y-auto p-4 space-y-4">
                    <div
                      v-for="message in chatStore.activeSession.messages"
                      :key="message.id"
                      :class="[
                        'flex gap-3',
                        message.senderRole === 'counselor' ? 'justify-end' : 'justify-start'
                      ]"
                    >
                      <div
                        v-if="message.senderRole === 'student'"
                        class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0"
                      >
                        <span class="text-white text-xs font-medium">{{ message.senderName.charAt(0) }}</span>
                      </div>
                      <div
                        :class="[
                          'max-w-[70%]',
                          message.senderRole === 'counselor' ? 'order-2' : 'order-1'
                        ]"
                      >
                        <div
                          :class="[
                            'px-4 py-2 rounded-xl',
                            message.senderRole === 'counselor'
                              ? 'bg-blue-600 text-white rounded-tr-sm'
                              : 'bg-gray-100 text-gray-900 rounded-tl-sm'
                          ]"
                        >
                          <p class="text-sm">{{ message.content }}</p>
                        </div>
                        <p class="text-xs text-gray-400 mt-1">{{ formatTime(message.timestamp) }}</p>
                      </div>
                      <div
                        v-if="message.senderRole === 'counselor'"
                        class="w-8 h-8 bg-gradient-to-br from-green-500 to-teal-600 rounded-lg flex items-center justify-center flex-shrink-0 order-1"
                      >
                        <span class="text-white text-xs font-medium">王</span>
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

                <div v-else class="bg-white rounded-xl border border-gray-100 p-12 text-center h-[calc(100vh-200px)] flex flex-col items-center justify-center">
                  <MessageSquare class="w-16 h-16 text-gray-300 mb-4" />
                  <p class="text-gray-500">选择一个学生开始对话</p>
                </div>
              </div>
            </div>
          </template>
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
      @close="modalVisible = false"
      @confirm="handleModalConfirm"
    >
      <div v-if="modalType === 'approve' || modalType === 'reject'" class="space-y-4">
        <div>
          <p class="text-sm text-gray-600 mb-2">处理意见（可选）</p>
          <textarea
            v-model="modalRemark"
            rows="3"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请输入处理意见..."
          ></textarea>
        </div>
      </div>
      <div v-else-if="modalType === 'cancel-appointment'" class="space-y-4">
        <div>
          <p class="text-sm text-gray-600 mb-2">取消原因（可选）</p>
          <textarea
            v-model="modalRemark"
            rows="3"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请输入取消原因..."
          ></textarea>
        </div>
      </div>
    </Modal>

    <div v-if="showAttachmentModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl mx-4">
        <div class="flex items-center justify-between p-4 border-b">
          <h3 class="text-lg font-semibold text-gray-900">{{ selectedAttachment?.name }}</h3>
          <button @click="showAttachmentModal = false" class="text-gray-400 hover:text-gray-600">
            <span class="text-xl">&times;</span>
          </button>
        </div>
        <div class="p-6">
          <div v-if="selectedAttachment?.type?.startsWith('image/')" class="flex justify-center">
            <img :src="selectedAttachment.url || URL.createObjectURL(selectedAttachment.blob)" alt="附件图片" class="max-w-full max-h-[60vh] object-contain rounded-lg" />
          </div>
          <div v-else class="text-center py-8">
            <p class="text-gray-500">该附件无法在线预览</p>
            <button
              @click="downloadAttachment"
              class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              下载附件
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Clock, CheckCircle, XCircle, Calendar, Send, MessageSquare } from 'lucide-vue-next'
import { useAffairsStore } from '@/stores/affairs'
import { useAppointmentsStore } from '@/stores/appointments'
import { useCounselorChatStore } from '@/stores/counselorChat'
import { useAuthStore } from '@/stores/auth'
import Modal from '@/components/Modal.vue'
import type { Affair } from '@/stores/affairs'
import type { Appointment } from '@/stores/appointments'

const affairsStore = useAffairsStore()
const appointmentsStore = useAppointmentsStore()
const chatStore = useCounselorChatStore()
const authStore = useAuthStore()

const activeTab = ref<'affairs' | 'appointments' | 'chat'>('affairs')
const filterStatus = ref('')
const chatInput = ref('')

const modalVisible = ref(false)
const modalTitle = ref('')
const modalConfirmText = ref('')
const modalType = ref('')
const modalRemark = ref('')
const modalData = ref<any>(null)

const showAttachmentModal = ref(false)
const selectedAttachment = ref<any>(null)

const viewAttachment = (attachment: any) => {
  console.log('viewAttachment called:', attachment)
  selectedAttachment.value = attachment
  showAttachmentModal.value = true
}

const downloadAttachment = () => {
  if (selectedAttachment.value?.blob) {
    const url = URL.createObjectURL(selectedAttachment.value.blob)
    const a = document.createElement('a')
    a.href = url
    a.download = selectedAttachment.value.name
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
  showAttachmentModal.value = false
}

const tabs = computed(() => [
  { id: 'affairs', name: '事务申请', badge: affairsStore.pendingCount },
  { id: 'appointments', name: '预约咨询', badge: appointmentsStore.pendingCount },
  { id: 'chat', name: '线上沟通', badge: chatStore.unreadTotal }
])

const filteredAffairs = computed(() => {
  let result = affairsStore.affairs
  if (filterStatus.value) {
    result = result.filter(a => a.status === filterStatus.value)
  }
  return result
})

const filteredAppointments = computed(() => {
  let result = appointmentsStore.appointments
  if (filterStatus.value) {
    result = result.filter(a => a.status === filterStatus.value)
  }
  return result
})

const formatTime = (timestamp?: string) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const handleApprove = (affair: Affair) => {
  modalTitle.value = '批准申请'
  modalConfirmText.value = '批准'
  modalType.value = 'approve'
  modalData.value = affair
  modalRemark.value = ''
  modalVisible.value = true
}

const handleReject = (affair: Affair) => {
  modalTitle.value = '拒绝申请'
  modalConfirmText.value = '拒绝'
  modalType.value = 'reject'
  modalData.value = affair
  modalRemark.value = ''
  modalVisible.value = true
}

const handleConfirmAppointment = (appointment: Appointment) => {
  appointmentsStore.confirmAppointment(appointment.id)
}

const handleCancelAppointment = (appointment: Appointment) => {
  modalTitle.value = '取消预约'
  modalConfirmText.value = '取消'
  modalType.value = 'cancel-appointment'
  modalData.value = appointment
  modalRemark.value = ''
  modalVisible.value = true
}

const handleCompleteAppointment = (appointment: Appointment) => {
  appointmentsStore.completeAppointment(appointment.id)
}

const handleSelectSession = async (sessionId: string) => {
  await chatStore.selectSession(sessionId)
  chatStore.startPolling()
}

const sendChatMessage = async () => {
  if (!chatInput.value.trim() || !chatStore.activeSessionId) return
  
  await chatStore.sendMessage(
    chatStore.activeSessionId,
    chatInput.value,
    authStore.currentUser?.id || '',
    authStore.currentUser?.name || '',
    'counselor'
  )
  chatInput.value = ''
}

const handleModalConfirm = () => {
  if (modalType.value === 'approve') {
    affairsStore.approveAffair(modalData.value.id, modalRemark.value)
  } else if (modalType.value === 'reject') {
    affairsStore.rejectAffair(modalData.value.id, modalRemark.value)
  } else if (modalType.value === 'cancel-appointment') {
    appointmentsStore.cancelAppointment(modalData.value.id, modalRemark.value)
  }
  modalVisible.value = false
}

onMounted(async () => {
  affairsStore.loadData()
  appointmentsStore.loadData()
  await chatStore.loadData('counselor_1', 'counselor')
})

onUnmounted(() => {
  chatStore.stopPolling()
})
</script>