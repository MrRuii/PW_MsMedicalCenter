import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '../api/client'

export interface Utente {
  id: number
  email: string
  ruolo: string
  is_active: boolean
  created_at: string
}

interface TokenResponse {
  access_token: string
  token_type: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const utente = ref<Utente | null>(null)

  const ruolo = computed(() => utente.value?.ruolo ?? null)
  const isAuthenticated = computed(() => token.value !== null)

  async function fetchUtente() {
    const response = await apiClient.get<Utente>('/api/auth/me')
    utente.value = response.data
  }

  async function login(email: string, password: string) {
    const response = await apiClient.post<TokenResponse>('/api/auth/login', {
      email,
      password,
    })
    token.value = response.data.access_token
    localStorage.setItem('token', token.value)
    await fetchUtente()
  }

  function logout() {
    token.value = null
    utente.value = null
    localStorage.removeItem('token')
  }

  return { token, utente, ruolo, isAuthenticated, login, logout, fetchUtente }
})
