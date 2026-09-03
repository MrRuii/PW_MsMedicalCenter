<template>
  <div class="flex min-h-screen flex-col">
    <header class="border-b border-primary-100 bg-white px-6 py-3 shadow-sm">
      <div class="mx-auto flex max-w-4xl items-center justify-between">
        <router-link :to="`/${authStore.ruolo}`" class="transition hover:opacity-80">
          <img :src="logoWordmark" alt="MS Medical Center" class="h-8" />
        </router-link>
        <div class="flex items-center gap-4">
          <div class="text-right leading-tight">
            <p class="text-sm font-medium text-gray-700">{{ authStore.utente?.email }}</p>
            <p class="text-xs text-primary-600 capitalize">{{ authStore.ruolo }}</p>
          </div>
          <button @click="onLogout" class="btn-secondary">Logout</button>
        </div>
      </div>
    </header>
    <main class="mx-auto w-full max-w-4xl flex-1 px-6 py-8">
      <router-view />
    </main>
    <footer class="bg-primary-900 px-6 py-5">
      <div class="mx-auto flex max-w-4xl flex-col gap-3 text-xs text-primary-200">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <span>© 2026 MS Medical Center · Progetto universitario</span>
          <span class="flex gap-4">
            <a href="/privacy.html" target="_blank" rel="noopener" class="hover:text-white hover:underline">Privacy</a>
            <a href="/termini-di-servizio.html" target="_blank" rel="noopener" class="hover:text-white hover:underline">Termini di servizio</a>
          </span>
        </div>
        <div class="border-t border-primary-800 pt-3">
          <p class="font-medium text-primary-100">Contatti</p>
          <p class="mt-1 text-primary-200/60">
            Email: info@msmedicalcenter.it · Tel: +39 06 1234567 · P.IVA 12345678901 · Capitale sociale € 50.000,00 i.v.
          </p>
        </div>
      </div>
    </footer>
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
