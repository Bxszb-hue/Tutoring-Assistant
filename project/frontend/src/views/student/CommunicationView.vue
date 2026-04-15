<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">沟通倾诉</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-4xl mx-auto space-y-6">
          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">快速入口</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                v-for="channel in channels"
                :key="channel.id"
                class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                @click="handleChannelClick(channel)"
              >
                <div class="flex items-center gap-3 mb-2">
                  <component :is="channel.icon" :class="['w-5 h-5', channel.iconColor]" />
                  <h4 class="font-medium text-gray-900">{{ channel.name }}</h4>
                </div>
                <p class="text-sm text-gray-500">{{ channel.description }}</p>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">心理健康资源</h3>
            <div class="space-y-4">
              <div class="flex items-start gap-4 p-4 bg-blue-50 rounded-lg">
                <Phone class="w-6 h-6 text-blue-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">24小时心理热线</h4>
                  <p class="text-lg font-bold text-blue-600 mt-1">400-161-9995</p>
                  <p class="text-sm text-gray-600 mt-1">全国心理援助热线，24小时免费服务</p>
                </div>
              </div>
              
              <div class="flex items-start gap-4 p-4 bg-purple-50 rounded-lg">
                <Building class="w-6 h-6 text-purple-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">学校心理咨询中心</h4>
                  <p class="text-sm text-gray-600 mt-1">地址：学生活动中心3楼</p>
                  <p class="text-sm text-gray-600">时间：工作日 8:00-17:00</p>
                  <p class="text-sm text-gray-600">预约电话：0123-4567890</p>
                </div>
              </div>
              
              <div class="flex items-start gap-4 p-4 bg-green-50 rounded-lg">
                <Heart class="w-6 h-6 text-green-600 mt-1" />
                <div>
                  <h4 class="font-medium text-gray-900">自我调节建议</h4>
                  <ul class="text-sm text-gray-600 mt-1 space-y-1">
                    <li>• 保持规律作息，充足睡眠</li>
                    <li>• 适度运动，释放压力</li>
                    <li>• 与朋友家人倾诉交流</li>
                    <li>• 培养兴趣爱好，放松心情</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">我的辅导员</h3>
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span class="text-white text-2xl font-bold">王</span>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900">王辅导员</h4>
                <p class="text-sm text-gray-500">计算机学院</p>
                <p class="text-sm text-gray-600 mt-1">电话：13800138000</p>
                <p class="text-sm text-gray-600">邮箱：wang@university.edu</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { MessageSquare, Phone, Heart, Building, Calendar } from 'lucide-vue-next'

const channels = ref([
  {
    id: 'counselor',
    name: '联系辅导员',
    description: '与辅导员一对一沟通',
    icon: MessageSquare,
    iconColor: 'text-blue-600'
  },
  {
    id: 'appointment',
    name: '预约咨询',
    description: '预约心理咨询服务',
    icon: Calendar,
    iconColor: 'text-purple-600'
  },
  {
    id: 'ai-chat',
    name: 'AI倾诉',
    description: '24小时在线倾听',
    icon: Heart,
    iconColor: 'text-pink-600'
  }
])

const handleChannelClick = (channel: any) => {
  alert(`功能开发中：${channel.name}`)
}
</script>
