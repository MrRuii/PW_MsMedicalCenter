<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">I miei referti</h1>
      <p class="mt-1 text-sm text-gray-500">I referti caricati dai medici per le tue visite.</p>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>
    <p v-else-if="referti.length === 0" class="text-sm text-gray-500">Non hai ancora nessun referto.</p>

    <div v-else class="flex flex-col gap-3">
      <div v-for="r in refertiOrdinati" :key="r.id" class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
        <p class="font-medium text-gray-900">{{ formatData(r.data) }}</p>
        <p class="mt-1 text-sm text-gray-600">
          {{ prestazioneDi(r)?.nome ?? 'Prestazione' }} · Dr. {{ medicoDi(r)?.nome }} {{ medicoDi(r)?.cognome }}
        </p>
        <p class="mt-1 text-sm text-gray-500">{{ r.descrizione ?? 'Nessuna descrizione' }}</p>

        <p v-if="erroreRiga[r.id]" class="mt-3 text-sm text-red-600">{{ erroreRiga[r.id] }}</p>

        <div class="mt-4">
          <button class="btn-secondary" @click="scarica(r)">Scarica</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Appuntamento, Medico, Prestazione, Referto } from '../types'
import { formatData } from '../utils/formato'
import { scaricaReferto } from '../utils/download'

const referti = ref<Referto[]>([])
const appuntamenti = ref<Appuntamento[]>([])
const mediciList = ref<Medico[]>([])
const prestazioniList = ref<Prestazione[]>([])

const caricamento = ref(true)
const errore = ref('')
const erroreRiga = reactive<Record<number, string>>({})

onMounted(caricaTutto)

async function caricaTutto() {
  caricamento.value = true
  errore.value = ''
  try {
    const [refResp, appResp, mediciResp, prestResp] = await Promise.all([
      apiClient.get<Referto[]>('/api/referti'),
      apiClient.get<Appuntamento[]>('/api/appuntamenti'),
      apiClient.get<Medico[]>('/api/medici'),
      apiClient.get<Prestazione[]>('/api/prestazioni'),
    ])
    referti.value = refResp.data
    appuntamenti.value = appResp.data
    mediciList.value = mediciResp.data
    prestazioniList.value = prestResp.data
  } catch {
    errore.value = 'Impossibile caricare i referti'
  } finally {
    caricamento.value = false
  }
}

const refertiOrdinati = computed(() => [...referti.value].sort((a, b) => b.data.localeCompare(a.data)))

function appuntamentoDi(r: Referto) {
  return appuntamenti.value.find((a) => a.id === r.appuntamento_id)
}

function medicoDi(r: Referto) {
  const app = appuntamentoDi(r)
  return app ? mediciList.value.find((m) => m.id === app.medico_id) : undefined
}

function prestazioneDi(r: Referto) {
  const app = appuntamentoDi(r)
  return app ? prestazioniList.value.find((p) => p.id === app.prestazione_id) : undefined
}

async function scarica(r: Referto) {
  delete erroreRiga[r.id]
  try {
    await scaricaReferto(r.id, `referto-${r.appuntamento_id}`)
  } catch {
    erroreRiga[r.id] = 'Non è stato possibile scaricare il referto'
  }
}
</script>
