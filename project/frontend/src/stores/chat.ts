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

  return {
    messages,
    isTyping,
    backendConnected,
    addMessage,
    clearMessages,
    checkBackendConnection
  }
})
