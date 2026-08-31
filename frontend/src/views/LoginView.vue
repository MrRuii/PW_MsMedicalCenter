<template>
  <div class="auth-page">
    <h1>Accedi</h1>
    <form @submit.prevent="onSubmit">
      <label>
        Email
        <input v-model="email" type="email" required />
      </label>
      <label>
        Password
        <input v-model="password" type="password" required />
      </label>
      <p v-if="errore">{{ errore }}</p>
      <button type="submit" :disabled="caricamento">Accedi</button>
    </form>
    <p><router-link to="/registrazione">Non hai un account? Registrati</router-link></p>
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
