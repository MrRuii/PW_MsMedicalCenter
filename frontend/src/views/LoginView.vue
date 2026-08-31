<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-sm rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
      <h1 class="text-2xl font-semibold text-gray-900">Accedi</h1>

      <form @submit.prevent="onSubmit" class="mt-6 flex flex-col gap-4">
        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Email</span>
          <input
            v-model="email"
            type="email"
            required
            class="input"
          />
        </label>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Password</span>
          <input
            v-model="password"
            type="password"
            required
            class="input"
          />
        </label>

        <p v-if="errore" class="text-sm text-red-600">{{ errore }}</p>

        <button
          type="submit"
          :disabled="caricamento"
          class="btn-primary mt-2"
        >
          Accedi
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-gray-500">
        <router-link to="/registrazione" class="text-indigo-600 hover:underline">
          Non hai un account? Registrati
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const email = ref('')
const password = ref('')
const errore = ref('')
const caricamento = ref(false)

const authStore = useAuthStore()
const router = useRouter()

async function onSubmit() {
  errore.value = ''
  caricamento.value = true
  try {
    await authStore.login(email.value, password.value)
    await router.push(`/${authStore.ruolo}`)
  } catch {
    errore.value = 'Email o password non corretti'
  } finally {
    caricamento.value = false
  }
}
</script>
