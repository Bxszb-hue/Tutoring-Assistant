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
            <h3 class="text-lg font-semibold text-gray-900 mb-4">我的申请记录</h3>
            <div class="space-y-3">
              <div
                v-for="record in records"
                :key="record.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center gap-3">
                  <component :is="record.icon" class="w-5 h-5 text-gray-400" />
                  <div>
                    <p class="font-medium text-gray-900">{{ record.type }}</p>
                    <p class="text-sm text-gray-500">{{ record.date }}</p>
                  </div>
                </div>
                <span :class="[
                  'px-3 py-1 rounded-full text-xs font-medium',
                  record.status === '已批准' ? 'bg-green-100 text-green-700' :
                  record.status === '待审批' ? 'bg-yellow-100 text-yellow-700' :
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
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Calendar, FileText, CreditCard, Award, HelpCircle } from 'lucide-vue-next'

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
  },
  {
    id: 'payment',
    name: '费用缴纳',
    description: '学费、住宿费等',
    icon: CreditCard,
    bgColor: 'bg-green-50',
    iconColor: 'text-green-600'
  },
  {
    id: 'scholarship',
    name: '奖助贷申请',
    description: '奖学金、助学金、贷款',
    icon: Award,
    bgColor: 'bg-yellow-50',
    iconColor: 'text-yellow-600'
  }
])

const records = ref([
  {
    id: '1',
    type: '病假申请',
    date: '2024-01-10 至 2024-01-12',
    status: '已批准',
    icon: Calendar
  },
  {
    id: '2',
    type: '在读证明',
    date: '2024-01-08',
    status: '已批准',
    icon: FileText
  },
  {
    id: '3',
    type: '事假申请',
    date: '2024-01-15 至 2024-01-16',
    status: '待审批',
    icon: Calendar
  }
])

const handleServiceClick = (service: any) => {
  alert(`功能开发中：${service.name}`)
}
</script>
