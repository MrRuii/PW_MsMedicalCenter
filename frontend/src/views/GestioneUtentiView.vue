<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">Gestione utenti</h1>
      <p class="mt-1 text-sm text-gray-500">Elenco di tutti gli utenti registrati.</p>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>

    <div v-else class="flex flex-col gap-3">
      <div v-for="u in utenti" :key="u.id" class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p class="font-medium text-gray-900">{{ u.nome ?? '—' }} {{ u.cognome ?? '' }}</p>
            <p class="text-sm text-gray-500">{{ u.email }}</p>
            <p class="mt-1 text-sm text-gray-500">
              <span v-if="u.codice_fiscale">Codice fiscale: {{ u.codice_fiscale }}</span>
              <span v-if="u.numero_albo">Numero albo: {{ u.numero_albo }}</span>
              <span v-if="u.telefono"> · Telefono: {{ u.telefono }}</span>
              · Registrato il {{ formatData(u.created_at) }}
            </p>
          </div>
          <div class="flex items-center gap-2">
            <span class="badge badge-grigio capitalize">{{ u.ruolo }}</span>
            <span class="badge" :class="u.is_active ? 'badge-verde' : 'badge-rosso'">
              {{ u.is_active ? 'Attivo' : 'Disattivato' }}
            </span>
          </div>
        </div>

        <p v-if="erroreRiga[u.id]" class="mt-3 text-sm text-red-600">{{ erroreRiga[u.id] }}</p>

        <div v-if="modificaId === u.id" class="mt-4 grid gap-3 sm:grid-cols-3">
          <input v-model="form.nome" placeholder="Nome" class="input" />
          <input v-model="form.cognome" placeholder="Cognome" class="input" />
          <input v-if="u.ruolo === 'paziente'" v-model="form.telefono" placeholder="Telefono" class="input" />
          <input v-if="u.ruolo === 'medico'" v-model="form.numero_albo" placeholder="Numero albo" class="input" />
          <p v-if="erroreForm" class="text-sm text-red-600 sm:col-span-3">{{ erroreForm }}</p>
          <div class="flex gap-3 sm:col-span-3">
            <button class="btn-secondary" @click="chiudiModifica">Annulla</button>
            <button class="btn-primary" :disabled="salvataggioInCorso" @click="salva(u)">Salva</button>
          </div>
        </div>

        <div v-else class="mt-4 flex gap-3">
          <button v-if="u.ruolo === 'paziente' || u.ruolo === 'medico'" class="btn-secondary" @click="apriModifica(u)">
            Modifica
          </button>
          <button v-if="u.id !== authStore.utente?.id" class="btn-secondary" @click="cambiaStato(u)">
            {{ u.is_active ? 'Disattiva' : 'Riattiva' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import { useAuthStore } from '../stores/auth'
import type { UtenteDettaglio } from '../types'

const authStore = useAuthStore()

const utenti = ref<UtenteDettaglio[]>([])
const caricamento = ref(true)
const errore = ref('')
const erroreForm = ref('')
const erroreRiga = reactive<Record<number, string>>({})
const salvataggioInCorso = ref(false)

const modificaId = ref<number | null>(null)
const form = reactive({ nome: '', cognome: '', telefono: '', numero_albo: '' })

onMounted(caricaUtenti)

async function caricaUtenti() {
  caricamento.value = true
  errore.value = ''
  try {
    const { data } = await apiClient.get<UtenteDettaglio[]>('/api/auth/users')
    utenti.value = data
  } catch {
    errore.value = 'Impossibile caricare gli utenti'
  } finally {
    caricamento.value = false
  }
}

function formatData(dataIso: string): string {
  return new Date(dataIso).toLocaleDateString('it-IT')
}

function apriModifica(u: UtenteDettaglio) {
  modificaId.value = u.id
  form.nome = u.nome ?? ''
  form.cognome = u.cognome ?? ''
  form.telefono = u.telefono ?? ''
  form.numero_albo = u.numero_albo ?? ''
  erroreForm.value = ''
}

function chiudiModifica() {
  modificaId.value = null
}

async function salva(u: UtenteDettaglio) {
  erroreForm.value = ''
  salvataggioInCorso.value = true
  const payload: Record<string, string> = { nome: form.nome, cognome: form.cognome }
  if (u.ruolo === 'paziente') payload.telefono = form.telefono
  if (u.ruolo === 'medico') payload.numero_albo = form.numero_albo
  try {
    const { data } = await apiClient.put<UtenteDettaglio>(`/api/auth/users/${u.id}`, payload)
    Object.assign(u, data)
    modificaId.value = null
  } catch (e: any) {
    erroreForm.value = e.response?.data?.detail ?? 'Non è stato possibile salvare le modifiche'
  } finally {
    salvataggioInCorso.value = false
  }
}

async function cambiaStato(u: UtenteDettaglio) {
  delete erroreRiga[u.id]
  if (u.is_active && !confirm(`Vuoi disattivare ${u.email}? Non potrà più accedere.`)) return
  try {
    const { data } = await apiClient.put<UtenteDettaglio>(`/api/auth/users/${u.id}`, {
      is_active: !u.is_active,
    })
    Object.assign(u, data)
  } catch (e: any) {
    erroreRiga[u.id] = e.response?.data?.detail ?? 'Non è stato possibile cambiare lo stato'
  }
}
</script>
