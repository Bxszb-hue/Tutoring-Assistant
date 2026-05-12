import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Question {
  id: string
  text: string
  options: string[]
  scores: number[]
}

export interface Assessment {
  id: string
  name: string
  description: string
  duration: string
  questions: Question[]
  scoringMethod: 'sum' | 'average'
  resultInterpretation: Record<number | string, { range: [number, number] | 'default'; label: string; color: string; description: string }>
}

export interface AssessmentRecord {
  id: string
  assessmentId: string
  assessmentName: string
  date: string
  score: number
  result: string
  resultDescription: string
  answers: number[]
}

const RECORDS_STORAGE_KEY = 'assessment_records'

export const useAssessmentsStore = defineStore('assessments', () => {
  const assessments = ref<Assessment[]>([])
  const currentAssessment = ref<Assessment | null>(null)
  const currentQuestionIndex = ref(0)
  const answers = ref<number[]>([])
  const isCompleting = ref(false)
  const records = ref<AssessmentRecord[]>([])

  const saveRecordsToStorage = () => {
    localStorage.setItem(RECORDS_STORAGE_KEY, JSON.stringify(records.value))
  }

  const loadRecordsFromStorage = () => {
    const saved = localStorage.getItem(RECORDS_STORAGE_KEY)
    if (saved) {
      try {
        records.value = JSON.parse(saved)
        return true
      } catch {
        return false
      }
    }
    return false
  }

  const loadAssessments = () => {
    assessments.value = [
      {
        id: 'anxiety',
        name: '焦虑自评量表',
        description: '评估您的焦虑水平',
        duration: '5-10分钟',
        scoringMethod: 'sum',
        questions: [
          { id: 'q1', text: '我觉得比平常容易紧张和着急', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q2', text: '我无缘无故地感到害怕', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q3', text: '我容易心里烦乱或觉得惊恐', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q4', text: '我觉得我可能将要发疯', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q5', text: '我觉得一切都很好，也不会发生什么不幸', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q6', text: '我手脚发抖打颤', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q7', text: '我因为头痛、颈痛和背痛而苦恼', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q8', text: '我感觉容易衰弱和疲乏', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q9', text: '我觉得心平气和，并且容易安静坐着', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q10', text: '我觉得心跳得很快', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q11', text: '我因为一阵阵头晕而苦恼', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q12', text: '我有晕倒发作，或觉得要晕倒似的', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q13', text: '我吸气呼气都感到很容易', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q14', text: '我的手脚麻木和刺痛', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q15', text: '我因为胃痛和消化不良而苦恼', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q16', text: '我常常要小便', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q17', text: '我的手常常是干燥温暖的', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q18', text: '我脸红发热', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q19', text: '我容易入睡并且一夜睡得很好', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q20', text: '我做恶梦', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] }
        ],
        resultInterpretation: {
          1: { range: [20, 29], label: '正常', color: 'text-green-600', description: '您的焦虑水平正常，保持良好的心态和生活习惯。' },
          2: { range: [30, 39], label: '轻度焦虑', color: 'text-yellow-600', description: '您有轻度焦虑倾向，建议适当放松，进行一些舒缓压力的活动。' },
          3: { range: [40, 49], label: '中度焦虑', color: 'text-orange-600', description: '您有中度焦虑，建议寻求朋友或家人的支持，必要时咨询专业心理师。' },
          4: { range: [50, 80], label: '重度焦虑', color: 'text-red-600', description: '您可能存在重度焦虑，建议尽快联系学校心理咨询中心或专业医疗机构进行评估。' },
          default: { range: 'default', label: '未评估', color: 'text-gray-600', description: '' }
        }
      },
      {
        id: 'depression',
        name: '抑郁自评量表',
        description: '评估您的抑郁倾向',
        duration: '5-10分钟',
        scoringMethod: 'sum',
        questions: [
          { id: 'q1', text: '我感到情绪沮丧，郁闷', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q2', text: '我感到早晨心情最好', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q3', text: '我要哭或想哭', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q4', text: '我夜间睡眠不好', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q5', text: '我吃饭像平时一样多', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q6', text: '我的性功能正常', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q7', text: '我感到体重减轻', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q8', text: '我为便秘烦恼', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q9', text: '我的心跳比平时快', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q10', text: '我无故感到疲劳', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q11', text: '我的头脑像往常一样清楚', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q12', text: '我做事情像平时一样不感到困难', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q13', text: '我坐卧不安，难以保持平静', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q14', text: '我对未来感到有希望', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q15', text: '我比平时更容易激怒', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] },
          { id: 'q16', text: '我觉得决定什么事很容易', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q17', text: '我感到自己是有用的和不可缺少的人', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q18', text: '我的生活很有意义', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q19', text: '我仍然喜爱自己平时喜爱的东西', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [4, 3, 2, 1] },
          { id: 'q20', text: '我认为如果我死了别人会生活得更好', options: ['没有或很少时间', '小部分时间', '相当多时间', '绝大部分或全部时间'], scores: [1, 2, 3, 4] }
        ],
        resultInterpretation: {
          1: { range: [20, 29], label: '正常', color: 'text-green-600', description: '您的情绪状态正常，保持积极的生活态度。' },
          2: { range: [30, 39], label: '轻度抑郁', color: 'text-yellow-600', description: '您有轻度抑郁倾向，建议多与他人交流，保持积极的生活节奏。' },
          3: { range: [40, 59], label: '中度抑郁', color: 'text-orange-600', description: '您有中度抑郁，建议寻求身边人的支持，考虑专业心理咨询。' },
          4: { range: [60, 80], label: '重度抑郁', color: 'text-red-600', description: '您可能存在重度抑郁，强烈建议立即联系学校心理咨询中心或专业医疗机构。' },
          default: { range: 'default', label: '未评估', color: 'text-gray-600', description: '' }
        }
      },
      {
        id: 'stress',
        name: '压力感知量表',
        description: '评估您的压力水平',
        duration: '5-8分钟',
        scoringMethod: 'average',
        questions: [
          { id: 'q1', text: '您感觉自己无法控制生活中重要的事情吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [1, 2, 3, 4, 5] },
          { id: 'q2', text: '您感觉自己对处理个人问题有信心吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] },
          { id: 'q3', text: '您觉得事情按您的方式进行吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] },
          { id: 'q4', text: '您感觉无法应对您必须做的所有事情吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [1, 2, 3, 4, 5] },
          { id: 'q5', text: '您感觉自己能掌控生活中重要事情的方向吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] },
          { id: 'q6', text: '您感觉事情正在变得超出您的控制吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [1, 2, 3, 4, 5] },
          { id: 'q7', text: '您对自己处理问题的能力有信心吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] },
          { id: 'q8', text: '您感觉事情堆积如山，让您无法克服吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [1, 2, 3, 4, 5] },
          { id: 'q9', text: '您感觉自己能成功处理生活中的变化吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] },
          { id: 'q10', text: '您感觉自己有能力处理生活中遇到的困难吗？', options: ['从不', '几乎不', '有时', '经常', '总是'], scores: [5, 4, 3, 2, 1] }
        ],
        resultInterpretation: {
          1: { range: [1, 2], label: '正常', color: 'text-green-600', description: '您的压力水平正常，能较好地应对生活中的挑战。' },
          2: { range: [2.1, 3], label: '轻度压力', color: 'text-yellow-600', description: '您有轻度压力，建议适当放松，进行一些减压活动。' },
          3: { range: [3.1, 4], label: '中度压力', color: 'text-orange-600', description: '您有中度压力，建议调整生活节奏，寻求适当的支持。' },
          4: { range: [4.1, 5], label: '重度压力', color: 'text-red-600', description: '您承受着较大压力，建议及时调整，必要时寻求专业帮助。' },
          default: { range: 'default', label: '未评估', color: 'text-gray-600', description: '' }
        }
      },
      {
        id: 'wellbeing',
        name: '心理健康综合评估',
        description: '全面评估心理健康状况',
        duration: '15-20分钟',
        scoringMethod: 'average',
        questions: [
          { id: 'q1', text: '在过去两周内，您对自己的整体健康状况满意吗？', options: ['非常不满意', '不太满意', '一般', '比较满意', '非常满意'], scores: [1, 2, 3, 4, 5] },
          { id: 'q2', text: '您能集中注意力完成日常任务吗？', options: ['完全不能', '不太能', '一般', '比较能', '完全能'], scores: [1, 2, 3, 4, 5] },
          { id: 'q3', text: '您觉得自己有足够的精力应对日常活动吗？', options: ['完全没有', '不太有', '一般', '比较有', '完全有'], scores: [1, 2, 3, 4, 5] },
          { id: 'q4', text: '您与家人和朋友的关系如何？', options: ['非常差', '不太好', '一般', '比较好', '非常好'], scores: [1, 2, 3, 4, 5] },
          { id: 'q5', text: '您对未来感到乐观吗？', options: ['完全不乐观', '不太乐观', '一般', '比较乐观', '非常乐观'], scores: [1, 2, 3, 4, 5] },
          { id: 'q6', text: '您能有效地管理自己的情绪吗？', options: ['完全不能', '不太能', '一般', '比较能', '完全能'], scores: [1, 2, 3, 4, 5] },
          { id: 'q7', text: '您的睡眠质量如何？', options: ['非常差', '不太好', '一般', '比较好', '非常好'], scores: [1, 2, 3, 4, 5] },
          { id: 'q8', text: '您对自己的学习/工作表现满意吗？', options: ['非常不满意', '不太满意', '一般', '比较满意', '非常满意'], scores: [1, 2, 3, 4, 5] },
          { id: 'q9', text: '您感觉自己能够应对生活中的挑战吗？', options: ['完全不能', '不太能', '一般', '比较能', '完全能'], scores: [1, 2, 3, 4, 5] },
          { id: 'q10', text: '您对生活总体感到满意吗？', options: ['非常不满意', '不太满意', '一般', '比较满意', '非常满意'], scores: [1, 2, 3, 4, 5] },
          { id: 'q11', text: '您有足够的社交支持吗？', options: ['完全没有', '不太够', '一般', '比较够', '完全够'], scores: [1, 2, 3, 4, 5] },
          { id: 'q12', text: '您能保持积极的心态吗？', options: ['完全不能', '不太能', '一般', '比较能', '完全能'], scores: [1, 2, 3, 4, 5] }
        ],
        resultInterpretation: {
          1: { range: [4.1, 5], label: '优秀', color: 'text-green-600', description: '您的心理健康状况优秀，继续保持良好的生活习惯和心态。' },
          2: { range: [3.1, 4], label: '良好', color: 'text-blue-600', description: '您的心理健康状况良好，建议继续保持积极的生活态度。' },
          3: { range: [2.1, 3], label: '一般', color: 'text-yellow-600', description: '您的心理健康状况一般，建议关注自身状态，适当调整。' },
          4: { range: [1, 2], label: '需关注', color: 'text-orange-600', description: '您的心理健康需要关注，建议寻求支持和帮助。' },
          default: { range: 'default', label: '未评估', color: 'text-gray-600', description: '' }
        }
      }
    ]

    if (!loadRecordsFromStorage()) {
      records.value = [
        { id: '1', assessmentId: 'stress', assessmentName: '压力感知量表', date: '2024-01-10', score: 2.8, result: '轻度压力', resultDescription: '您有轻度压力，建议适当放松，进行一些减压活动。', answers: [3, 4, 3, 2, 4, 2, 4, 3, 4, 3] },
        { id: '2', assessmentId: 'anxiety', assessmentName: '焦虑自评量表', date: '2024-01-05', score: 38, result: '正常', resultDescription: '您的焦虑水平正常，保持良好的心态和生活习惯。', answers: [1, 2, 1, 1, 4, 2, 1, 2, 4, 1, 1, 1, 4, 1, 1, 1, 4, 1, 4, 1] }
      ]
      saveRecordsToStorage()
    }
  }

  const currentQuestion = computed(() => {
    if (!currentAssessment.value) return null
    return currentAssessment.value.questions[currentQuestionIndex.value]
  })

  const progress = computed(() => {
    if (!currentAssessment.value) return 0
    return ((currentQuestionIndex.value + 1) / currentAssessment.value.questions.length) * 100
  })

  const startAssessment = (assessmentId: string) => {
    const assessment = assessments.value.find(a => a.id === assessmentId)
    if (assessment) {
      currentAssessment.value = assessment
      currentQuestionIndex.value = 0
      answers.value = []
      isCompleting.value = true
    }
  }

  const answerQuestion = (score: number) => {
    answers.value.push(score)
    if (currentQuestionIndex.value < (currentAssessment.value?.questions.length || 0) - 1) {
      currentQuestionIndex.value++
    } else {
      completeAssessment()
    }
  }

  const completeAssessment = () => {
    if (!currentAssessment.value) return

    let score: number
    if (currentAssessment.value.scoringMethod === 'sum') {
      score = answers.value.reduce((a, b) => a + b, 0)
    } else {
      score = parseFloat((answers.value.reduce((a, b) => a + b, 0) / answers.value.length).toFixed(1))
    }

    let result = '未评估'
    let resultDescription = ''
    let resultColor = 'text-gray-600'

    for (const key of Object.keys(currentAssessment.value.resultInterpretation)) {
      const interpretation = currentAssessment.value.resultInterpretation[key]
      if (interpretation.range !== 'default') {
        const [min, max] = interpretation.range as [number, number]
        if (score >= min && score <= max) {
          result = interpretation.label
          resultDescription = interpretation.description
          resultColor = interpretation.color
          break
        }
      }
    }

    const record: AssessmentRecord = {
      id: `record_${Date.now()}`,
      assessmentId: currentAssessment.value.id,
      assessmentName: currentAssessment.value.name,
      date: new Date().toISOString().split('T')[0],
      score,
      result,
      resultDescription,
      answers: [...answers.value]
    }

    records.value.unshift(record)
    saveRecordsToStorage()
    isCompleting.value = false
  }

  const getAssessmentById = (id: string) => {
    return assessments.value.find(a => a.id === id)
  }

  const getRecordById = (id: string) => {
    return records.value.find(r => r.id === id)
  }

  const cancelAssessment = () => {
    currentAssessment.value = null
    currentQuestionIndex.value = 0
    answers.value = []
    isCompleting.value = false
  }

  return {
    assessments,
    currentAssessment,
    currentQuestion,
    currentQuestionIndex,
    answers,
    isCompleting,
    records,
    progress,
    loadAssessments,
    startAssessment,
    answerQuestion,
    cancelAssessment,
    getAssessmentById,
    getRecordById
  }
})