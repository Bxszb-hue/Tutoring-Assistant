import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface ChatMessage {
  id: string
  senderId: string
  senderName: string
  senderRole: 'counselor' | 'student'
  content: string
  timestamp: string
}

export interface ChatSession {
  id: string
  studentId: string
  studentName: string
  counselorId: string
  counselorName: string
  lastMessage?: string
  lastMessageTime?: string
  unreadCount: number
  messages: ChatMessage[]
}

const API_BASE = 'http://localhost:8005'

export const useCounselorChatStore = defineStore('counselorChat', () => {
  const sessions = ref<ChatSession[]>([])
  const activeSessionId = ref<string | null>(null)
  const loading = ref(false)

  const loadData = async (userId: string, userType: string) => {
    try {
      const response = await fetch(`${API_BASE}/chat/sessions/${userId}?user_type=${userType}`)
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success' && data.data) {
          sessions.value = data.data.map((s: any) => ({
            id: s.session_id,
            studentId: s.student_id,
            studentName: s.student_name,
            counselorId: s.counselor_id,
            counselorName: s.counselor_name,
            lastMessage: s.last_message,
            lastMessageTime: s.last_message_time,
            unreadCount: s.unread_count,
            messages: []
          }))
        }
      }
    } catch (error) {
      console.error('Failed to load chat sessions:', error)
      // 如果后端不可用，使用本地模拟数据
      loadMockData()
    }
  }

  const loadMockData = () => {
    const now = new Date().toISOString()
    
    sessions.value = [
      {
        id: 'chat_1',
        studentId: 'student_1',
        studentName: '张伟',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        lastMessage: '好的，谢谢老师！',
        lastMessageTime: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
        unreadCount: 0,
        messages: [
          {
            id: 'msg_1_1',
            senderId: 'student_1',
            senderName: '张伟',
            senderRole: 'student',
            content: '老师您好，我想咨询一下奖学金申请的事情。',
            timestamp: new Date(Date.now() - 45 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_1_2',
            senderId: 'counselor_1',
            senderName: '王辅导员',
            senderRole: 'counselor',
            content: '你好！奖学金申请通常在每年9月份开始，需要GPA达到3.0以上，并且没有违纪记录。你现在的GPA是多少？',
            timestamp: new Date(Date.now() - 40 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_1_3',
            senderId: 'student_1',
            senderName: '张伟',
            senderRole: 'student',
            content: '我现在GPA是3.5，没有违纪记录。需要准备哪些材料呢？',
            timestamp: new Date(Date.now() - 35 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_1_4',
            senderId: 'counselor_1',
            senderName: '王辅导员',
            senderRole: 'counselor',
            content: '需要准备：1. 申请表；2. 成绩单；3. 获奖证书复印件；4. 个人陈述。具体时间留意学院通知。',
            timestamp: new Date(Date.now() - 32 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_1_5',
            senderId: 'student_1',
            senderName: '张伟',
            senderRole: 'student',
            content: '好的，谢谢老师！',
            timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString()
          }
        ]
      },
      {
        id: 'chat_2',
        studentId: 'student_2',
        studentName: '李娜',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        lastMessage: '我最近学习压力很大...',
        lastMessageTime: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        unreadCount: 2,
        messages: [
          {
            id: 'msg_2_1',
            senderId: 'student_2',
            senderName: '李娜',
            senderRole: 'student',
            content: '老师，我想和您聊聊。',
            timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_2_2',
            senderId: 'counselor_1',
            senderName: '王辅导员',
            senderRole: 'counselor',
            content: '好的，李娜同学。有什么可以帮你的？',
            timestamp: new Date(Date.now() - 2.5 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_2_3',
            senderId: 'student_2',
            senderName: '李娜',
            senderRole: 'student',
            content: '我最近学习压力很大，感觉跟不上进度。',
            timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_2_4',
            senderId: 'student_2',
            senderName: '李娜',
            senderRole: 'student',
            content: '特别是高等数学，上课听不懂，作业也不会做。',
            timestamp: new Date(Date.now() - 1.5 * 60 * 60 * 1000).toISOString()
          }
        ]
      },
      {
        id: 'chat_3',
        studentId: 'student_3',
        studentName: '王磊',
        counselorId: 'counselor_1',
        counselorName: '王辅导员',
        lastMessage: '知道了，谢谢老师。',
        lastMessageTime: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        unreadCount: 0,
        messages: [
          {
            id: 'msg_3_1',
            senderId: 'counselor_1',
            senderName: '王辅导员',
            senderRole: 'counselor',
            content: '王磊同学，你最近的出勤情况不太好，有什么困难吗？',
            timestamp: new Date(Date.now() - 1.5 * 24 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_3_2',
            senderId: 'student_3',
            senderName: '王磊',
            senderRole: 'student',
            content: '老师，最近家里有点事，所以请假比较多。',
            timestamp: new Date(Date.now() - 1.2 * 24 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_3_3',
            senderId: 'counselor_1',
            senderName: '王辅导员',
            senderRole: 'counselor',
            content: '明白了。家里的事情处理完了吗？如果需要帮助可以告诉我。另外，你的几门课程成绩不太理想，需要多加努力。',
            timestamp: new Date(Date.now() - 1.1 * 24 * 60 * 60 * 1000).toISOString()
          },
          {
            id: 'msg_3_4',
            senderId: 'student_3',
            senderName: '王磊',
            senderRole: 'student',
            content: '知道了，谢谢老师。',
            timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
          }
        ]
      }
    ]
  }

  const activeSession = computed(() => {
    return sessions.value.find(s => s.id === activeSessionId.value) || null
  })

  const unreadTotal = computed(() => {
    return sessions.value.reduce((sum, s) => sum + s.unreadCount, 0)
  })

  const selectSession = async (sessionId: string) => {
    const session = sessions.value.find(s => s.id === sessionId)
    if (session) {
      activeSessionId.value = sessionId
      session.unreadCount = 0
      // 从后端加载消息
      await loadMessages(sessionId)
    }
  }

  const loadMessages = async (sessionId: string) => {
    try {
      const response = await fetch(`${API_BASE}/chat/messages/${sessionId}`)
      if (response.ok) {
        const data = await response.json()
        if (data.status === 'success' && data.data) {
          const session = sessions.value.find(s => s.id === sessionId)
          if (session) {
            session.messages = data.data.map((m: any) => ({
              id: String(m.id),
              senderId: m.sender_id,
              senderName: m.sender_name,
              senderRole: m.sender_role as 'counselor' | 'student',
              content: m.content,
              timestamp: m.created_at
            }))
          }
        }
      }
    } catch (error) {
      console.error('Failed to load messages:', error)
    }
  }

  const sendMessage = async (sessionId: string, content: string, senderId: string, senderName: string, senderRole: 'counselor' | 'student') => {
    const session = sessions.value.find(s => s.id === sessionId)
    if (session) {
      const newMessage: ChatMessage = {
        id: `msg_${Date.now()}`,
        senderId,
        senderName,
        senderRole,
        content,
        timestamp: new Date().toISOString()
      }
      session.messages.push(newMessage)
      session.lastMessage = content
      session.lastMessageTime = newMessage.timestamp

      // 发送到后端
      try {
        await fetch(`${API_BASE}/chat/message`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: sessionId,
            sender_id: senderId,
            sender_name: senderName,
            sender_role: senderRole,
            content: content
          })
        })
      } catch (error) {
        console.error('Failed to send message:', error)
      }
    }
  }

  const createSession = async (studentId: string, studentName: string, counselorId: string, counselorName: string) => {
    const sessionId = `chat_${Date.now()}`
    
    // 尝试从后端创建会话
    try {
      const response = await fetch(`${API_BASE}/chat/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          session_id: sessionId,
          student_id: studentId,
          student_name: studentName,
          counselor_id: counselorId,
          counselor_name: counselorName
        })
      })
      
      if (response.ok) {
        const data = await response.json()
        sessionId = data.session_id
      }
    } catch (error) {
      console.error('Failed to create session:', error)
    }

    const newSession: ChatSession = {
      id: sessionId,
      studentId,
      studentName,
      counselorId,
      counselorName,
      unreadCount: 0,
      messages: []
    }
    sessions.value.unshift(newSession)
    return newSession
  }

  let pollInterval: number | null = null

  const startPolling = () => {
    if (pollInterval) return
    pollInterval = window.setInterval(async () => {
      if (activeSessionId.value) {
        await loadMessages(activeSessionId.value)
      }
    }, 3000)
  }

  const stopPolling = () => {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
  }

  return {
    sessions,
    activeSessionId,
    activeSession,
    loading,
    unreadTotal,
    loadData,
    selectSession,
    sendMessage,
    createSession,
    startPolling,
    stopPolling
  }
})