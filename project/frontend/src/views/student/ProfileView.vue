<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">个人中心</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <div class="flex items-center gap-6">
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center">
                <span class="text-white text-4xl font-bold">{{ studentInitial }}</span>
              </div>
              <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ authStore.currentUser?.name }}</h2>
                <p class="text-gray-500 mt-1">{{ authStore.currentUser?.studentId }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <span class="text-sm text-gray-600">{{ authStore.currentUser?.className }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">基础信息</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-500">手机号</p>
                <p class="text-gray-900">{{ authStore.currentUser?.phone }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-500">邮箱</p>
                <p class="text-gray-900">{{ authStore.currentUser?.email }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">学业概况</h3>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center p-4 bg-gray-50 rounded-xl">
                <p class="text-2xl font-bold text-gray-900">3.5</p>
                <p class="text-sm text-gray-500">GPA</p>
              </div>
              <div class="text-center p-4 bg-gray-50 rounded-xl">
                <p class="text-2xl font-bold text-green-600">92%</p>
                <p class="text-sm text-gray-500">出勤率</p>
              </div>
              <div class="text-center p-4 bg-gray-50 rounded-xl">
                <p class="text-2xl font-bold text-gray-900">0</p>
                <p class="text-sm text-gray-500">挂科数</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">预警提醒</h3>
            <div class="text-center py-8 text-gray-500">
              <CheckCircle class="w-12 h-12 mx-auto mb-3 text-green-500" />
              <p>当前无预警提醒</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { CheckCircle } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const studentInitial = computed(() => {
  return authStore.currentUser?.name?.charAt(0) || 'U'
})
</script>
