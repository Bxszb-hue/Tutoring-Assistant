<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <h1 class="text-xl font-bold text-gray-900">数据统计</h1>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm text-gray-500">学生总数</p>
                <Users class="w-5 h-5 text-blue-600" />
              </div>
              <p class="text-3xl font-bold text-gray-900">{{ studentsStore.statistics.total }}</p>
              <p class="text-sm text-green-600 mt-1">↑ 2 本月新增</p>
            </div>
            
            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm text-gray-500">平均GPA</p>
                <TrendingUp class="w-5 h-5 text-green-600" />
              </div>
              <p class="text-3xl font-bold text-gray-900">{{ studentsStore.statistics.averageGPA }}</p>
              <p class="text-sm text-green-600 mt-1">↑ 0.2 较上学期</p>
            </div>
            
            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm text-gray-500">平均出勤率</p>
                <Calendar class="w-5 h-5 text-purple-600" />
              </div>
              <p class="text-3xl font-bold text-gray-900">{{ studentsStore.statistics.averageAttendance }}%</p>
              <p class="text-sm text-red-600 mt-1">↓ 1.5% 较上月</p>
            </div>
            
            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm text-gray-500">预警数量</p>
                <AlertTriangle class="w-5 h-5 text-orange-600" />
              </div>
              <p class="text-3xl font-bold text-gray-900">{{ warningsStore.statistics.total }}</p>
              <p class="text-sm text-green-600 mt-1">↓ 1 较上周</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">风险等级分布</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">安全</span>
                    <span class="text-sm font-medium text-gray-900">{{ studentsStore.statistics.byRiskLevel.safe }}人</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" :style="{ width: (studentsStore.statistics.byRiskLevel.safe / studentsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">关注</span>
                    <span class="text-sm font-medium text-gray-900">{{ studentsStore.statistics.byRiskLevel.attention }}人</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: (studentsStore.statistics.byRiskLevel.attention / studentsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">预警</span>
                    <span class="text-sm font-medium text-gray-900">{{ studentsStore.statistics.byRiskLevel.warning }}人</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-orange-500 h-2 rounded-full" :style="{ width: (studentsStore.statistics.byRiskLevel.warning / studentsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">紧急</span>
                    <span class="text-sm font-medium text-gray-900">{{ studentsStore.statistics.byRiskLevel.urgent }}人</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-red-500 h-2 rounded-full" :style="{ width: (studentsStore.statistics.byRiskLevel.urgent / studentsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl border border-gray-100 p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">预警类型分布</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">学业预警</span>
                    <span class="text-sm font-medium text-gray-900">{{ warningsStore.statistics.byType.academic }}条</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-500 h-2 rounded-full" :style="{ width: (warningsStore.statistics.byType.academic / warningsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">心理预警</span>
                    <span class="text-sm font-medium text-gray-900">{{ warningsStore.statistics.byType.psychological }}条</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-purple-500 h-2 rounded-full" :style="{ width: (warningsStore.statistics.byType.psychological / warningsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
                
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-gray-600">日常预警</span>
                    <span class="text-sm font-medium text-gray-900">{{ warningsStore.statistics.byType.daily }}条</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-500 h-2 rounded-full" :style="{ width: (warningsStore.statistics.byType.daily / warningsStore.statistics.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-xl border border-gray-100 p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">近期工作记录</h3>
            <div class="space-y-3">
              <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <MessageSquare class="w-5 h-5 text-blue-600" />
                </div>
                <div class="flex-1">
                  <p class="font-medium text-gray-900">与张伟同学进行学业辅导谈话</p>
                  <p class="text-sm text-gray-500">2024-01-15 14:00</p>
                </div>
                <span class="text-xs text-gray-400">已完成</span>
              </div>
              
              <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle class="w-5 h-5 text-green-600" />
                </div>
                <div class="flex-1">
                  <p class="font-medium text-gray-900">处理李娜同学的请假申请</p>
                  <p class="text-sm text-gray-500">2024-01-14 16:30</p>
                </div>
                <span class="text-xs text-gray-400">已完成</span>
              </div>
              
              <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <AlertTriangle class="w-5 h-5 text-purple-600" />
                </div>
                <div class="flex-1">
                  <p class="font-medium text-gray-900">跟进王磊同学的预警情况</p>
                  <p class="text-sm text-gray-500">2024-01-13 10:00</p>
                </div>
                <span class="text-xs text-gray-400">已完成</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Users, TrendingUp, Calendar, AlertTriangle, MessageSquare, CheckCircle } from 'lucide-vue-next'
import { useStudentsStore } from '@/stores/students'
import { useWarningsStore } from '@/stores/warnings'

const studentsStore = useStudentsStore()
const warningsStore = useWarningsStore()
</script>
