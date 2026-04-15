<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-2xl shadow-xl p-8">
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <span class="text-white text-3xl">🎓</span>
          </div>
          <h1 class="text-2xl font-bold text-gray-900">辅导员学生管理系统</h1>
          <p class="text-gray-500 mt-2">智能辅助 · 精准育人</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">用户类型</label>
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="userRole = 'student'"
                  :class="[
                    'flex-1 py-2 px-4 rounded-lg border-2 transition-all',
                    userRole === 'student'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 text-gray-600 hover:border-gray-300'
                  ]"
                >
                  学生
                </button>
                <button
                  type="button"
                  @click="userRole = 'counselor'"
                  :class="[
                    'flex-1 py-2 px-4 rounded-lg border-2 transition-all',
                    userRole === 'counselor'
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 text-gray-600 hover:border-gray-300'
                  ]"
                >
                  辅导员
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
              <input
                v-model="username"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                :placeholder="userRole === 'student' ? '请输入学生账号' : '请输入辅导员账号'"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
              <input
                v-model="password"
                type="password"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="请输入密码"
              />
            </div>

            <div v-if="errorMessage" class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-600">{{ errorMessage }}</p>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ loading ? '登录中...' : '登录' }}
            </button>
          </div>
        </form>

        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
          <p class="text-sm text-gray-600 text-center mb-2">测试账号</p>
          <div class="text-xs text-gray-500 space-y-1">
            <p><span class="font-medium">学生账号：</span>student / 123456</p>
            <p><span class="font-medium">辅导员账号：</span>counselor / 123456</p>
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
const userRole = ref<'student' | 'counselor'>('student')
const loading = ref(false)
const errorMessage = ref('')

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
