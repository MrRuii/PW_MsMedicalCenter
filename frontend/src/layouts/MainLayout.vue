<template>
  <div class="layout">
    <header class="app-header">
      <span>{{ authStore.utente?.email }}</span>
      <button @click="onLogout">Logout</button>
    </header>
    <main>
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
