<template>
  <div class="flex min-h-screen items-center justify-center bg-linear-to-br from-primary-50 via-white to-accent-50 px-4 py-10">
    <div class="w-full max-w-md rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
      <img :src="logoWordmark" alt="MS Medical Center" class="mx-auto h-9" />
      <h1 class="mt-6 text-2xl font-semibold text-gray-900">Registrazione paziente</h1>

      <form @submit.prevent="onSubmit" class="mt-6 flex flex-col gap-4">
        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Email</span>
          <input v-model="form.email" type="email" required class="input" />
        </label>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Password</span>
          <input v-model="form.password" type="password" required minlength="8" class="input" />
        </label>

        <div class="grid grid-cols-2 gap-4">
          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Nome</span>
            <input v-model="form.nome" required class="input" />
          </label>
          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Cognome</span>
            <input v-model="form.cognome" required class="input" />
          </label>
        </div>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Codice fiscale</span>
          <input v-model="form.codice_fiscale" required class="input" />
        </label>

        <div class="grid grid-cols-2 gap-4">
          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Data di nascita</span>
            <input v-model="form.data_nascita" type="date" class="input" />
          </label>
          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Telefono</span>
            <input v-model="form.telefono" class="input" />
          </label>
        </div>

        <p v-if="errore" class="text-sm text-red-600">{{ errore }}</p>
        <p v-if="successo" class="text-sm text-green-600">
          Registrazione completata, ora puoi accedere.
        </p>

        <button
          type="submit"
          :disabled="caricamento"
          class="btn-primary mt-2"
        >
          Registrati
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-gray-500">
        <router-link to="/login" class="text-primary-600 hover:underline">
          Hai già un account? Accedi
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import apiClient from '../api/client'
import logoWordmark from '../assets/logo-wordmark.png'

const form = reactive({
  email: '',
  password: '',
  nome: '',
  cognome: '',
  codice_fiscale: '',
  data_nascita: '',
  telefono: '',
})

const errore = ref('')
const successo = ref(false)
const caricamento = ref(false)

async function onSubmit() {
  errore.value = ''
  successo.value = false
  caricamento.value = true
  try {
    await apiClient.post('/api/auth/register', {
      ...form,
      data_nascita: form.data_nascita || null,
      telefono: form.telefono || null,
    })
    successo.value = true
  } catch {
    errore.value = 'Registrazione non riuscita, controlla i dati inseriti'
  } finally {
    caricamento.value = false
  }
}
</script>
