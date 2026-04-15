<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">自我测评</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">心理健康测评</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="assessment in assessments"
                :key="assessment.id"
                class="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                @click="handleAssessmentClick(assessment)"
              >
                <div class="flex items-center gap-3 mb-2">
                  <component :is="assessment.icon" :class="['w-5 h-5', assessment.iconColor]" />
                  <h4 class="font-medium text-gray-900">{{ assessment.name }}</h4>
                </div>
                <p class="text-sm text-gray-500 mb-2">{{ assessment.description }}</p>
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-400">预计用时：{{ assessment.duration }}</span>
                  <span :class="[
                    'text-xs font-medium',
                    assessment.completed ? 'text-green-600' : 'text-blue-600'
                  ]">
                    {{ assessment.completed ? '已完成' : '开始测评' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">测评历史</h3>
            <div class="space-y-3">
              <div
                v-for="record in historyRecords"
                :key="record.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ record.name }}</p>
                  <p class="text-sm text-gray-500">{{ record.date }}</p>
                </div>
                <div class="flex items-center gap-3">
                  <div class="text-right">
                    <p class="font-semibold text-gray-900">{{ record.score }}分</p>
                    <p :class="['text-xs', getResultColor(record.result)]">{{ record.result }}</p>
                  </div>
                  <button class="text-blue-600 hover:text-blue-700 text-sm">查看详情</button>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 text-white">
            <h3 class="text-lg font-semibold mb-2">温馨提示</h3>
            <p class="text-sm opacity-90">
              测评结果仅供参考，不能作为诊断依据。如果您感到持续的心理困扰，建议及时寻求专业心理咨询师的帮助。
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Heart, Activity, Brain, Smile } from 'lucide-vue-next'

const assessments = ref([
  {
    id: 'anxiety',
    name: '焦虑自评量表',
    description: '评估您的焦虑水平',
    icon: Activity,
    iconColor: 'text-blue-600',
    duration: '5-10分钟',
    completed: false
  },
  {
    id: 'depression',
    name: '抑郁自评量表',
    description: '评估您的抑郁倾向',
    icon: Heart,
    iconColor: 'text-pink-600',
    duration: '5-10分钟',
    completed: false
  },
  {
    id: 'stress',
    name: '压力感知量表',
    description: '评估您的压力水平',
    icon: Brain,
    iconColor: 'text-purple-600',
    duration: '5-8分钟',
    completed: true
  },
  {
    id: 'wellbeing',
    name: '心理健康综合评估',
    description: '全面评估心理健康状况',
    icon: Smile,
    iconColor: 'text-green-600',
    duration: '15-20分钟',
    completed: false
  }
])

const historyRecords = ref([
  {
    id: '1',
    name: '压力感知量表',
    date: '2024-01-10',
    score: 45,
    result: '轻度压力'
  },
  {
    id: '2',
    name: '焦虑自评量表',
    date: '2024-01-05',
    score: 38,
    result: '正常'
  }
])

const getResultColor = (result: string) => {
  const colors: Record<string, string> = {
    '正常': 'text-green-600',
    '轻度压力': 'text-yellow-600',
    '中度压力': 'text-orange-600',
    '重度压力': 'text-red-600'
  }
  return colors[result] || 'text-gray-600'
}

const handleAssessmentClick = (assessment: any) => {
  alert(`功能开发中：${assessment.name}`)
}
</script>
