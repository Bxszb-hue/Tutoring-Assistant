<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div v-if="!assessmentsStore.isCompleting" class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">自我测评</h1>
      </div>

      <div v-else class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <button @click="assessmentsStore.cancelAssessment()" class="flex items-center gap-2 text-gray-600 hover:text-gray-800">
            <ArrowLeft class="w-5 h-5" />
            <span>返回</span>
          </button>
          <h1 class="text-xl font-bold text-gray-900">{{ assessmentsStore.currentAssessment?.name }}</h1>
          <div class="text-gray-500 text-sm">{{ assessmentsStore.currentQuestionIndex + 1 }} / {{ assessmentsStore.currentAssessment?.questions.length }}</div>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div v-if="showResult" class="max-w-2xl mx-auto">
          <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
            <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white">
              <h2 class="text-xl font-bold mb-2">测评完成</h2>
              <p class="text-blue-100">{{ assessmentsStore.currentAssessment?.name }}</p>
            </div>
            <div class="p-6">
              <div class="text-center mb-6">
                <div :class="['text-6xl font-bold mb-2', resultColor]">{{ finalScore }}</div>
                <div :class="['text-lg font-semibold', resultColor]">{{ finalResult }}</div>
              </div>
              <div class="bg-gray-50 rounded-lg p-4 mb-6">
                <p class="text-gray-700">{{ finalResultDescription }}</p>
              </div>
              <div class="space-y-3">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div class="flex items-center gap-2 mb-2">
                    <Heart class="w-5 h-5 text-green-600" />
                    <span class="font-medium text-green-800">自我调节建议</span>
                  </div>
                  <ul class="text-sm text-green-700 space-y-1">
                    <li>• 保持规律作息，保证充足睡眠</li>
                    <li>• 适度运动，释放压力</li>
                    <li>• 与朋友家人倾诉交流</li>
                    <li>• 培养兴趣爱好，放松心情</li>
                  </ul>
                </div>
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div class="flex items-center gap-2 mb-2">
                    <Phone class="w-5 h-5 text-blue-600" />
                    <span class="font-medium text-blue-800">专业帮助</span>
                  </div>
                  <p class="text-sm text-blue-700">
                    如需进一步帮助，请联系学校心理咨询中心（电话：0123-4567890）或拨打24小时心理热线：400-161-9995
                  </p>
                </div>
              </div>
              <button
                @click="handleBackToList"
                class="w-full mt-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium transition-colors"
              >
                返回测评列表
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="assessmentsStore.isCompleting && assessmentsStore.currentQuestion" class="max-w-2xl mx-auto">
          <div class="bg-white rounded-xl border border-gray-100 overflow-hidden">
            <div class="bg-gray-50 px-6 py-3">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm text-gray-500">完成进度</span>
                <span class="text-sm font-medium text-gray-700">{{ Math.round(assessmentsStore.progress) }}%</span>
              </div>
              <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-600 transition-all duration-300"
                  :style="{ width: `${assessmentsStore.progress}%` }"
                ></div>
              </div>
            </div>

            <div class="p-6">
              <div class="mb-6">
                <span class="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full mb-4">
                  第 {{ assessmentsStore.currentQuestionIndex + 1 }} 题
                </span>
                <h3 class="text-xl font-semibold text-gray-900">
                  {{ assessmentsStore.currentQuestion?.text }}
                </h3>
              </div>

              <div class="space-y-3">
                <button
                  v-for="(option, index) in assessmentsStore.currentQuestion?.options"
                  :key="index"
                  @click="assessmentsStore.answerQuestion(assessmentsStore.currentQuestion?.scores[index] || 0)"
                  class="w-full p-4 text-left border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all"
                >
                  <div class="flex items-center gap-3">
                    <span :class="[
                      'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium',
                      'bg-gray-100 text-gray-600 hover:bg-blue-100 hover:text-blue-600'
                    ]">
                      {{ index + 1 }}
                    </span>
                    <span class="text-gray-700">{{ option }}</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="max-w-7xl mx-auto space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">心理健康测评</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div
                v-for="assessment in assessmentsStore.assessments"
                :key="assessment.id"
                class="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                @click="handleAssessmentClick(assessment)"
              >
                <div class="flex items-center gap-3 mb-2">
                  <component :is="getIcon(assessment.id)" :class="['w-5 h-5', getIconColor(assessment.id)]" />
                  <h4 class="font-medium text-gray-900">{{ assessment.name }}</h4>
                </div>
                <p class="text-sm text-gray-500 mb-2">{{ assessment.description }}</p>
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-400">预计用时：{{ assessment.duration }}</span>
                  <span :class="[
                    'text-xs font-medium',
                    isAssessmentCompleted(assessment.id) ? 'text-green-600' : 'text-blue-600'
                  ]">
                    {{ isAssessmentCompleted(assessment.id) ? '已完成' : '开始测评' }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">测评历史</h3>
            <div v-if="assessmentsStore.records.length > 0" class="space-y-3">
              <div
                v-for="record in assessmentsStore.records"
                :key="record.id"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ record.assessmentName }}</p>
                  <p class="text-sm text-gray-500">{{ record.date }}</p>
                </div>
                <div class="flex items-center gap-3">
                  <div class="text-right">
                    <p class="font-semibold text-gray-900">{{ record.score }}{{ isScoreInteger(record.score) ? '' : '' }}</p>
                    <p :class="['text-xs', getResultColorClass(record.result)]">{{ record.result }}</p>
                  </div>
                  <button
                    @click="viewRecordDetail(record)"
                    class="text-blue-600 hover:text-blue-700 text-sm"
                  >
                    查看详情
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8">
              <FileText class="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p class="text-gray-500">暂无测评记录</p>
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

    <Modal
      v-if="detailModalVisible"
      :visible="detailModalVisible"
      :title="selectedRecord?.assessmentName"
      :show-footer="true"
      :show-cancel="false"
      confirm-text="关闭"
      @close="detailModalVisible = false"
      @confirm="detailModalVisible = false"
    >
      <div v-if="selectedRecord" class="space-y-4">
        <div class="text-center py-4">
          <div :class="['text-5xl font-bold mb-2', getResultColorClass(selectedRecord.result)]">{{ selectedRecord.score }}{{ isScoreInteger(selectedRecord.score) ? '' : '' }}</div>
          <div :class="['text-lg font-semibold', getResultColorClass(selectedRecord.result)]">{{ selectedRecord.result }}</div>
        </div>
        <div class="bg-gray-50 rounded-lg p-4">
          <p class="text-gray-700">{{ selectedRecord.resultDescription }}</p>
        </div>
        <div class="text-sm text-gray-500">
          <p>测评日期：{{ selectedRecord.date }}</p>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Heart, Activity, Brain, Smile, ArrowLeft, Phone, FileText } from 'lucide-vue-next'
import { useAssessmentsStore } from '@/stores/assessments'
import Modal from '@/components/Modal.vue'
import type { Assessment, AssessmentRecord } from '@/stores/assessments'

const assessmentsStore = useAssessmentsStore()

const showResult = ref(false)
const detailModalVisible = ref(false)
const selectedRecord = ref<AssessmentRecord | null>(null)

const finalScore = computed(() => {
  const latestRecord = assessmentsStore.records[0]
  return latestRecord?.score || 0
})

const finalResult = computed(() => {
  const latestRecord = assessmentsStore.records[0]
  return latestRecord?.result || '未评估'
})

const finalResultDescription = computed(() => {
  const latestRecord = assessmentsStore.records[0]
  return latestRecord?.resultDescription || ''
})

const resultColor = computed(() => {
  return getResultColorClass(finalResult.value)
})

const getIcon = (id: string) => {
  const icons: Record<string, any> = {
    anxiety: Activity,
    depression: Heart,
    stress: Brain,
    wellbeing: Smile
  }
  return icons[id] || Heart
}

const getIconColor = (id: string) => {
  const colors: Record<string, string> = {
    anxiety: 'text-blue-600',
    depression: 'text-pink-600',
    stress: 'text-purple-600',
    wellbeing: 'text-green-600'
  }
  return colors[id] || 'text-gray-600'
}

const getResultColorClass = (result: string) => {
  const colors: Record<string, string> = {
    '正常': 'text-green-600',
    '优秀': 'text-green-600',
    '良好': 'text-blue-600',
    '轻度焦虑': 'text-yellow-600',
    '轻度压力': 'text-yellow-600',
    '一般': 'text-yellow-600',
    '中度焦虑': 'text-orange-600',
    '中度抑郁': 'text-orange-600',
    '中度压力': 'text-orange-600',
    '需关注': 'text-orange-600',
    '重度焦虑': 'text-red-600',
    '重度抑郁': 'text-red-600',
    '重度压力': 'text-red-600'
  }
  return colors[result] || 'text-gray-600'
}

const isAssessmentCompleted = (id: string) => {
  return assessmentsStore.records.some(r => r.assessmentId === id)
}

const isScoreInteger = (score: number) => {
  return Number.isInteger(score)
}

const handleAssessmentClick = (assessment: Assessment) => {
  showResult.value = false
  assessmentsStore.startAssessment(assessment.id)
}

const handleBackToList = () => {
  showResult.value = false
  assessmentsStore.cancelAssessment()
}

const viewRecordDetail = (record: AssessmentRecord) => {
  selectedRecord.value = record
  detailModalVisible.value = true
}

onMounted(() => {
  assessmentsStore.loadAssessments()
})

watch(() => [assessmentsStore.isCompleting, assessmentsStore.currentAssessment], ([isCompleting, currentAssessment]) => {
  if (!isCompleting && currentAssessment) {
    showResult.value = true
  }
})
</script>