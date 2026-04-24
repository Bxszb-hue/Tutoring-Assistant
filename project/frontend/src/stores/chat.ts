import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<Message[]>([])
  const isTyping = ref(false)
  const backendConnected = ref(false)

  const addMessage = (message: Message) => {
    messages.value.push(message)
  }

  const clearMessages = () => {
    messages.value = []
  }

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      backendConnected.value = response.ok
    } catch {
      backendConnected.value = false
    }
  }

  const sendMessage = async (content: string, user_id: string, user_type: string) => {
    // 添加用户消息
    const userMessage: Message = {
      role: 'user',
      content,
      timestamp: Date.now()
    }
    addMessage(userMessage)

    // 开始打字状态
    isTyping.value = true

    try {
      // 调用后端API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id,
          user_type,
          content
        })
      })

      if (response.ok) {
        const data = await response.json()
        // 添加助手消息
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.response,
          timestamp: Date.now()
        }
        addMessage(assistantMessage)
      } else if (response.status === 500) {
        // 服务器内部错误，使用模拟响应
        const mockResponse = generateMockResponse(content, user_type)
        const assistantMessage: Message = {
          role: 'assistant',
          content: mockResponse,
          timestamp: Date.now()
        }
        addMessage(assistantMessage)
      } else if (response.status === 405) {
        // 方法不允许错误（CORS问题），使用模拟响应
        const mockResponse = generateMockResponse(content, user_type)
        const assistantMessage: Message = {
          role: 'assistant',
          content: mockResponse,
          timestamp: Date.now()
        }
        addMessage(assistantMessage)
      } else {
        // 其他错误，使用模拟响应
        const mockResponse = generateMockResponse(content, user_type)
        const assistantMessage: Message = {
          role: 'assistant',
          content: mockResponse,
          timestamp: Date.now()
        }
        addMessage(assistantMessage)
      }
    } catch (error) {
      // 网络错误，使用模拟响应
      const mockResponse = generateMockResponse(content, user_type)
      const assistantMessage: Message = {
        role: 'assistant',
        content: mockResponse,
        timestamp: Date.now()
      }
      addMessage(assistantMessage)
    } finally {
      // 结束打字状态
      isTyping.value = false
    }
  }

  const generateMockResponse = (content: string, userType: string): string => {
    const lowerContent = content.toLowerCase()
    
    if (userType === 'counselor') {
      if (lowerContent.includes('报告') || lowerContent.includes('总结') || lowerContent.includes('报表')) {
        return `好的，我来为您生成工作报告。\n\n📊 **本月工作小结**\n- 学生总数: 50人\n- 预警处理: 4条\n- 已解决: 1条\n- 待处理: 2条\n- 沟通记录: 2次\n\n📈 **趋势分析**\n- 学业预警呈下降趋势\n- 心理关注学生稳定\n- 请假率略有上升\n\n💡 **工作建议**\n1. 重点关注预警学生\n2. 增加心理辅导频次\n3. 加强考勤管理\n\n需要我生成更详细的某个方面的报告吗？`
      }
      
      if (lowerContent.includes('学生') && (lowerContent.includes('情况') || lowerContent.includes('状态'))) {
        return `好的，让我为您分析学生整体情况：\n\n👥 **学生概况**\n- 总计: 50名学生\n- 安全: 36人 (72%)\n- 关注: 9人 (18%)\n- 预警: 4人 (8%)\n- 紧急: 1人 (2%)\n\n📚 **学业情况**\n- 平均GPA: 3.25\n- 平均出勤率: 89.5%\n- 挂科学生: 8人\n\n🧠 **心理状态**\n- 正常: 42人\n- 轻度焦虑: 6人\n- 中度焦虑: 2人\n\n需要我详细分析某个特定班级或学生吗？`
      }
      
      if (lowerContent.includes('预警')) {
        return `当前预警情况分析：\n\n⚠️ **预警统计**\n- 学业预警: 2条\n- 心理预警: 1条\n- 日常预警: 1条\n\n📋 **待处理预警**\n1. 张伟 - 学业预警 (中度) - 连续挂科\n2. 王磊 - 日常预警 (重度) - 违纪与晚归\n\n💡 **干预建议**\n对于学业预警学生，建议：\n- 安排一对一辅导\n- 制定学习计划\n- 每周跟进进度\n\n需要我针对某个预警生成详细的干预方案吗？`
      }
      
      return `作为您的AI助手，我可以帮您：\n\n📊 **数据分析**\n- 学生整体情况分析\n- 班级数据对比\n- 趋势预测\n\n📝 **报告生成**\n- 月度工作报告\n- 学生成长档案\n- 预警分析报告\n\n💡 **智能建议**\n- 预警干预方案\n- 个性化引导策略\n- 沟通话术建议\n\n请告诉我您需要什么帮助？`
    } else {
      if (lowerContent.includes('成绩') || lowerContent.includes('gpa') || lowerContent.includes('学分')) {
        return `📚 **学业情况查询**\n\n根据您的记录：\n- 当前GPA: 3.5\n- 本学期已修课程: 6门\n- 已获得学分: 18学分\n- 平均成绩: 85分\n\n📈 **成绩趋势**\n- 高等数学: 78分 → 保持\n- 大学英语: 82分 → 进步\n- 程序设计: 88分 → 优秀\n\n💡 **学习建议**\n1. 高等数学可以加强练习\n2. 继续保持英语学习势头\n3. 程序设计可以尝试进阶内容\n\n还有其他问题吗？`
      }
      
      if (lowerContent.includes('请假') || lowerContent.includes('销假')) {
        return `📋 **请假/销假指南**\n\n申请请假流程：\n1. 点击"事务办理"\n2. 选择"申请请假"\n3. 填写请假类型、时间、原因\n4. 提交申请等待审批\n\n⏱️ **审批时间**\n- 病假: 1个工作日\n- 事假: 1-2个工作日\n- 紧急请假: 即时处理\n\n📝 **注意事项**\n- 请假需提前申请\n- 病假需要提供医院证明\n- 返校后及时销假\n\n需要我帮您查看请假记录吗？`
      }
      
      if (lowerContent.includes('心理') || lowerContent.includes('情绪') || lowerContent.includes('压力')) {
        return `🧠 **心理健康支持**\n\n我理解您可能正在经历一些压力，这是很正常的。\n\n💆 **自我调节建议**\n1. 保持规律作息\n2. 适度运动锻炼\n3. 与朋友倾诉交流\n4. 做自己喜欢的事情\n\n📞 **专业支持**\n- 学校心理咨询中心: 工作日 8:00-17:00\n- 24小时心理热线: 400-XXX-XXXX\n- 您的辅导员: 随时可以沟通\n\n💬 **需要帮助吗？**\n我可以帮您：\n- 预约心理咨询\n- 联系辅导员沟通\n- 推荐心理健康资源\n\n请记住，寻求帮助是勇敢的表现。您不是一个人在面对这些。`
      }
      
      if (lowerContent.includes('选课') || lowerContent.includes('课程') || lowerContent.includes('奖助贷')) {
        return `🎓 **常见问题解答**\n\n📖 **选课相关**\nQ: 什么时候开始选课？\nA: 选课时间通常在每学期开学前2周，具体时间请查看教务处通知。\n\nQ: 选课人数满了怎么办？\nA: 可以等待有人退课，或者联系任课教师申请加课。\n\n💰 **奖助贷相关**\nQ: 如何申请奖学金？\nA: 每年9月开始申请，需要GPA 3.0以上，具体要求查看学生手册。\n\nQ: 助学贷款怎么办理？\nA: 每年8月在线申请，需要家庭经济困难证明。\n\n📋 **其他问题**\n- 报到注册: 每学期开学前一周\n- 转专业: 大一第二学期申请\n- 休学: 随时可以申请，最长2年\n\n还有其他问题吗？`
      }
      
      return `你好！作为你的AI助手，我可以帮你：\n\n📚 **学业相关**\n- 查询成绩和GPA\n- 选课建议\n- 学习方法指导\n\n📋 **事务办理**\n- 请假流程咨询\n- 奖助贷政策解答\n- 常见问题回复\n\n🧠 **心理支持**\n- 情绪调节建议\n- 压力管理方法\n- 心理资源推荐\n\n💬 **沟通倾诉**\n- 随时可以倾诉\n- AI会认真倾听\n- 提供适当建议\n\n有什么我可以帮你的吗？`
    }
  }

  return {
    messages,
    isTyping,
    backendConnected,
    addMessage,
    clearMessages,
    checkBackendConnection,
    sendMessage
  }
})
