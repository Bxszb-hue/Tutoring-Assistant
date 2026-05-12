<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">事务办理</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="service in services"
              :key="service.id"
              class="bg-white rounded-xl border border-gray-100 p-6 hover:shadow-md transition-all cursor-pointer"
              @click="handleServiceClick(service)"
            >
              <div class="flex items-center gap-4">
                <div :class="['w-12 h-12 rounded-xl flex items-center justify-center', service.bgColor]">
                  <component :is="service.icon" :class="['w-6 h-6', service.iconColor]" />
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">{{ service.name }}</h3>
                  <p class="text-sm text-gray-500">{{ service.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900">我的申请记录</h3>
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
            <div class="space-y-3">
              <div
                v-for="record in filteredRecords"
                :key="record.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center gap-3">
                  <component :is="getTypeIcon(record.type)" class="w-5 h-5 text-gray-400" />
                  <div>
                    <p class="font-medium text-gray-900">{{ record.typeDetail }}</p>
                    <p class="text-sm text-gray-500">{{ record.details }}</p>
                    <p class="text-xs text-gray-400">{{ formatTime(record.submitTime) }}</p>
                  </div>
                </div>
                <span :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  record.status === '已批准' ? 'bg-green-100 text-green-700' :
                  record.status === '待审批' ? 'bg-yellow-100 text-yellow-700' :
                  record.status === '已拒绝' ? 'bg-red-100 text-red-700' :
                  'bg-gray-100 text-gray-700'
                ]">
                  {{ record.status }}
                </span>
              </div>
            </div>
          </div>
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
      <div v-if="activeService === 'leave'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">请假类型</label>
          <select
            v-model="formData.leaveType"
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
              v-model="formData.startDate"
              type="date"
              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">结束日期</label>
            <input
              v-model="formData.endDate"
              type="date"
              class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">请假原因</label>
          <textarea
            v-model="formData.reason"
            rows="3"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="请输入请假原因..."
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">附件上传（可选）</label>
          <div
            @click="triggerFileInput"
            class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 hover:bg-blue-50 cursor-pointer transition-colors"
          >
            <Upload class="w-8 h-8 text-gray-400 mx-auto mb-2" />
            <p class="text-sm text-gray-500">点击选择文件或拖拽上传</p>
            <p class="text-xs text-gray-400 mt-1">支持 PDF、图片、Word 等格式</p>
            <input
              ref="fileInputRef"
              type="file"
              multiple
              class="hidden"
              @change="handleFileSelect"
            />
          </div>
          <div v-if="formData.attachments.length > 0" class="mt-3 space-y-2">
            <div
              v-for="(file, index) in formData.attachments"
              :key="index"
              class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center gap-2">
                <FileText class="w-4 h-4 text-gray-400" />
                <span class="text-sm text-gray-700 truncate">{{ file.name }}</span>
              </div>
              <button
                @click="removeAttachment(index)"
                class="text-red-500 hover:text-red-700"
              >
                <X class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="activeService === 'certificate'" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">证明类型</label>
          <select
            v-model="formData.certificateType"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">请选择</option>
            <option value="在读证明">在读证明</option>
            <option value="成绩证明">成绩证明</option>
            <option value="学籍证明">学籍证明</option>
            <option value="其他证明">其他证明</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">用途</label>
          <input
            v-model="formData.purpose"
            type="text"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入证明用途..."
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">备注（可选）</label>
          <textarea
            v-model="formData.remark"
            rows="2"
            class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="如有其他需求，请在此说明..."
          ></textarea>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Calendar, FileText, CreditCard, Award, Upload, X } from 'lucide-vue-next'
import { useAffairsStore } from '@/stores/affairs'
import { useAuthStore } from '@/stores/auth'
import Modal from '@/components/Modal.vue'

const affairsStore = useAffairsStore()
const authStore = useAuthStore()

const services = ref([
  {
    id: 'leave',
    name: '请假申请',
    description: '病假、事假、公假等',
    icon: Calendar,
    bgColor: 'bg-blue-50',
    iconColor: 'text-blue-600'
  },
  {
    id: 'certificate',
    name: '证明开具',
    description: '在读证明、成绩证明等',
    icon: FileText,
    bgColor: 'bg-purple-50',
    iconColor: 'text-purple-600'
  }
])

const filterStatus = ref('')
const modalVisible = ref(false)
const modalTitle = ref('')
const modalConfirmText = ref('')
const activeService = ref('')

const formData = ref({
  leaveType: '',
  startDate: '',
  endDate: '',
  reason: '',
  certificateType: '',
  purpose: '',
  remark: '',
  attachments: [] as File[]
})

const fileInputRef = ref<HTMLInputElement | null>(null)

const triggerFileInput = () => {
  fileInputRef.value?.click()
}

const handleFileSelect = (event: any) => {
  const files = Array.from(event.target.files) as File[]
  formData.value.attachments = [...formData.value.attachments, ...files]
}

const removeAttachment = (index: number) => {
  formData.value.attachments.splice(index, 1)
}

const filteredRecords = computed(() => {
  let records = affairsStore.affairs.filter(a => a.studentId === authStore.currentUser?.id)
  if (filterStatus.value) {
    records = records.filter(r => r.status === filterStatus.value)
  }
  return records
})

const isFormValid = computed(() => {
  if (activeService.value === 'leave') {
    return formData.value.leaveType && formData.value.startDate && formData.value.endDate && formData.value.reason
  } else if (activeService.value === 'certificate') {
    return formData.value.certificateType && formData.value.purpose
  }
  return false
})

const getTypeIcon = (type: string) => {
  const icons: Record<string, any> = {
    '请假': Calendar,
    '证明': FileText
  }
  return icons[type] || FileText
}

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

const handleServiceClick = (service: any) => {
  if (service.id === 'leave' || service.id === 'certificate') {
    activeService.value = service.id
    modalTitle.value = service.name
    modalConfirmText.value = '提交申请'
    modalVisible.value = true
  } else {
    alert(`功能开发中：${service.name}`)
  }
}

const handleModalClose = () => {
  modalVisible.value = false
  formData.value = {
    leaveType: '',
    startDate: '',
    endDate: '',
    reason: '',
    certificateType: '',
    purpose: '',
    remark: '',
    attachments: []
  }
}

const handleModalConfirm = () => {
  if (activeService.value === 'leave') {
    affairsStore.submitAffair({
      studentId: authStore.currentUser?.id || '',
      studentName: authStore.currentUser?.name || '',
      type: '请假',
      typeDetail: formData.value.leaveType,
      details: `${formData.value.startDate} 至 ${formData.value.endDate}，${formData.value.reason}`,
      attachments: formData.value.attachments.map((f: File) => ({
        name: f.name,
        size: f.size,
        type: f.type,
        blob: f
      }))
    })
  } else if (activeService.value === 'certificate') {
    affairsStore.submitAffair({
      studentId: authStore.currentUser?.id || '',
      studentName: authStore.currentUser?.name || '',
      type: '证明',
      typeDetail: formData.value.certificateType,
      details: `用途：${formData.value.purpose}${formData.value.remark ? '，备注：' + formData.value.remark : ''}`
    })
  }
  
  handleModalClose()
}

onMounted(() => {
  affairsStore.loadData()
})
</script>