<template>
  <div class="min-h-screen">
    <header class="border-b border-primary-100 bg-white px-6 py-3 shadow-sm">
      <div class="mx-auto flex max-w-4xl items-center justify-between">
        <img :src="logoWordmark" alt="MS Medical Center" class="h-8" />
        <div class="flex items-center gap-4">
          <div class="text-right leading-tight">
            <p class="text-sm font-medium text-gray-700">{{ authStore.utente?.email }}</p>
            <p class="text-xs text-primary-600 capitalize">{{ authStore.ruolo }}</p>
          </div>
          <button @click="onLogout" class="btn-secondary">Logout</button>
        </div>
      </div>
    </header>
    <main class="mx-auto max-w-4xl px-6 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import logoWordmark from '../assets/logo-wordmark.png'

const authStore = useAuthStore()
const router = useRouter()

async function onLogout() {
  authStore.logout()
  await router.push('/login')
}
</script>
