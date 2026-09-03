import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import MainLayout from '../layouts/MainLayout.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import PazienteDashboard from '../views/PazienteDashboard.vue'
import MedicoDashboard from '../views/MedicoDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import PrenotaView from '../views/PrenotaView.vue'
import AppuntamentiView from '../views/AppuntamentiView.vue'
import AgendaView from '../views/AgendaView.vue'
import DisponibilitaMedicoView from '../views/DisponibilitaMedicoView.vue'
import GestioneUtentiView from '../views/GestioneUtentiView.vue'
import CreaMedicoView from '../views/CreaMedicoView.vue'
import MedicoRefertiView from '../views/MedicoRefertiView.vue'
import PazienteRefertiView from '../views/PazienteRefertiView.vue'
import DashboardIncassiView from '../views/DashboardIncassiView.vue'

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
          path: 'paziente/prenota',
          name: 'prenota',
          component: PrenotaView,
          meta: { requiresAuth: true, ruoli: ['paziente'] },
        },
        {
          path: 'paziente/appuntamenti',
          name: 'appuntamenti',
          component: AppuntamentiView,
          meta: { requiresAuth: true, ruoli: ['paziente'] },
        },
        {
          path: 'paziente/referti',
          name: 'paziente-referti',
          component: PazienteRefertiView,
          meta: { requiresAuth: true, ruoli: ['paziente'] },
        },
        {
          path: 'medico',
          name: 'medico',
          component: MedicoDashboard,
          meta: { requiresAuth: true, ruoli: ['medico'] },
        },
        {
          path: 'medico/agenda',
          name: 'agenda',
          component: AgendaView,
          meta: { requiresAuth: true, ruoli: ['medico'] },
        },
        {
          path: 'medico/disponibilita',
          name: 'disponibilita-medico',
          component: DisponibilitaMedicoView,
          meta: { requiresAuth: true, ruoli: ['medico'] },
        },
        {
          path: 'medico/referti',
          name: 'medico-referti',
          component: MedicoRefertiView,
          meta: { requiresAuth: true, ruoli: ['medico'] },
        },
        {
          path: 'admin',
          name: 'admin',
          component: AdminDashboard,
          meta: { requiresAuth: true, ruoli: ['admin'] },
        },
        {
          path: 'admin/utenti',
          name: 'gestione-utenti',
          component: GestioneUtentiView,
          meta: { requiresAuth: true, ruoli: ['admin'] },
        },
        {
          path: 'admin/nuovo-medico',
          name: 'crea-medico',
          component: CreaMedicoView,
          meta: { requiresAuth: true, ruoli: ['admin'] },
        },
        {
          path: 'admin/dashboard',
          name: 'dashboard-incassi',
          component: DashboardIncassiView,
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
