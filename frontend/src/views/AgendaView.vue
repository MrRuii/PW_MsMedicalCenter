<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">La mia agenda</h1>
      <p class="mt-1 text-sm text-gray-500">Gli appuntamenti dei tuoi pazienti.</p>
    </div>

    <div class="flex gap-2">
      <button
        class="chip"
        :class="{ 'bg-primary-600! text-white! border-primary-600!': periodo === 'giorno' }"
        @click="periodo = 'giorno'"
      >
        Oggi
      </button>
      <button
        class="chip"
        :class="{ 'bg-primary-600! text-white! border-primary-600!': periodo === 'settimana' }"
        @click="periodo = 'settimana'"
      >
        Questa settimana
      </button>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>
    <p v-else-if="appuntamentiFiltrati.length === 0" class="text-sm text-gray-500">
      Nessun appuntamento in questo periodo.
    </p>

    <div v-else class="flex flex-col gap-3">
      <div
        v-for="app in appuntamentiFiltrati"
        :key="app.id"
        class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p class="font-medium text-gray-900">{{ formatDataOra(app.data_ora) }}</p>
            <p class="mt-1 text-sm text-gray-600">
              {{ app.paziente.nome }} {{ app.paziente.cognome }} · {{ prestazioneDi(app)?.nome ?? 'Prestazione' }}
            </p>
            <p class="text-sm text-gray-500">{{ sedeDi(app)?.nome }} ({{ sedeDi(app)?.citta }})</p>
          </div>
          <span :class="['badge', badgeClasse(app.stato)]">{{ etichettaStato(app.stato) }}</span>
        </div>

        <p v-if="erroreAzione[app.id]" class="mt-3 text-sm text-red-600">{{ erroreAzione[app.id] }}</p>

        <div v-if="puoCompletare(app.stato)" class="mt-4">
          <button class="btn-secondary" @click="completa(app)">Completa appuntamento</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Appuntamento, Prestazione, Sede } from '../types'
import { formatDataOra } from '../utils/formato'
import { badgeClasse, etichettaStato, puoCompletare } from '../utils/statoAppuntamento'

const appuntamenti = ref<Appuntamento[]>([])
const sediList = ref<Sede[]>([])
const prestazioniList = ref<Prestazione[]>([])

const caricamento = ref(true)
const errore = ref('')
const erroreAzione = reactive<Record<number, string>>({})
const periodo = ref<'giorno' | 'settimana'>('giorno')

onMounted(caricaTutto)

async function caricaTutto() {
  caricamento.value = true
  errore.value = ''
  try {
    const [appResp, sediResp, prestResp] = await Promise.all([
      apiClient.get<Appuntamento[]>('/api/appuntamenti'),
      apiClient.get<Sede[]>('/api/sedi'),
      apiClient.get<Prestazione[]>('/api/prestazioni'),
    ])
    appuntamenti.value = appResp.data
    sediList.value = sediResp.data
    prestazioniList.value = prestResp.data
  } catch {
    errore.value = 'Impossibile caricare gli appuntamenti'
  } finally {
    caricamento.value = false
  }
}

function inizioGiorno(d: Date): Date {
  const r = new Date(d)
  r.setHours(0, 0, 0, 0)
  return r
}

function fineGiorno(d: Date): Date {
  const r = new Date(d)
  r.setHours(23, 59, 59, 999)
  return r
}

function inizioSettimana(d: Date): Date {
  const r = inizioGiorno(d)
  const giorno = r.getDay()
  const offset = giorno === 0 ? 6 : giorno - 1
  r.setDate(r.getDate() - offset)
  return r
}

function fineSettimana(d: Date): Date {
  const inizio = inizioSettimana(d)
  const r = new Date(inizio)
  r.setDate(r.getDate() + 6)
  return fineGiorno(r)
}

const appuntamentiFiltrati = computed(() => {
  const ora = new Date()
  const [inizio, fine] =
    periodo.value === 'giorno' ? [inizioGiorno(ora), fineGiorno(ora)] : [inizioSettimana(ora), fineSettimana(ora)]
  return appuntamenti.value
    .filter((a) => {
      const dataOra = new Date(a.data_ora)
      return dataOra >= inizio && dataOra <= fine
    })
    .sort((a, b) => a.data_ora.localeCompare(b.data_ora))
})

function sedeDi(app: Appuntamento) {
  return sediList.value.find((s) => s.id === app.sede_id)
}
function prestazioneDi(app: Appuntamento) {
  return prestazioniList.value.find((p) => p.id === app.prestazione_id)
}

async function completa(app: Appuntamento) {
  delete erroreAzione[app.id]
  try {
    const { data } = await apiClient.patch<Appuntamento>(`/api/appuntamenti/${app.id}/completa`)
    const index = appuntamenti.value.findIndex((a) => a.id === app.id)
    if (index !== -1) appuntamenti.value[index] = data
  } catch {
    erroreAzione[app.id] = "Non è stato possibile completare l'appuntamento"
  }
}
</script>
