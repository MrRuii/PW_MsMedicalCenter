<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">Prenota una visita</h1>
      <p class="mt-1 text-sm text-gray-500">Segui i passaggi per scegliere una visita disponibile.</p>
    </div>

    <ol class="flex items-center">
      <li v-for="(etichetta, i) in FASI" :key="etichetta" class="flex flex-1 items-center last:flex-none">
        <span
          class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-medium"
          :class="
            i + 1 < passo
              ? 'bg-accent-500 text-white'
              : i + 1 === passo
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 text-gray-500'
          "
        >
          <svg v-if="i + 1 < passo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="h-3.5 w-3.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="m5 13 4 4L19 7" />
          </svg>
          <template v-else>{{ i + 1 }}</template>
        </span>
        <span
          class="ml-2 hidden text-xs font-medium sm:inline"
          :class="i + 1 === passo ? 'text-primary-700' : 'text-gray-500'"
        >
          {{ etichetta }}
        </span>
        <span v-if="i < FASI.length - 1" class="mx-3 h-px flex-1" :class="i + 1 < passo ? 'bg-accent-400' : 'bg-gray-200'" />
      </li>
    </ol>

    <div v-if="specialitaScelta" class="flex flex-wrap gap-2">
      <button class="chip" @click="tornaA(1)">Specialità: {{ specialitaScelta.nome }}</button>
      <button v-if="prestazioneScelta" class="chip" @click="tornaA(2)">
        Prestazione: {{ prestazioneScelta.nome }}
      </button>
      <button v-if="sedeScelta" class="chip" @click="tornaA(3)">Sede: {{ sedeScelta.nome }}</button>
    </div>

    <p v-if="errore" class="text-sm text-red-600">{{ errore }}</p>

    <!-- Passo 1: specialita -->
    <section v-if="passo === 1" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="font-medium text-gray-900">1. Scegli la specialità</h2>
      <p v-if="caricamento" class="mt-4 text-sm text-gray-500">Caricamento...</p>
      <div v-else class="mt-4 grid gap-3 sm:grid-cols-2">
        <button v-for="s in specialitaList" :key="s.id" class="option-card" @click="scegliSpecialita(s)">
          <span class="font-medium text-gray-900">{{ s.nome }}</span>
          <span v-if="s.descrizione" class="mt-1 block text-xs text-gray-500">{{ s.descrizione }}</span>
        </button>
      </div>
    </section>

    <!-- Passo 2: prestazione -->
    <section v-else-if="passo === 2" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="font-medium text-gray-900">2. Scegli la prestazione</h2>
      <p v-if="caricamento" class="mt-4 text-sm text-gray-500">Caricamento...</p>
      <p v-else-if="prestazioniList.length === 0" class="mt-4 text-sm text-gray-500">
        Nessuna prestazione disponibile per questa specialità.
      </p>
      <div v-else class="mt-4 grid gap-3 sm:grid-cols-2">
        <button v-for="p in prestazioniList" :key="p.id" class="option-card" @click="scegliPrestazione(p)">
          <span class="font-medium text-gray-900">{{ p.nome }}</span>
          <span class="mt-1 block text-xs text-gray-500">{{ p.durata_min }} min · {{ formatPrezzo(p.prezzo) }}</span>
        </button>
      </div>
      <button class="btn-secondary mt-4" @click="tornaA(1)">← Indietro</button>
    </section>

    <!-- Passo 3: sede -->
    <section v-else-if="passo === 3" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="font-medium text-gray-900">3. Scegli la sede</h2>
      <p v-if="caricamento" class="mt-4 text-sm text-gray-500">Caricamento...</p>
      <div v-else class="mt-4 grid gap-3 sm:grid-cols-2">
        <button v-for="sede in sediList" :key="sede.id" class="option-card" @click="scegliSede(sede)">
          <span class="font-medium text-gray-900">{{ sede.nome }}</span>
          <span class="mt-1 block text-xs text-gray-500">{{ sede.citta }} · {{ sede.indirizzo }}</span>
        </button>
      </div>
      <button class="btn-secondary mt-4" @click="tornaA(2)">← Indietro</button>
    </section>

    <!-- Passo 4: slot liberi -->
    <section v-else-if="passo === 4" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="font-medium text-gray-900">4. Scegli data e ora</h2>
      <p v-if="caricamento" class="mt-4 text-sm text-gray-500">Caricamento...</p>
      <p v-else-if="slotList.length === 0" class="mt-4 text-sm text-gray-500">
        Non ci sono slot liberi per questa specialità in questa sede al momento.
      </p>
      <div v-else class="mt-4 grid gap-3 sm:grid-cols-2">
        <button v-for="slot in slotList" :key="slot.id" class="option-card" @click="scegliSlot(slot)">
          <span class="font-medium text-gray-900">{{ formatData(slot.data) }}, {{ formatOra(slot.ora_inizio) }}</span>
          <span class="mt-1 block text-xs text-gray-500">
            Dr. {{ medicoDiSlot(slot)?.nome }} {{ medicoDiSlot(slot)?.cognome }}
          </span>
        </button>
      </div>
      <button class="btn-secondary mt-4" @click="tornaA(3)">← Indietro</button>
    </section>

    <!-- Passo 5: conferma -->
    <section v-else-if="passo === 5" class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
      <template v-if="!prenotazioneOk">
        <h2 class="font-medium text-gray-900">5. Conferma la prenotazione</h2>
        <dl class="mt-4 grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
          <dt class="text-gray-500">Specialità</dt>
          <dd class="text-gray-900">{{ specialitaScelta?.nome }}</dd>
          <dt class="text-gray-500">Prestazione</dt>
          <dd class="text-gray-900">{{ prestazioneScelta?.nome }}</dd>
          <dt class="text-gray-500">Medico</dt>
          <dd class="text-gray-900">Dr. {{ medicoSlotScelto?.nome }} {{ medicoSlotScelto?.cognome }}</dd>
          <dt class="text-gray-500">Sede</dt>
          <dd class="text-gray-900">{{ sedeScelta?.nome }} ({{ sedeScelta?.citta }})</dd>
          <dt class="text-gray-500">Data e ora</dt>
          <dd class="text-gray-900">
            {{ slotScelto ? formatData(slotScelto.data) : '' }}, {{ slotScelto ? formatOra(slotScelto.ora_inizio) : '' }}
          </dd>
          <dt class="text-gray-500">Prezzo</dt>
          <dd class="font-medium text-gray-900">
            {{ prestazioneScelta ? formatPrezzo(prestazioneScelta.prezzo) : '' }}
          </dd>
        </dl>

        <p v-if="erroreConferma" class="mt-4 text-sm text-red-600">{{ erroreConferma }}</p>

        <div class="mt-6 flex gap-3">
          <button class="btn-secondary" @click="tornaA(4)">← Indietro</button>
          <button class="btn-primary" :disabled="caricamento" @click="confermaPrenotazione">
            Conferma prenotazione
          </button>
        </div>
      </template>

      <template v-else>
        <h2 class="font-medium text-gray-900">Prenotazione confermata</h2>
        <p class="mt-2 text-sm text-gray-600">
          La tua visita è stata prenotata. La trovi nella pagina "I miei appuntamenti".
        </p>
        <div class="mt-6 flex gap-3">
          <button class="btn-secondary" @click="nuovaPrenotazione">Prenota un'altra visita</button>
          <router-link class="btn-primary" to="/paziente/appuntamenti">Vai ai miei appuntamenti</router-link>
        </div>
      </template>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import apiClient from '../api/client'
import type { Disponibilita, Medico, Prestazione, Sede, Specialita } from '../types'

const FASI = ['Specialità', 'Prestazione', 'Sede', 'Orario', 'Conferma']

const passo = ref(1)
const caricamento = ref(false)
const errore = ref('')
const erroreConferma = ref('')
const prenotazioneOk = ref(false)

const specialitaList = ref<Specialita[]>([])
const prestazioniList = ref<Prestazione[]>([])
const sediList = ref<Sede[]>([])
const mediciList = ref<Medico[]>([])
const slotList = ref<Disponibilita[]>([])

const specialitaScelta = ref<Specialita | null>(null)
const prestazioneScelta = ref<Prestazione | null>(null)
const sedeScelta = ref<Sede | null>(null)
const slotScelto = ref<Disponibilita | null>(null)

const medicoSlotScelto = computed(() => (slotScelto.value ? medicoDiSlot(slotScelto.value) : undefined))

onMounted(caricaSpecialita)

async function caricaSpecialita() {
  caricamento.value = true
  errore.value = ''
  try {
    const { data } = await apiClient.get<Specialita[]>('/api/specialita')
    specialitaList.value = data
  } catch {
    errore.value = 'Impossibile caricare le specialità'
  } finally {
    caricamento.value = false
  }
}

async function scegliSpecialita(s: Specialita) {
  specialitaScelta.value = s
  prestazioneScelta.value = null
  errore.value = ''
  passo.value = 2
  caricamento.value = true
  try {
    const { data } = await apiClient.get<Prestazione[]>('/api/prestazioni', {
      params: { specialita_id: s.id },
    })
    prestazioniList.value = data
  } catch {
    errore.value = 'Impossibile caricare le prestazioni'
  } finally {
    caricamento.value = false
  }
}

async function scegliPrestazione(p: Prestazione) {
  prestazioneScelta.value = p
  passo.value = 3
  if (sediList.value.length > 0) return
  errore.value = ''
  caricamento.value = true
  try {
    const { data } = await apiClient.get<Sede[]>('/api/sedi')
    sediList.value = data
  } catch {
    errore.value = 'Impossibile caricare le sedi'
  } finally {
    caricamento.value = false
  }
}

async function scegliSede(sede: Sede) {
  sedeScelta.value = sede
  passo.value = 4
  await caricaSlot()
}

async function caricaSlot() {
  if (!specialitaScelta.value || !sedeScelta.value) return
  errore.value = ''
  caricamento.value = true
  slotScelto.value = null
  try {
    const [mediciResp, disponibilitaResp] = await Promise.all([
      apiClient.get<Medico[]>('/api/medici', { params: { specialita_id: specialitaScelta.value.id } }),
      apiClient.get<Disponibilita[]>('/api/disponibilita', { params: { sede_id: sedeScelta.value.id } }),
    ])
    mediciList.value = mediciResp.data
    const mediciIds = new Set(mediciResp.data.map((m) => m.id))
    slotList.value = disponibilitaResp.data
      .filter((d) => mediciIds.has(d.medico_id))
      .sort((a, b) => (a.data + a.ora_inizio).localeCompare(b.data + b.ora_inizio))
  } catch {
    errore.value = 'Impossibile caricare gli slot disponibili'
  } finally {
    caricamento.value = false
  }
}

function medicoDiSlot(slot: Disponibilita): Medico | undefined {
  return mediciList.value.find((m) => m.id === slot.medico_id)
}

function scegliSlot(slot: Disponibilita) {
  slotScelto.value = slot
  erroreConferma.value = ''
  passo.value = 5
}

async function confermaPrenotazione() {
  if (!slotScelto.value || !prestazioneScelta.value) return
  erroreConferma.value = ''
  caricamento.value = true
  try {
    await apiClient.post('/api/appuntamenti', {
      disponibilita_id: slotScelto.value.id,
      prestazione_id: prestazioneScelta.value.id,
    })
    prenotazioneOk.value = true
  } catch (e: any) {
    if (e.response?.status === 409) {
      erroreConferma.value = 'Questo slot è stato appena prenotato da un altro paziente. Scegline un altro.'
      passo.value = 4
      await caricaSlot()
    } else {
      erroreConferma.value = 'Non è stato possibile completare la prenotazione'
    }
  } finally {
    caricamento.value = false
  }
}

function tornaA(destinazione: number) {
  errore.value = ''
  passo.value = destinazione
}

function nuovaPrenotazione() {
  passo.value = 1
  specialitaScelta.value = null
  prestazioneScelta.value = null
  sedeScelta.value = null
  slotScelto.value = null
  prenotazioneOk.value = false
  erroreConferma.value = ''
}

function formatData(data: string): string {
  const d = new Date(`${data}T00:00:00`)
  return d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' })
}

function formatOra(ora: string): string {
  return ora.slice(0, 5)
}

function formatPrezzo(prezzo: number): string {
  return `€ ${prezzo.toFixed(2)}`
}
</script>
