<template>
  <div class="min-h-screen bg-gray-50">
    <header class="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4 shadow-sm">
      <span class="font-medium text-gray-700">{{ authStore.utente?.email }}</span>
      <button
        @click="onLogout"
        class="rounded-md bg-gray-100 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
      >
        Logout
      </button>
    </header>
    <main class="mx-auto max-w-4xl px-6 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

async function onLogout() {
  authStore.logout()
  await router.push('/login')
}
</script>
