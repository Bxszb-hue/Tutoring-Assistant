<template>
  <div class="flex flex-col h-full bg-white">
    <div class="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-600 to-purple-600">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
          <Sparkles class="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 class="text-white font-semibold">{{ title }}</h3>
          <p class="text-blue-100 text-xs">{{ subtitle }}</p>
        </div>
      </div>
    </div>

    <div v-if="!backendConnected" class="p-4 bg-yellow-50 border-b border-yellow-200">
      <div class="flex items-start gap-2">
        <AlertCircle class="w-4 h-4 text-yellow-600 mt-0.5 flex-shrink-0" />
        <div class="flex-1">
          <p class="text-sm text-yellow-800 font-medium">后端服务未连接</p>
          <p class="text-xs text-yellow-700 mt-1">正在使用模拟响应。请启动后端服务以体验完整功能。</p>
        </div>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center text-gray-500">
        <Sparkles class="w-12 h-12 mx-auto mb-3 text-blue-400" />
        <p class="font-medium text-gray-700 mb-1">你好！我是AI助手</p>
        <p class="text-sm">{{ welcomeMessage }}</p>
        <div v-if="suggestions.length > 0" class="mt-6 space-y-2">
          <p class="text-xs text-gray-500 mb-2">试试问这些问题：</p>
          <button
            v-for="(suggestion, index) in suggestions"
            :key="index"
            @click="sendMessage(suggestion)"
            class="block w-full text-left px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm text-gray-700 transition-colors"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>
      
      <div v-else>
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'flex gap-3',
            message.role === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <div
            v-if="message.role === 'assistant'"
            class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0"
          >
            <Sparkles class="w-4 h-4 text-white" />
          </div>
          
          <div
            :class="[
              'max-w-[80%]',
              message.role === 'user' ? 'order-2' : 'order-1'
            ]"
          >
            <div
              :class="[
                'px-4 py-3 rounded-2xl',
                message.role === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-sm'
                  : 'bg-gray-100 text-gray-900 rounded-tl-sm'
              ]"
            >
              <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
            </div>
            <p class="text-xs text-gray-400 mt-1">
              {{ formatTime(message.timestamp) }}
            </p>
          </div>
          
          <div
            v-if="message.role === 'user'"
            class="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center flex-shrink-0 order-1"
          >
            <span class="text-white text-xs font-medium">{{ userInitial }}</span>
          </div>
        </div>
        
        <div v-if="isTyping" class="flex gap-3">
          <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <Sparkles class="w-4 h-4 text-white" />
          </div>
          <div class="px-4 py-3 bg-gray-100 rounded-2xl rounded-tl-sm">
            <div class="flex gap-1">
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="p-4 border-t border-gray-200">
      <div class="flex gap-2">
        <input
          v-model="inputMessage"
          @keydown.enter.prevent="handleSend"
          type="text"
          :placeholder="inputPlaceholder"
          class="flex-1 px-4 py-2 bg-gray-100 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          @click="handleSend"
          :disabled="!inputMessage.trim() || isTyping"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-xl transition-colors"
        >
          <Send class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { Sparkles, Send, AlertCircle } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  title?: string
  subtitle?: string
  welcomeMessage?: string
  inputPlaceholder?: string
  suggestions?: string[]
  context?: any
  role?: 'counselor' | 'student'
}>()

const authStore = useAuthStore()

const messages = ref<Array<{
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}>>([])
const inputMessage = ref('')
const isTyping = ref(false)
const backendConnected = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const title = computed(() => props.title || 'AI助手')
const subtitle = computed(() => props.subtitle || '智能辅助')
const welcomeMessage = computed(() => props.welcomeMessage || '有什么我可以帮你的吗？')
const inputPlaceholder = computed(() => props.inputPlaceholder || '输入消息...')
const suggestions = computed(() => props.suggestions || [])

const userInitial = computed(() => {
  return authStore.currentUser?.name?.charAt(0) || 'U'
})

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleQuickAction = (event: any) => {
  if (event.detail) {
    inputMessage.value = event.detail
    handleSend()
  }
}

onMounted(async () => {
  window.addEventListener('quickAction', handleQuickAction)
  try {
    const response = await fetch('http://localhost:8000/health')
    backendConnected.value = response.ok
  } catch {
    backendConnected.value = false
  }
})

onUnmounted(() => {
  window.removeEventListener('quickAction', handleQuickAction)
})

const handleSend = () => {
  sendMessage(inputMessage.value)
}

const sendMessage = async (text?: string) => {
  const message = text || inputMessage.value
  if (!message.trim() || isTyping.value) return
  
  messages.value.push({
    role: 'user',
    content: message,
    timestamp: Date.now()
  })
  
  inputMessage.value = ''
  scrollToBottom()
  
  isTyping.value = true
  scrollToBottom()
  
  try {
    let response = ''
    
    if (backendConnected.value) {
      try {
        const apiResponse = await fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: message,
            role: props.role || 'student',
            user_id: authStore.currentUser?.id
          })
        })
        
        if (apiResponse.ok) {
          const data = await apiResponse.json()
          response = data.response
        } else {
          throw new Error('API请求失败')
        }
      } catch (error) {
        console.error('API调用失败，使用模拟响应:', error)
        response = await generateMockResponse(message)
      }
    } else {
      response = await generateMockResponse(message)
    }
    
    messages.value.push({
      role: 'assistant',
      content: response,
      timestamp: Date.now()
    })
  } catch (error) {
    console.error('发送消息失败:', error)
  }
  
  isTyping.value = false
  scrollToBottom()
}

const generateMockResponse = async (userMessage: string): Promise<string> => {
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000))
  
  const lowerMessage = userMessage.toLowerCase()
  
  if (props.role === 'counselor') {
    if (lowerMessage.includes('报告') || lowerMessage.includes('总结') || lowerMessage.includes('报表')) {
      return `好的，我来为您生成工作报告。

📊 **本月工作小结**
- 学生总数: 50人
- 预警处理: 4条
- 已解决: 1条
- 待处理: 2条
- 沟通记录: 2次

📈 **趋势分析**
- 学业预警呈下降趋势
- 心理关注学生稳定
- 请假率略有上升

💡 **工作建议**
1. 重点关注预警学生
2. 增加心理辅导频次
3. 加强考勤管理

需要我生成更详细的某个方面的报告吗？`
    }
    
    if (lowerMessage.includes('学生') && (lowerMessage.includes('情况') || lowerMessage.includes('状态'))) {
      return `好的，让我为您分析学生整体情况：

👥 **学生概况**
- 总计: 50名学生
- 安全: 36人 (72%)
- 关注: 9人 (18%)
- 预警: 4人 (8%)
- 紧急: 1人 (2%)

📚 **学业情况**
- 平均GPA: 3.25
- 平均出勤率: 89.5%
- 挂科学生: 8人

🧠 **心理状态**
- 正常: 42人
- 轻度焦虑: 6人
- 中度焦虑: 2人

需要我详细分析某个特定班级或学生吗？`
    }
    
    if (lowerMessage.includes('预警')) {
      return `当前预警情况分析：

⚠️ **预警统计**
- 学业预警: 2条
- 心理预警: 1条
- 日常预警: 1条

📋 **待处理预警**
1. 张伟 - 学业预警 (中度) - 连续挂科
2. 王磊 - 日常预警 (重度) - 违纪与晚归

💡 **干预建议**
对于学业预警学生，建议：
- 安排一对一辅导
- 制定学习计划
- 每周跟进进度

需要我针对某个预警生成详细的干预方案吗？`
    }
    
    return `作为您的AI助手，我可以帮您：

📊 **数据分析**
- 学生整体情况分析
- 班级数据对比
- 趋势预测

📝 **报告生成**
- 月度工作报告
- 学生成长档案
- 预警分析报告

💡 **智能建议**
- 预警干预方案
- 个性化引导策略
- 沟通话术建议

请告诉我您需要什么帮助？`
  } else {
    if (lowerMessage.includes('成绩') || lowerMessage.includes('gpa') || lowerMessage.includes('学分')) {
      return `📚 **学业情况查询**

根据您的记录：
- 当前GPA: 3.5
- 本学期已修课程: 6门
- 已获得学分: 18学分
- 平均成绩: 85分

📈 **成绩趋势**
- 高等数学: 78分 → 保持
- 大学英语: 82分 → 进步
- 程序设计: 88分 → 优秀

💡 **学习建议**
1. 高等数学可以加强练习
2. 继续保持英语学习势头
3. 程序设计可以尝试进阶内容

还有其他问题吗？`
    }
    
    if (lowerMessage.includes('请假') || lowerMessage.includes('销假')) {
      return `📋 **请假/销假指南**

申请请假流程：
1. 点击"事务办理"
2. 选择"申请请假"
3. 填写请假类型、时间、原因
4. 提交申请等待审批

⏱️ **审批时间**
- 病假: 1个工作日
- 事假: 1-2个工作日
- 紧急请假: 即时处理

📝 **注意事项**
- 请假需提前申请
- 病假需要提供医院证明
- 返校后及时销假

需要我帮您查看请假记录吗？`
    }
    
    if (lowerMessage.includes('心理') || lowerMessage.includes('情绪') || lowerMessage.includes('压力')) {
      return `🧠 **心理健康支持**

我理解您可能正在经历一些压力，这是很正常的。

💆 **自我调节建议**
1. 保持规律作息
2. 适度运动锻炼
3. 与朋友倾诉交流
4. 做自己喜欢的事情

📞 **专业支持**
- 学校心理咨询中心: 工作日 8:00-17:00
- 24小时心理热线: 400-XXX-XXXX
- 您的辅导员: 随时可以沟通

💬 **需要帮助吗？**
我可以帮您：
- 预约心理咨询
- 联系辅导员沟通
- 推荐心理健康资源

请记住，寻求帮助是勇敢的表现。您不是一个人在面对这些。`
    }
    
    if (lowerMessage.includes('选课') || lowerMessage.includes('课程') || lowerMessage.includes('奖助贷')) {
      return `🎓 **常见问题解答**

📖 **选课相关**
Q: 什么时候开始选课？
A: 选课时间通常在每学期开学前2周，具体时间请查看教务处通知。

Q: 选课人数满了怎么办？
A: 可以等待有人退课，或者联系任课教师申请加课。

💰 **奖助贷相关**
Q: 如何申请奖学金？
A: 每年9月开始申请，需要GPA 3.0以上，具体要求查看学生手册。

Q: 助学贷款怎么办理？
A: 每年8月在线申请，需要家庭经济困难证明。

📋 **其他问题**
- 报到注册: 每学期开学前一周
- 转专业: 大一第二学期申请
- 休学: 随时可以申请，最长2年

还有其他问题吗？`
    }
    
    return `你好！作为你的AI助手，我可以帮你：

📚 **学业相关**
- 查询成绩和GPA
- 选课建议
- 学习方法指导

📋 **事务办理**
- 请假流程咨询
- 奖助贷政策解答
- 常见问题回复

🧠 **心理支持**
- 情绪调节建议
- 压力管理方法
- 心理资源推荐

💬 **沟通倾诉**
- 随时可以倾诉
- AI会认真倾听
- 提供适当建议

有什么我可以帮你的吗？`
  }
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })
</script>
