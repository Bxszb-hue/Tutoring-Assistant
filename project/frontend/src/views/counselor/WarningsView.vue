<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-bold text-gray-900">智能预警</h1>
          <div class="flex items-center gap-3">
            <select
              v-model="filterType"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部类型</option>
              <option value="学业预警">学业预警</option>
              <option value="心理预警">心理预警</option>
              <option value="日常预警">日常预警</option>
            </select>
            <select
              v-model="filterStatus"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部状态</option>
              <option value="待处理">待处理</option>
              <option value="处理中">处理中</option>
              <option value="已解决">已解决</option>
            </select>
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
                  <AlertTriangle class="w-5 h-5 text-red-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">待处理</p>
                  <p class="text-xl font-bold text-gray-900">{{ warningsStore.statistics.pending }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-yellow-50 rounded-lg flex items-center justify-center">
                  <Clock class="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">处理中</p>
                  <p class="text-xl font-bold text-gray-900">{{ warningsStore.statistics.processing }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center">
                  <CheckCircle class="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">已解决</p>
                  <p class="text-xl font-bold text-gray-900">{{ warningsStore.statistics.resolved }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-50 rounded-lg flex items-center justify-center">
                  <BarChart3 class="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">总计</p>
                  <p class="text-xl font-bold text-gray-900">{{ warningsStore.statistics.total }}</p>
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
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">等级</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">原因</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="warning in filteredWarnings"
                  :key="warning.id"
                  class="hover:bg-gray-50"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                        <span class="text-white text-sm font-medium">{{ warning.studentName.charAt(0) }}</span>
                      </div>
                      <div>
                        <p class="font-medium text-gray-900">{{ warning.studentName }}</p>
                        <p class="text-sm text-gray-500">{{ warning.studentId }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      warning.type === '学业预警' ? 'bg-blue-100 text-blue-700' :
                      warning.type === '心理预警' ? 'bg-purple-100 text-purple-700' :
                      'bg-yellow-100 text-yellow-700'
                    ]">
                      {{ warning.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      warning.level === '轻度' ? 'bg-green-100 text-green-700' :
                      warning.level === '中度' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    ]">
                      {{ warning.level }}
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <p class="text-sm text-gray-900">{{ warning.reason }}</p>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      warning.status === '待处理' ? 'bg-red-100 text-red-700' :
                      warning.status === '处理中' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-green-100 text-green-700'
                    ]">
                      {{ warning.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <button
                      @click="handleWarning(warning)"
                      class="text-blue-600 hover:text-blue-700 text-sm font-medium"
                    >
                      处理
                    </button>
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
import { AlertTriangle, Clock, CheckCircle, BarChart3 } from 'lucide-vue-next'
import { useWarningsStore } from '@/stores/warnings'

const warningsStore = useWarningsStore()

const filterType = ref('')
const filterStatus = ref('')

const filteredWarnings = computed(() => {
  let warnings = warningsStore.warnings
  
  if (filterType.value) {
    warnings = warnings.filter(w => w.type === filterType.value)
  }
  
  if (filterStatus.value) {
    warnings = warnings.filter(w => w.status === filterStatus.value)
  }
  
  return warnings
})

const handleWarning = (warning: any) => {
  alert(`处理预警：${warning.studentName} - ${warning.type}`)
}
</script>
