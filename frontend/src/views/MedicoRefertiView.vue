<template>
  <div class="flex flex-col gap-8">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">I miei referti</h1>
      <p class="mt-1 text-sm text-gray-500">Carica i referti degli appuntamenti completati e gestisci quelli già caricati.</p>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>

    <template v-else>
      <section v-if="appuntamentiSenzaReferto.length > 0" class="flex flex-col gap-3">
        <h2 class="font-medium text-gray-900">Appuntamenti completati senza referto</h2>

        <div v-for="app in appuntamentiSenzaReferto" :key="app.id" class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p class="font-medium text-gray-900">{{ formatDataOra(app.data_ora) }}</p>
          <p class="mt-1 text-sm text-gray-600">
            {{ app.paziente.nome }} {{ app.paziente.cognome }} · {{ prestazioneDi(app)?.nome ?? 'Prestazione' }}
          </p>

          <div v-if="uploadAppuntamentoId === app.id" class="mt-4 flex flex-col gap-3">
            <input type="file" accept=".pdf,.jpg,.jpeg,.png" class="input" @change="onFileChange" />
            <textarea v-model="formUpload.descrizione" placeholder="Descrizione (opzionale)" rows="2" class="input" />
            <p v-if="erroreUpload" class="text-sm text-red-600">{{ erroreUpload }}</p>
            <div class="flex gap-3">
              <button class="btn-secondary" @click="chiudiUpload">Annulla</button>
              <button class="btn-primary" :disabled="caricamentoInCorso" @click="carica(app)">Carica referto</button>
            </div>
          </div>
          <div v-else class="mt-4">
            <button class="btn-secondary" @click="apriUpload(app)">Carica referto</button>
          </div>
        </div>
      </section>

      <section class="flex flex-col gap-3">
        <h2 class="font-medium text-gray-900">Referti caricati</h2>

        <p v-if="referti.length === 0" class="text-sm text-gray-500">Non hai ancora caricato nessun referto.</p>

        <div v-for="r in referti" :key="r.id" class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p class="font-medium text-gray-900">{{ formatData(r.data) }}</p>
          <p class="mt-1 text-sm text-gray-600">
            {{ appuntamentoDi(r)?.paziente.nome }} {{ appuntamentoDi(r)?.paziente.cognome }} ·
            {{ prestazioneDiReferto(r)?.nome ?? 'Prestazione' }}
          </p>

          <div v-if="modificaId === r.id" class="mt-4 flex flex-col gap-3">
            <textarea v-model="formModifica.descrizione" rows="2" class="input" />
            <p v-if="erroreModifica" class="text-sm text-red-600">{{ erroreModifica }}</p>
            <div class="flex gap-3">
              <button class="btn-secondary" @click="chiudiModifica">Annulla</button>
              <button class="btn-primary" :disabled="salvataggioInCorso" @click="salvaModifica(r)">Salva</button>
            </div>
          </div>
          <template v-else>
            <p class="mt-1 text-sm text-gray-500">{{ r.descrizione ?? 'Nessuna descrizione' }}</p>
            <p v-if="erroreRiga[r.id]" class="mt-3 text-sm text-red-600">{{ erroreRiga[r.id] }}</p>
            <div class="mt-4 flex gap-3">
              <button class="btn-secondary" @click="scarica(r)">Scarica</button>
              <button class="btn-secondary" @click="apriModifica(r)">Modifica descrizione</button>
              <button class="btn-secondary" @click="elimina(r)">Elimina</button>
            </div>
          </template>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Appuntamento, Prestazione, Referto } from '../types'
import { formatData, formatDataOra } from '../utils/formato'
import { scaricaReferto } from '../utils/download'

const appuntamenti = ref<Appuntamento[]>([])
const referti = ref<Referto[]>([])
const prestazioniList = ref<Prestazione[]>([])

const caricamento = ref(true)
const errore = ref('')

const uploadAppuntamentoId = ref<number | null>(null)
const fileSelezionato = ref<File | null>(null)
const formUpload = reactive({ descrizione: '' })
const erroreUpload = ref('')
const caricamentoInCorso = ref(false)

const modificaId = ref<number | null>(null)
const formModifica = reactive({ descrizione: '' })
const erroreModifica = ref('')
const salvataggioInCorso = ref(false)
const erroreRiga = reactive<Record<number, string>>({})

onMounted(caricaTutto)

async function caricaTutto() {
  caricamento.value = true
  errore.value = ''
  try {
    const [appResp, refResp, prestResp] = await Promise.all([
      apiClient.get<Appuntamento[]>('/api/appuntamenti'),
      apiClient.get<Referto[]>('/api/referti'),
      apiClient.get<Prestazione[]>('/api/prestazioni'),
    ])
    appuntamenti.value = appResp.data
    referti.value = refResp.data
    prestazioniList.value = prestResp.data
  } catch {
    errore.value = 'Impossibile caricare i referti'
  } finally {
    caricamento.value = false
  }
}

const appuntamentiSenzaReferto = computed(() => {
  const conReferto = new Set(referti.value.map((r) => r.appuntamento_id))
  return appuntamenti.value
    .filter((a) => a.stato === 'completato' && !conReferto.has(a.id))
    .sort((a, b) => b.data_ora.localeCompare(a.data_ora))
})

function prestazioneDi(app: Appuntamento) {
  return prestazioniList.value.find((p) => p.id === app.prestazione_id)
}

function appuntamentoDi(r: Referto) {
  return appuntamenti.value.find((a) => a.id === r.appuntamento_id)
}

function prestazioneDiReferto(r: Referto) {
  const app = appuntamentoDi(r)
  return app ? prestazioniList.value.find((p) => p.id === app.prestazione_id) : undefined
}

function apriUpload(app: Appuntamento) {
  uploadAppuntamentoId.value = app.id
  fileSelezionato.value = null
  formUpload.descrizione = ''
  erroreUpload.value = ''
}

function chiudiUpload() {
  uploadAppuntamentoId.value = null
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  fileSelezionato.value = input.files?.[0] ?? null
}

async function carica(app: Appuntamento) {
  if (!fileSelezionato.value) {
    erroreUpload.value = 'Seleziona un file'
    return
  }
  erroreUpload.value = ''
  caricamentoInCorso.value = true
  const dati = new FormData()
  dati.append('file', fileSelezionato.value)
  if (formUpload.descrizione) dati.append('descrizione', formUpload.descrizione)
  try {
    await apiClient.post(`/api/appuntamenti/${app.id}/referto`, dati)
    uploadAppuntamentoId.value = null
    await caricaTutto()
  } catch (e: any) {
    erroreUpload.value = e.response?.data?.detail ?? 'Non è stato possibile caricare il referto'
  } finally {
    caricamentoInCorso.value = false
  }
}

function apriModifica(r: Referto) {
  modificaId.value = r.id
  formModifica.descrizione = r.descrizione ?? ''
  erroreModifica.value = ''
}

function chiudiModifica() {
  modificaId.value = null
}

async function salvaModifica(r: Referto) {
  erroreModifica.value = ''
  salvataggioInCorso.value = true
  try {
    const { data } = await apiClient.put<Referto>(`/api/referti/${r.id}`, {
      descrizione: formModifica.descrizione || null,
    })
    Object.assign(r, data)
    modificaId.value = null
  } catch (e: any) {
    erroreModifica.value = e.response?.data?.detail ?? 'Non è stato possibile salvare la descrizione'
  } finally {
    salvataggioInCorso.value = false
  }
}

async function scarica(r: Referto) {
  delete erroreRiga[r.id]
  try {
    await scaricaReferto(r.id, `referto-${r.appuntamento_id}`)
  } catch {
    erroreRiga[r.id] = 'Non è stato possibile scaricare il referto'
  }
}

async function elimina(r: Referto) {
  delete erroreRiga[r.id]
  if (!confirm('Vuoi eliminare questo referto?')) return
  try {
    await apiClient.delete(`/api/referti/${r.id}`)
    referti.value = referti.value.filter((x) => x.id !== r.id)
  } catch (e: any) {
    erroreRiga[r.id] = e.response?.data?.detail ?? 'Non è stato possibile eliminare il referto'
  }
}
</script>
