<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <div v-if="authStore.isAuthenticated" class="flex h-screen">
      <Sidebar />
      <main class="flex-1 overflow-hidden">
        <router-view />
      </main>
    </div>
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import { useAuthStore } from '@/stores/auth'
import { useStudentsStore } from '@/stores/students'
import { useWarningsStore } from '@/stores/warnings'
import { useNotificationsStore } from '@/stores/notifications'
import { useAffairsStore } from '@/stores/affairs'
import { useAppointmentsStore } from '@/stores/appointments'
import { useCounselorChatStore } from '@/stores/counselorChat'
import { useAssessmentsStore } from '@/stores/assessments'

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const warningsStore = useWarningsStore()
const notificationsStore = useNotificationsStore()
const affairsStore = useAffairsStore()
const appointmentsStore = useAppointmentsStore()
const counselorChatStore = useCounselorChatStore()
const assessmentsStore = useAssessmentsStore()

onMounted(() => {
  authStore.loadUser()
  studentsStore.loadStudents()
  warningsStore.loadWarnings()
  notificationsStore.loadData()
  affairsStore.loadData()
  appointmentsStore.loadData()
  counselorChatStore.loadData()
  assessmentsStore.loadAssessments()
})
</script>
