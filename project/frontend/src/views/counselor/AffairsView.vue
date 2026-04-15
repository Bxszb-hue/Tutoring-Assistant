<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold text-gray-900">事务处理</h1>
          <div class="flex items-center gap-3">
            <select
              v-model="filterType"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部类型</option>
              <option value="请假">请假申请</option>
              <option value="证明">证明开具</option>
              <option value="其他">其他事务</option>
            </select>
            <select
              v-model="filterStatus"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部状态</option>
              <option value="待审批">待审批</option>
              <option value="已批准">已批准</option>
              <option value="已拒绝">已拒绝</option>
            </select>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-yellow-50 rounded-lg flex items-center justify-center">
                  <Clock class="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">待审批</p>
                  <p class="text-xl font-bold text-gray-900">{{ pendingCount }}</p>
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
                  <p class="text-xl font-bold text-gray-900">{{ approvedCount }}</p>
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
                  <p class="text-xl font-bold text-gray-900">{{ rejectedCount }}</p>
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
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <p class="text-sm text-gray-500">{{ affair.submitTime }}</p>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      affair.status === '待审批' ? 'bg-yellow-100 text-yellow-700' :
                      affair.status === '已批准' ? 'bg-green-100 text-green-700' :
                      'bg-red-100 text-red-700'
                    ]">
                      {{ affair.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div v-if="affair.status === '待审批'" class="flex gap-2">
                      <button
                        @click="approveAffair(affair)"
                        class="text-green-600 hover:text-green-700 text-sm font-medium"
                      >
                        批准
                      </button>
                      <button
                        @click="rejectAffair(affair)"
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
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Clock, CheckCircle, XCircle } from 'lucide-vue-next'

const filterType = ref('')
const filterStatus = ref('')

const affairs = ref([
  {
    id: '1',
    studentId: '20210001',
    studentName: '张伟',
    type: '请假',
    details: '病假：2024-01-15 至 2024-01-17，感冒发烧',
    submitTime: '2024-01-14 20:00',
    status: '待审批'
  },
  {
    id: '2',
    studentId: '20210002',
    studentName: '李娜',
    type: '证明',
    details: '在读证明，用于实习申请',
    submitTime: '2024-01-13 15:30',
    status: '已批准'
  },
  {
    id: '3',
    studentId: '20210003',
    studentName: '王磊',
    type: '请假',
    details: '事假：2024-01-20 至 2024-01-22，家庭事务',
    submitTime: '2024-01-12 10:00',
    status: '待审批'
  }
])

const filteredAffairs = computed(() => {
  let result = affairs.value
  
  if (filterType.value) {
    result = result.filter(a => a.type === filterType.value)
  }
  
  if (filterStatus.value) {
    result = result.filter(a => a.status === filterStatus.value)
  }
  
  return result
})

const pendingCount = computed(() => affairs.value.filter(a => a.status === '待审批').length)
const approvedCount = computed(() => affairs.value.filter(a => a.status === '已批准').length)
const rejectedCount = computed(() => affairs.value.filter(a => a.status === '已拒绝').length)

const approveAffair = (affair: any) => {
  affair.status = '已批准'
}

const rejectAffair = (affair: any) => {
  affair.status = '已拒绝'
}
</script>
