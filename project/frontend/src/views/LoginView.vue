<template>
  <div class="min-h-screen bg-white flex">
    <div class="hidden lg:flex lg:w-1/2 flex-col items-center justify-center p-12 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl opacity-50"></div>
      <div class="absolute bottom-0 right-0 w-80 h-80 bg-purple-50 rounded-full blur-3xl opacity-50"></div>
      
      <div class="relative z-10 w-full max-w-lg">
        <div class="flex items-center gap-4 mb-10">
          <div class="w-14 h-14 bg-gradient-to-br from-blue-600 to-purple-700 rounded-2xl flex items-center justify-center">
            <span class="text-white text-2xl">🎓</span>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">辅导员学生管理智能体</h1>
            <p class="text-sm text-gray-500">智慧校园 · 精准育人</p>
          </div>
        </div>
        
        <div class="space-y-4 mb-12">
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <span class="text-xl">📊</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">学生画像全维度管理</h3>
                <p class="text-sm text-gray-500">智能分析学生数据，精准识别风险，提供个性化干预方案</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 bg-purple-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <span class="text-xl">🤖</span>
              </div>
              <div>
                <h3 class="font-semibold text-gray-900 mb-1">AI 智能助手</h3>
                <p class="text-sm text-gray-500">基于 LangChain 的智能体，自动生成报告、提供建议</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="flex gap-16">
          <div>
            <p class="text-3xl font-bold text-blue-600">50+</p>
            <p class="text-sm text-gray-500">虚拟学生</p>
          </div>
          <div>
            <p class="text-3xl font-bold text-purple-600">24/7</p>
            <p class="text-sm text-gray-500">智能服务</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="flex-1 flex items-center justify-center p-8 lg:p-12">
      <div class="w-full max-w-md">
        <div class="bg-white rounded-3xl shadow-xl p-8 lg:p-10">
          <div class="text-center mb-8">
            <h2 class="text-xl font-bold text-gray-900">欢迎使用</h2>
            <p class="text-sm text-gray-500 mt-2">请选择您的角色登录系统</p>
          </div>
          
          <div class="flex gap-2 mb-6 bg-gray-100 p-1 rounded-xl">
            <button
              type="button"
              @click="userRole = 'counselor'"
              :class="[
                'flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all',
                userRole === 'counselor'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              辅导员端
            </button>
            <button
              type="button"
              @click="userRole = 'student'"
              :class="[
                'flex-1 py-2 px-4 rounded-lg text-sm font-medium transition-all',
                userRole === 'student'
                  ? 'bg-white text-blue-600 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              ]"
            >
              学生端
            </button>
          </div>
          
          <form @submit.prevent="handleLogin" class="space-y-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">工号 / 用户名</label>
              <input
                v-model="username"
                type="text"
                required
                class="w-full px-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                :placeholder="userRole === 'student' ? '请输入工号或用户名' : '请输入工号或用户名'"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
              <div class="relative">
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  class="w-full px-4 py-3 pr-12 bg-gray-50 border border-gray-100 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:bg-white transition-all"
                  placeholder="请输入密码"
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="flex items-center justify-between">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" class="w-4 h-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                <span class="text-sm text-gray-600">记住我</span>
              </label>
              <a href="#" class="text-sm text-blue-600 hover:text-blue-700">忘记密码？</a>
            </div>
            
            <div v-if="errorMessage" class="p-3 bg-red-50 border border-red-200 rounded-xl">
              <p class="text-sm text-red-600">{{ errorMessage }}</p>
            </div>
            
            <button
              type="submit"
              :disabled="loading"
              class="w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </form>
          
          <div class="mt-6 p-4 bg-gray-50 rounded-xl">
            <p class="text-xs text-gray-500 mb-2">测试账号：</p>
            <div class="text-xs text-gray-600 space-y-1">
              <p>辅导员：counselor / 123456</p>
              <p>学生：student / 123456</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const userRole = ref<'student' | 'counselor'>('counselor')
const loading = ref(false)
const errorMessage = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''
  
  try {
    const success = await authStore.login(username.value, password.value, userRole.value)
    
    if (success) {
      if (userRole.value === 'counselor') {
        router.push('/counselor/students')
      } else {
        router.push('/student/profile')
      }
    } else {
      errorMessage.value = '用户名或密码错误'
    }
  } catch (error) {
    errorMessage.value = '登录失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>
