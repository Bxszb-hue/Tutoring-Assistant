import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/counselor',
      redirect: '/counselor/students',
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/counselor/students',
      name: 'counselor-students',
      component: () => import('@/views/counselor/StudentsView.vue'),
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/counselor/warnings',
      name: 'counselor-warnings',
      component: () => import('@/views/counselor/WarningsView.vue'),
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/counselor/affairs',
      name: 'counselor-affairs',
      component: () => import('@/views/counselor/AffairsView.vue'),
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/counselor/statistics',
      name: 'counselor-statistics',
      component: () => import('@/views/counselor/StatisticsView.vue'),
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/counselor/ai-chat',
      name: 'counselor-ai-chat',
      component: () => import('@/views/AIChatView.vue'),
      meta: { requiresAuth: true, role: 'counselor' }
    },
    {
      path: '/student',
      redirect: '/student/profile',
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/profile',
      name: 'student-profile',
      component: () => import('@/views/student/ProfileView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/affairs',
      name: 'student-affairs',
      component: () => import('@/views/student/AffairsView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/communication',
      name: 'student-communication',
      component: () => import('@/views/student/CommunicationView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/notifications',
      name: 'student-notifications',
      component: () => import('@/views/student/NotificationsView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/assessment',
      name: 'student-assessment',
      component: () => import('@/views/student/AssessmentView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    },
    {
      path: '/student/ai-chat',
      name: 'student-ai-chat',
      component: () => import('@/views/AIChatView.vue'),
      meta: { requiresAuth: true, role: 'student' }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  authStore.loadUser()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.role && authStore.currentUser?.role !== to.meta.role) {
    if (authStore.isCounselor) {
      next('/counselor/students')
    } else if (authStore.isStudent) {
      next('/student/profile')
    } else {
      next('/login')
    }
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    if (authStore.isCounselor) {
      next('/counselor/students')
    } else {
      next('/student/profile')
    }
  } else {
    next()
  }
})

export default router
