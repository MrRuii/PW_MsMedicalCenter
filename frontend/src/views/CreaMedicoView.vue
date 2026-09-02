<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">Crea medico</h1>
      <p class="mt-1 text-sm text-gray-500">Crea un nuovo account medico con le relative specialità.</p>
    </div>

    <section class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <template v-if="!creatoConSuccesso">
        <form @submit.prevent="salva" class="grid gap-4 sm:grid-cols-2">
          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Email</span>
            <input v-model="form.email" type="email" required class="input" />
          </label>

          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Password</span>
            <input v-model="form.password" type="password" required minlength="8" class="input" />
          </label>

          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Nome</span>
            <input v-model="form.nome" required class="input" />
          </label>

          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Cognome</span>
            <input v-model="form.cognome" required class="input" />
          </label>

          <label class="flex flex-col gap-1">
            <span class="text-sm font-medium text-gray-700">Numero albo</span>
            <input v-model="form.numero_albo" class="input" />
          </label>

          <div class="sm:col-span-2">
            <span class="text-sm font-medium text-gray-700">Specialità</span>
            <div class="mt-2 grid gap-2 sm:grid-cols-2">
              <label
                v-for="s in specialitaList"
                :key="s.id"
                class="flex items-center gap-2 rounded-md border border-gray-200 px-3 py-2 text-sm"
              >
                <input type="checkbox" :value="s.id" v-model="form.specialita_ids" />
                {{ s.nome }}
              </label>
            </div>
          </div>

          <p v-if="errore" class="text-sm text-red-600 sm:col-span-2">{{ errore }}</p>

          <button type="submit" class="btn-primary sm:col-span-2" :disabled="salvataggioInCorso">
            Crea medico
          </button>
        </form>
      </template>

      <template v-else>
        <p class="text-sm text-gray-700">Medico creato correttamente.</p>
        <div class="mt-4 flex gap-3">
          <button class="btn-secondary" @click="nuovoMedico">Crea un altro medico</button>
          <router-link class="btn-primary" to="/admin/utenti">Vai a gestione utenti</router-link>
        </div>
      </template>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Specialita } from '../types'

const specialitaList = ref<Specialita[]>([])
const errore = ref('')
const salvataggioInCorso = ref(false)
const creatoConSuccesso = ref(false)

const form = reactive({
  email: '',
  password: '',
  nome: '',
  cognome: '',
  numero_albo: '',
  specialita_ids: [] as number[],
})

onMounted(async () => {
  try {
    const { data } = await apiClient.get<Specialita[]>('/api/specialita')
    specialitaList.value = data
  } catch {
    errore.value = 'Impossibile caricare le specialità'
  }
})

async function salva() {
  errore.value = ''
  salvataggioInCorso.value = true
  try {
    await apiClient.post('/api/medici', {
      email: form.email,
      password: form.password,
      nome: form.nome,
      cognome: form.cognome,
      numero_albo: form.numero_albo || null,
      specialita_ids: form.specialita_ids,
    })
    creatoConSuccesso.value = true
  } catch (e: any) {
    errore.value = e.response?.data?.detail ?? 'Non è stato possibile creare il medico'
  } finally {
    salvataggioInCorso.value = false
  }
}

function nuovoMedico() {
  form.email = ''
  form.password = ''
  form.nome = ''
  form.cognome = ''
  form.numero_albo = ''
  form.specialita_ids = []
  creatoConSuccesso.value = false
}
</script>
