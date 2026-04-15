<template>
  <div class="flex h-full bg-gray-50">
    <div class="flex-1 flex flex-col">
      <div class="bg-white border-b border-gray-100 px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold text-gray-900">学生画像</h1>
            <span class="px-3 py-1 bg-gray-100 text-gray-600 text-sm rounded-lg">
              {{ studentsStore.statistics.total }} 名学生
            </span>
          </div>
          <div class="flex items-center gap-3">
            <select
              v-model="filterClass"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部班级</option>
              <option v-for="cls in studentsStore.classes" :key="cls" :value="cls">{{ cls }}</option>
            </select>
            <select
              v-model="filterMajor"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部专业</option>
              <option v-for="major in studentsStore.majors" :key="major" :value="major">{{ major }}</option>
            </select>
            <select
              v-model="filterRisk"
              class="px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">全部风险等级</option>
              <option value="安全">安全</option>
              <option value="关注">关注</option>
              <option value="预警">预警</option>
              <option value="紧急">紧急</option>
            </select>
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索学生..."
              class="px-4 py-2 bg-gray-100 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      <div class="flex-1 overflow-auto p-6">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-green-50 rounded-lg flex items-center justify-center">
                  <Users class="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">安全学生</p>
                  <p class="text-xl font-bold text-gray-900">{{ studentsStore.statistics.byRiskLevel.safe }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-yellow-50 rounded-lg flex items-center justify-center">
                  <AlertTriangle class="w-5 h-5 text-yellow-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">关注学生</p>
                  <p class="text-xl font-bold text-gray-900">{{ studentsStore.statistics.byRiskLevel.attention }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-orange-50 rounded-lg flex items-center justify-center">
                  <AlertTriangle class="w-5 h-5 text-orange-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">预警学生</p>
                  <p class="text-xl font-bold text-gray-900">{{ studentsStore.statistics.byRiskLevel.warning }}</p>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl border border-gray-100 p-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-red-50 rounded-lg flex items-center justify-center">
                  <AlertCircle class="w-5 h-5 text-red-600" />
                </div>
                <div>
                  <p class="text-sm text-gray-500">紧急学生</p>
                  <p class="text-xl font-bold text-gray-900">{{ studentsStore.statistics.byRiskLevel.urgent }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="student in filteredStudents"
              :key="student.id"
              @click="studentsStore.selectedStudent = student"
              class="bg-white rounded-xl border border-gray-100 p-4 hover:shadow-md transition-all cursor-pointer"
              :class="{
                'ring-2 ring-blue-500': studentsStore.selectedStudent?.id === student.id
              }"
            >
              <div class="flex items-start justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                    <span class="text-white font-semibold">{{ student.name.charAt(0) }}</span>
                  </div>
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ student.name }}</h3>
                    <p class="text-sm text-gray-500">{{ student.studentId }}</p>
                  </div>
                </div>
                <span :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  student.riskLevel === '安全' ? 'bg-green-100 text-green-700' :
                  student.riskLevel === '关注' ? 'bg-yellow-100 text-yellow-700' :
                  student.riskLevel === '预警' ? 'bg-orange-100 text-orange-700' :
                  'bg-red-100 text-red-700'
                ]">
                  {{ student.riskLevel }}
                </span>
              </div>

              <div class="grid grid-cols-2 gap-2 text-sm mb-3">
                <div>
                  <span class="text-gray-500">专业：</span>
                  <span class="text-gray-700">{{ student.major }}</span>
                </div>
                <div>
                  <span class="text-gray-500">班级：</span>
                  <span class="text-gray-700">{{ student.className }}</span>
                </div>
                <div>
                  <span class="text-gray-500">GPA：</span>
                  <span class="text-gray-700">{{ student.grades.gpa }}</span>
                </div>
                <div>
                  <span class="text-gray-500">出勤率：</span>
                  <span class="text-gray-700">{{ student.grades.attendanceRate }}%</span>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <span v-for="tag in student.tags.slice(0, 3)" :key="tag" class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Users, AlertTriangle, AlertCircle } from 'lucide-vue-next'
import { useStudentsStore } from '@/stores/students'

const studentsStore = useStudentsStore()

const filterClass = ref('')
const filterMajor = ref('')
const filterRisk = ref('')
const searchKeyword = ref('')

const filteredStudents = computed(() => {
  let students = studentsStore.students
  
  if (filterClass.value) {
    students = students.filter(s => s.className === filterClass.value)
  }
  
  if (filterMajor.value) {
    students = students.filter(s => s.major === filterMajor.value)
  }
  
  if (filterRisk.value) {
    students = students.filter(s => s.riskLevel === filterRisk.value)
  }
  
  if (searchKeyword.value) {
    students = studentsStore.searchStudents(searchKeyword.value)
  }
  
  return students
})
</script>
