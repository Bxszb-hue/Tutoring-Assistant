<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="visible"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="handleClose"
      >
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>
        
        <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-lg max-h-[90vh] overflow-hidden">
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">发布通知</h3>
            <button
              @click="handleClose"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <div class="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
            <div class="space-y-5">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">通知标题</label>
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="请输入通知标题"
                  class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="block text-sm font-medium text-gray-700">目标班级</label>
                  <button
                    @click="toggleSelectAll"
                    class="text-sm text-blue-600 hover:text-blue-700"
                  >
                    {{ isAllSelected ? '取消全选' : '全选' }}
                  </button>
                </div>
                <div class="space-y-2 max-h-48 overflow-y-auto">
                  <label
                    v-for="classItem in availableClasses"
                    :key="classItem"
                    class="flex items-center gap-2 p-2 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <input
                      v-model="form.targetClasses"
                      type="checkbox"
                      :value="classItem"
                      class="w-4 h-4 text-blue-600 rounded"
                    />
                    <span class="text-sm text-gray-700">{{ classItem }}</span>
                    <span class="text-xs text-gray-400 ml-auto">({{ getClassStudentCount(classItem) }}人)</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">通知类型</label>
                <div class="flex gap-3">
                  <label class="flex items-center gap-2">
                    <input
                      v-model="form.type"
                      type="radio"
                      value="普通通知"
                      class="w-4 h-4 text-blue-600"
                    />
                    <span class="text-sm text-gray-700">普通通知</span>
                  </label>
                  <label class="flex items-center gap-2">
                    <input
                      v-model="form.type"
                      type="radio"
                      value="重要通知"
                      class="w-4 h-4 text-blue-600"
                    />
                    <span class="text-sm text-gray-700">重要通知</span>
                  </label>
                  <label class="flex items-center gap-2">
                    <input
                      v-model="form.type"
                      type="radio"
                      value="紧急通知"
                      class="w-4 h-4 text-blue-600"
                    />
                    <span class="text-sm text-gray-700">紧急通知</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">通知内容</label>
                <textarea
                  v-model="form.content"
                  rows="4"
                  placeholder="请输入通知内容"
                  class="w-full px-4 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                ></textarea>
              </div>
            </div>
          </div>
          
          <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100 bg-gray-50">
            <button
              @click="handleClose"
              class="px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
            >
              取消
            </button>
            <button
              @click="handleSend"
              :disabled="!form.title.trim() || !form.content.trim() || form.targetClasses.length === 0"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white rounded-lg transition-colors"
            >
              发送通知
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { reactive, computed, onMounted } from 'vue'
import { X } from 'lucide-vue-next'
import { useStudentsStore } from '@/stores/students'

const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'send', data: { title: string; content: string; targetClasses: string[]; type: string; totalStudents: number }): void
}>()

const studentsStore = useStudentsStore()

const form = reactive({
  title: '',
  content: '',
  targetClasses: [] as string[],
  type: '普通通知'
})

const availableClasses = computed(() => {
  return studentsStore.classes
})

const isAllSelected = computed(() => {
  return availableClasses.value.length > 0 && 
         form.targetClasses.length === availableClasses.value.length
})

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    form.targetClasses = []
  } else {
    form.targetClasses = [...availableClasses.value]
  }
}

const getClassStudentCount = (className: string) => {
  return studentsStore.students.filter(s => s.className === className).length
}

const handleClose = () => {
  emit('close')
}

const handleSend = () => {
  if (!form.title.trim() || !form.content.trim() || form.targetClasses.length === 0) return
  
  const totalStudents = form.targetClasses.reduce((sum, className) => {
    return sum + getClassStudentCount(className)
  }, 0)
  
  emit('send', {
    title: form.title,
    content: form.content,
    targetClasses: [...form.targetClasses],
    type: form.type,
    totalStudents
  })
  
  form.title = ''
  form.content = ''
  form.targetClasses = []
  form.type = '普通通知'
}

onMounted(() => {
  if (!studentsStore.students.length) {
    studentsStore.loadStudents()
  }
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95) translateY(10px);
}
</style>
