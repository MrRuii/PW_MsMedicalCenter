import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import MainLayout from '../layouts/MainLayout.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import PazienteDashboard from '../views/PazienteDashboard.vue'
import MedicoDashboard from '../views/MedicoDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    ruoli?: string[]
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { path: '/registrazione', name: 'registrazione', component: RegisterView },
    {
      path: '/',
      component: MainLayout,
      redirect: '/login',
      children: [
        {
          path: 'paziente',
          name: 'paziente',
          component: PazienteDashboard,
          meta: { requiresAuth: true, ruoli: ['paziente'] },
        },
        {
          path: 'medico',
          name: 'medico',
          component: MedicoDashboard,
          meta: { requiresAuth: true, ruoli: ['medico'] },
        },
        {
          path: 'admin',
          name: 'admin',
          component: AdminDashboard,
          meta: { requiresAuth: true, ruoli: ['admin'] },
        },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/login' },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return '/login'
  }

  // Dopo un ricaricamento della pagina abbiamo il token ma non ancora i dati utente
  if (authStore.isAuthenticated && !authStore.utente) {
    try {
      await authStore.fetchUtente()
    } catch {
      authStore.logout()
      return '/login'
    }
  }

  if (to.meta.ruoli && authStore.ruolo && !to.meta.ruoli.includes(authStore.ruolo)) {
    return `/${authStore.ruolo}`
  }

  return true
})

export default router
