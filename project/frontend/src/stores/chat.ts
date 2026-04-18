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
        // 服务器内部错误
        const errorMessage: Message = {
          role: 'assistant',
          content: '服务器内部错误，请稍后再试。\n\n**提示：** 请确保后端服务已启动，并且所有依赖已安装。\n\n**启动后端服务步骤：**\n1. 确保已安装Python 3.8+\n2. 安装依赖：`pip install -r requirements.txt`\n3. 启动服务：`uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload`',
          timestamp: Date.now()
        }
        addMessage(errorMessage)
      } else if (response.status === 405) {
        // 方法不允许错误（CORS问题）
        const errorMessage: Message = {
          role: 'assistant',
          content: '服务器拒绝了请求，请检查CORS配置。\n\n**提示：** 后端服务需要配置CORS以允许前端访问。',
          timestamp: Date.now()
        }
        addMessage(errorMessage)
      } else {
        // 其他错误
        const errorMessage: Message = {
          role: 'assistant',
          content: `服务器返回错误：${response.status} ${response.statusText}`,
          timestamp: Date.now()
        }
        addMessage(errorMessage)
      }
    } catch (error: any) {
      // 网络错误
      let errorContent = '网络连接失败，请检查网络设置后重试。\n\n'+
                        '**可能的原因：**\n'+
                        '1. 后端服务未启动\n'+
                        '2. 网络连接问题\n'+
                        '3. 防火墙阻止了连接\n\n'+
                        '**解决方案：**\n'+
                        '1. 启动后端服务\n'+
                        '2. 检查网络连接\n'+
                        '3. 暂时关闭防火墙\n\n'+
                        '**启动后端服务命令：**\n'+
                        '`uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload`';
      
      if (error.message) {
        errorContent += `\n\n**错误详情：** ${error.message}`;
      }
      
      const errorMessage: Message = {
        role: 'assistant',
        content: errorContent,
        timestamp: Date.now()
      }
      addMessage(errorMessage)
    } finally {
      // 结束打字状态
      isTyping.value = false
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
