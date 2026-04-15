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

const authStore = useAuthStore()
const studentsStore = useStudentsStore()
const warningsStore = useWarningsStore()
const notificationsStore = useNotificationsStore()

onMounted(() => {
  authStore.loadUser()
  studentsStore.loadStudents()
  warningsStore.loadWarnings()
  notificationsStore.loadData()
})
</script>
