<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <h1 class="text-2xl font-semibold text-gray-900">I miei appuntamenti</h1>
      <router-link to="/paziente/prenota" class="btn-primary">Prenota una visita</router-link>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>
    <p v-else-if="appuntamentiOrdinati.length === 0" class="text-sm text-gray-500">
      Non hai ancora prenotato nessun appuntamento.
    </p>

    <div v-else class="flex flex-col gap-3">
      <div
        v-for="app in appuntamentiOrdinati"
        :key="app.id"
        class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p class="font-medium text-gray-900">{{ formatDataOra(app.data_ora) }}</p>
            <p class="mt-1 text-sm text-gray-600">
              {{ prestazioneDi(app)?.nome ?? 'Prestazione' }} · Dr. {{ medicoDi(app)?.nome }}
              {{ medicoDi(app)?.cognome }}
            </p>
            <p class="text-sm text-gray-500">{{ sedeDi(app)?.nome }} ({{ sedeDi(app)?.citta }})</p>
          </div>
          <span :class="['badge', badgeClasse(app.stato)]">{{ etichettaStato(app.stato) }}</span>
        </div>

        <p v-if="erroreAnnulla[app.id]" class="mt-3 text-sm text-red-600">{{ erroreAnnulla[app.id] }}</p>

        <div v-if="puoAnnullare(app.stato)" class="mt-4">
          <button class="btn-secondary" @click="annulla(app)">Annulla appuntamento</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Appuntamento, Medico, Prestazione, Sede } from '../types'
import { formatDataOra } from '../utils/formato'
import { badgeClasse, etichettaStato, puoAnnullare } from '../utils/statoAppuntamento'

const appuntamenti = ref<Appuntamento[]>([])
const mediciList = ref<Medico[]>([])
const sediList = ref<Sede[]>([])
const prestazioniList = ref<Prestazione[]>([])

const caricamento = ref(true)
const errore = ref('')
const erroreAnnulla = reactive<Record<number, string>>({})

onMounted(caricaTutto)

async function caricaTutto() {
  caricamento.value = true
  errore.value = ''
  try {
    const [appResp, mediciResp, sediResp, prestResp] = await Promise.all([
      apiClient.get<Appuntamento[]>('/api/appuntamenti'),
      apiClient.get<Medico[]>('/api/medici'),
      apiClient.get<Sede[]>('/api/sedi'),
      apiClient.get<Prestazione[]>('/api/prestazioni'),
    ])
    appuntamenti.value = appResp.data
    mediciList.value = mediciResp.data
    sediList.value = sediResp.data
    prestazioniList.value = prestResp.data
  } catch {
    errore.value = 'Impossibile caricare gli appuntamenti'
  } finally {
    caricamento.value = false
  }
}

const appuntamentiOrdinati = computed(() =>
  [...appuntamenti.value].sort((a, b) => a.data_ora.localeCompare(b.data_ora)),
)

function medicoDi(app: Appuntamento) {
  return mediciList.value.find((m) => m.id === app.medico_id)
}
function sedeDi(app: Appuntamento) {
  return sediList.value.find((s) => s.id === app.sede_id)
}
function prestazioneDi(app: Appuntamento) {
  return prestazioniList.value.find((p) => p.id === app.prestazione_id)
}

async function annulla(app: Appuntamento) {
  delete erroreAnnulla[app.id]
  if (!confirm('Vuoi annullare questo appuntamento?')) return
  try {
    const { data } = await apiClient.patch<Appuntamento>(`/api/appuntamenti/${app.id}/annulla`)
    const index = appuntamenti.value.findIndex((a) => a.id === app.id)
    if (index !== -1) appuntamenti.value[index] = data
  } catch {
    erroreAnnulla[app.id] = "Non è stato possibile annullare l'appuntamento"
  }
}
</script>
