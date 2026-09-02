<template>
  <div class="flex flex-col gap-6">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-semibold text-gray-900">Le mie disponibilità</h1>
        <p class="mt-1 text-sm text-gray-500">Crea, modifica ed elimina le tue fasce orarie.</p>
      </div>
      <button v-if="modalitaForm === 'chiusa'" class="btn-primary" @click="apriCrea">Nuova disponibilità</button>
    </div>

    <p v-if="errore" class="text-sm text-red-600">{{ errore }}</p>

    <section v-if="modalitaForm !== 'chiusa'" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="font-medium text-gray-900">
        {{ modalitaForm === 'crea' ? 'Nuova disponibilità' : 'Modifica disponibilità' }}
      </h2>

      <form @submit.prevent="salva" class="mt-4 grid gap-4 sm:grid-cols-2">
        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Sede</span>
          <select v-model.number="form.sede_id" required class="input">
            <option v-for="sede in sediList" :key="sede.id" :value="sede.id">{{ sede.nome }}</option>
          </select>
        </label>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Data</span>
          <input v-model="form.data" type="date" required class="input" />
        </label>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Ora inizio</span>
          <input v-model="form.ora_inizio" type="time" required class="input" />
        </label>

        <label class="flex flex-col gap-1">
          <span class="text-sm font-medium text-gray-700">Ora fine</span>
          <input v-model="form.ora_fine" type="time" required class="input" />
        </label>

        <p v-if="erroreForm" class="text-sm text-red-600 sm:col-span-2">{{ erroreForm }}</p>

        <div class="flex gap-3 sm:col-span-2">
          <button type="button" class="btn-secondary" @click="chiudiForm">Annulla</button>
          <button type="submit" class="btn-primary" :disabled="salvataggioInCorso">Salva</button>
        </div>
      </form>
    </section>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="disponibilitaOrdinate.length === 0" class="text-sm text-gray-500">
      Non hai ancora creato nessuna disponibilità.
    </p>

    <div v-else class="flex flex-col gap-3">
      <div
        v-for="d in disponibilitaOrdinate"
        :key="d.id"
        class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p class="font-medium text-gray-900">{{ formatData(d.data) }}, {{ formatOra(d.ora_inizio) }} - {{ formatOra(d.ora_fine) }}</p>
            <p class="mt-1 text-sm text-gray-500">{{ sedeDi(d)?.nome }} ({{ sedeDi(d)?.citta }})</p>
          </div>
          <span class="badge" :class="d.libera ? 'badge-verde' : 'badge-grigio'">
            {{ d.libera ? 'Libera' : 'Occupata' }}
          </span>
        </div>

        <p v-if="erroreRiga[d.id]" class="mt-3 text-sm text-red-600">{{ erroreRiga[d.id] }}</p>

        <div class="mt-4 flex gap-3">
          <button v-if="d.libera" class="btn-secondary" @click="apriModifica(d)">Modifica</button>
          <button class="btn-secondary" @click="elimina(d)">Elimina</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import { useAuthStore } from '../stores/auth'
import type { Disponibilita, Sede } from '../types'
import { formatData, formatOra } from '../utils/formato'

const authStore = useAuthStore()

const disponibilitaList = ref<Disponibilita[]>([])
const sediList = ref<Sede[]>([])

const caricamento = ref(true)
const errore = ref('')
const erroreForm = ref('')
const erroreRiga = reactive<Record<number, string>>({})
const salvataggioInCorso = ref(false)

const modalitaForm = ref<'chiusa' | 'crea' | 'modifica'>('chiusa')
const idInModifica = ref<number | null>(null)
const form = reactive({
  sede_id: null as number | null,
  data: '',
  ora_inizio: '',
  ora_fine: '',
})

onMounted(caricaTutto)

async function caricaTutto() {
  const medicoId = authStore.utente?.medico_id
  if (!medicoId) {
    errore.value = 'Utente non associato a un profilo medico'
    caricamento.value = false
    return
  }
  caricamento.value = true
  errore.value = ''
  try {
    const [dispResp, sediResp] = await Promise.all([
      apiClient.get<Disponibilita[]>(`/api/medici/${medicoId}/disponibilita`),
      apiClient.get<Sede[]>('/api/sedi'),
    ])
    disponibilitaList.value = dispResp.data
    sediList.value = sediResp.data
  } catch {
    errore.value = 'Impossibile caricare le disponibilità'
  } finally {
    caricamento.value = false
  }
}

const disponibilitaOrdinate = computed(() =>
  [...disponibilitaList.value].sort((a, b) => (a.data + a.ora_inizio).localeCompare(b.data + b.ora_inizio)),
)

function sedeDi(d: Disponibilita) {
  return sediList.value.find((s) => s.id === d.sede_id)
}

function apriCrea() {
  modalitaForm.value = 'crea'
  idInModifica.value = null
  form.sede_id = sediList.value[0]?.id ?? null
  form.data = ''
  form.ora_inizio = ''
  form.ora_fine = ''
  erroreForm.value = ''
}

function apriModifica(d: Disponibilita) {
  modalitaForm.value = 'modifica'
  idInModifica.value = d.id
  form.sede_id = d.sede_id
  form.data = d.data
  form.ora_inizio = formatOra(d.ora_inizio)
  form.ora_fine = formatOra(d.ora_fine)
  erroreForm.value = ''
}

function chiudiForm() {
  modalitaForm.value = 'chiusa'
  idInModifica.value = null
}

async function salva() {
  erroreForm.value = ''
  salvataggioInCorso.value = true
  const payload = {
    sede_id: form.sede_id,
    data: form.data,
    ora_inizio: form.ora_inizio,
    ora_fine: form.ora_fine,
  }
  try {
    if (modalitaForm.value === 'crea') {
      await apiClient.post('/api/disponibilita', payload)
    } else if (idInModifica.value !== null) {
      await apiClient.put(`/api/disponibilita/${idInModifica.value}`, payload)
    }
    modalitaForm.value = 'chiusa'
    await caricaTutto()
  } catch (e: any) {
    erroreForm.value = e.response?.data?.detail ?? 'Non è stato possibile salvare la disponibilità'
  } finally {
    salvataggioInCorso.value = false
  }
}

async function elimina(d: Disponibilita) {
  delete erroreRiga[d.id]
  if (!confirm('Vuoi eliminare questa disponibilità?')) return
  try {
    await apiClient.delete(`/api/disponibilita/${d.id}`)
    disponibilitaList.value = disponibilitaList.value.filter((x) => x.id !== d.id)
  } catch (e: any) {
    erroreRiga[d.id] = e.response?.data?.detail ?? 'Non è stato possibile eliminare la disponibilità'
  }
}
</script>
