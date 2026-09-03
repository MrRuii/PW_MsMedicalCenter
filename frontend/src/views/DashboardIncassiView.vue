<template>
  <div class="flex flex-col gap-6">
    <div>
      <h1 class="text-2xl font-semibold text-gray-900">Dashboard incassi</h1>
      <p class="mt-1 text-sm text-gray-500">Panoramica degli incassi e gestione dei pagamenti.</p>
    </div>

    <div class="flex flex-wrap items-end gap-3 rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <div>
        <label class="block text-xs font-medium text-gray-500">Da</label>
        <input v-model="da" type="date" class="input" />
      </div>
      <div>
        <label class="block text-xs font-medium text-gray-500">A</label>
        <input v-model="a" type="date" class="input" />
      </div>
      <button class="btn-primary" @click="applicaFiltro">Applica</button>
      <button class="btn-secondary" @click="azzeraFiltro">Tutti i periodi</button>
    </div>

    <p v-if="caricamento" class="text-sm text-gray-500">Caricamento...</p>
    <p v-else-if="errore" class="text-sm text-red-600">{{ errore }}</p>

    <template v-else>
      <div class="grid gap-4 sm:grid-cols-3">
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-sm text-gray-500">Incasso totale</p>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{{ formatPrezzo(kpi?.incasso_totale ?? 0) }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-sm text-gray-500">Prestazioni pagate</p>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{{ kpi?.numero_prestazioni ?? 0 }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <p class="text-sm text-gray-500">Ticket medio</p>
          <p class="mt-1 text-2xl font-semibold text-gray-900">{{ formatPrezzo(kpi?.ticket_medio ?? 0) }}</p>
        </div>
      </div>

      <div class="grid gap-4 lg:grid-cols-2">
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <h2 class="font-medium text-gray-900">Incassi per specialità</h2>
          <p v-if="incassiSpecialita.length === 0" class="mt-4 text-sm text-gray-500">Nessun dato per il periodo selezionato.</p>
          <div v-show="incassiSpecialita.length > 0" class="mt-4" style="height: 260px">
            <canvas ref="chartSpecialitaRef"></canvas>
          </div>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-5 shadow-sm">
          <h2 class="font-medium text-gray-900">Andamento mensile</h2>
          <p v-if="incassiMese.length === 0" class="mt-4 text-sm text-gray-500">Nessun dato per il periodo selezionato.</p>
          <div v-show="incassiMese.length > 0" class="mt-4" style="height: 260px">
            <canvas ref="chartMeseRef"></canvas>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-3">
        <h2 class="font-medium text-gray-900">Pagamenti</h2>
        <p v-if="righeTabella.length === 0" class="text-sm text-gray-500">
          Nessun appuntamento completato nel periodo selezionato.
        </p>
        <div v-else class="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-left text-xs font-medium uppercase text-gray-500">
              <tr>
                <th class="px-4 py-3">Data</th>
                <th class="px-4 py-3">Paziente</th>
                <th class="px-4 py-3">Prestazione</th>
                <th class="px-4 py-3">Importo</th>
                <th class="px-4 py-3">Stato</th>
                <th class="px-4 py-3">Azione</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="riga in righeTabella" :key="riga.appuntamento.id">
                <td class="px-4 py-3 whitespace-nowrap">{{ formatDataOra(riga.appuntamento.data_ora) }}</td>
                <td class="px-4 py-3">{{ riga.appuntamento.paziente.nome }} {{ riga.appuntamento.paziente.cognome }}</td>
                <td class="px-4 py-3">{{ riga.prestazione?.nome ?? 'Prestazione' }}</td>
                <td class="px-4 py-3">{{ riga.pagamento ? formatPrezzo(riga.pagamento.importo) : '—' }}</td>
                <td class="px-4 py-3">
                  <span
                    v-if="riga.pagamento"
                    class="badge"
                    :class="riga.pagamento.stato === 'pagato' ? 'badge-verde' : 'badge-rosso'"
                  >
                    {{ riga.pagamento.stato === 'pagato' ? 'Pagato' : 'Rimborsato' }}
                  </span>
                  <span v-else class="badge badge-giallo">Da incassare</span>
                </td>
                <td class="px-4 py-3">
                  <template v-if="!riga.pagamento">
                    <div v-if="registrazioneAppId === riga.appuntamento.id" class="flex flex-col gap-2">
                      <input v-model="formRegistrazione.importo" type="number" step="0.01" min="0.01" class="input w-28" />
                      <p v-if="erroreRegistrazione" class="text-xs text-red-600">{{ erroreRegistrazione }}</p>
                      <div class="flex gap-2">
                        <button class="btn-secondary" @click="chiudiRegistrazione">Annulla</button>
                        <button class="btn-primary" :disabled="registrazioneInCorso" @click="confermaRegistrazione(riga)">
                          Conferma
                        </button>
                      </div>
                    </div>
                    <button v-else class="btn-secondary" @click="apriRegistrazione(riga)">Registra incasso</button>
                  </template>
                  <template v-else-if="riga.pagamento.stato === 'pagato'">
                    <button class="btn-secondary" @click="rimborsa(riga.pagamento)">Rimborsa</button>
                  </template>
                  <span v-else class="text-gray-400">—</span>
                  <p v-if="riga.pagamento && erroreRiga[riga.pagamento.id]" class="mt-1 text-xs text-red-600">
                    {{ erroreRiga[riga.pagamento.id] }}
                  </p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { Chart, registerables } from 'chart.js'
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import apiClient from '../api/client'
import type { Appuntamento, DashboardKPI, IncassoRaggruppato, Pagamento, Prestazione } from '../types'
import { formatDataOra, formatMese, formatPrezzo } from '../utils/formato'

Chart.register(...registerables)

interface RigaPagamento {
  appuntamento: Appuntamento
  pagamento: Pagamento | null
  prestazione: Prestazione | undefined
}

const da = ref('')
const a = ref('')

const appuntamenti = ref<Appuntamento[]>([])
const prestazioniList = ref<Prestazione[]>([])
const pagamenti = ref<Pagamento[]>([])
const kpi = ref<DashboardKPI | null>(null)
const incassiSpecialita = ref<IncassoRaggruppato[]>([])
const incassiMese = ref<IncassoRaggruppato[]>([])

const caricamento = ref(true)
const errore = ref('')

const registrazioneAppId = ref<number | null>(null)
const formRegistrazione = reactive({ importo: '' })
const erroreRegistrazione = ref('')
const registrazioneInCorso = ref(false)
const erroreRiga = reactive<Record<number, string>>({})

const chartSpecialitaRef = ref<HTMLCanvasElement | null>(null)
const chartMeseRef = ref<HTMLCanvasElement | null>(null)
let chartSpecialita: Chart | null = null
let chartMese: Chart | null = null

onMounted(caricaTutto)
onBeforeUnmount(() => {
  chartSpecialita?.destroy()
  chartMese?.destroy()
})

function parametriPeriodo() {
  const params: Record<string, string> = {}
  if (da.value) params.da = da.value
  if (a.value) params.a = a.value
  return params
}

async function caricaTutto() {
  caricamento.value = true
  errore.value = ''
  try {
    const [appResp, prestResp, pagResp] = await Promise.all([
      apiClient.get<Appuntamento[]>('/api/appuntamenti'),
      apiClient.get<Prestazione[]>('/api/prestazioni'),
      apiClient.get<Pagamento[]>('/api/pagamenti'),
    ])
    appuntamenti.value = appResp.data
    prestazioniList.value = prestResp.data
    pagamenti.value = pagResp.data
    await caricaKpiEIncassi()
  } catch {
    errore.value = 'Impossibile caricare la dashboard'
  } finally {
    caricamento.value = false
  }
  await nextTick()
  disegnaGrafici()
}

async function caricaKpiEIncassi() {
  const params = parametriPeriodo()
  const [kpiResp, specResp, meseResp] = await Promise.all([
    apiClient.get<DashboardKPI>('/api/dashboard/kpi', { params }),
    apiClient.get<IncassoRaggruppato[]>('/api/dashboard/incassi', { params: { ...params, raggruppa: 'specialita' } }),
    apiClient.get<IncassoRaggruppato[]>('/api/dashboard/incassi', { params: { ...params, raggruppa: 'mese' } }),
  ])
  kpi.value = kpiResp.data
  incassiSpecialita.value = specResp.data
  incassiMese.value = meseResp.data
}

async function applicaFiltro() {
  errore.value = ''
  try {
    await caricaKpiEIncassi()
    await nextTick()
    disegnaGrafici()
  } catch {
    errore.value = 'Impossibile aggiornare i dati del periodo'
  }
}

function azzeraFiltro() {
  da.value = ''
  a.value = ''
  applicaFiltro()
}

function disegnaGrafici() {
  if (chartSpecialitaRef.value) {
    chartSpecialita?.destroy()
    chartSpecialita = new Chart(chartSpecialitaRef.value, {
      type: 'bar',
      data: {
        labels: incassiSpecialita.value.map((d) => d.etichetta),
        datasets: [{ label: 'Incasso (€)', data: incassiSpecialita.value.map((d) => d.totale), backgroundColor: '#1597f5' }],
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
    })
  }

  if (chartMeseRef.value) {
    chartMese?.destroy()
    chartMese = new Chart(chartMeseRef.value, {
      type: 'line',
      data: {
        labels: incassiMese.value.map((d) => formatMese(d.etichetta)),
        datasets: [
          {
            label: 'Incasso (€)',
            data: incassiMese.value.map((d) => d.totale),
            borderColor: '#41a97b',
            backgroundColor: '#daf1e7',
            tension: 0.3,
            fill: true,
          },
        ],
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } },
    })
  }
}

const righeTabella = computed<RigaPagamento[]>(() => {
  const inizio = da.value ? new Date(`${da.value}T00:00:00`) : null
  const fine = a.value ? new Date(`${a.value}T23:59:59`) : null
  return appuntamenti.value
    .filter((app) => app.stato === 'completato')
    .filter((app) => {
      const dataApp = new Date(app.data_ora)
      if (inizio && dataApp < inizio) return false
      if (fine && dataApp > fine) return false
      return true
    })
    .map((app) => ({
      appuntamento: app,
      pagamento: pagamenti.value.find((p) => p.appuntamento_id === app.id) ?? null,
      prestazione: prestazioniList.value.find((p) => p.id === app.prestazione_id),
    }))
    .sort((x, y) => y.appuntamento.data_ora.localeCompare(x.appuntamento.data_ora))
})

function apriRegistrazione(riga: RigaPagamento) {
  registrazioneAppId.value = riga.appuntamento.id
  formRegistrazione.importo = riga.prestazione ? String(riga.prestazione.prezzo) : ''
  erroreRegistrazione.value = ''
}

function chiudiRegistrazione() {
  registrazioneAppId.value = null
}

function messaggioErrore(e: any, messaggioDefault: string): string {
  const dettaglio = e.response?.data?.detail
  if (typeof dettaglio === 'string') return dettaglio
  return messaggioDefault
}

async function confermaRegistrazione(riga: RigaPagamento) {
  erroreRegistrazione.value = ''
  const importo = formRegistrazione.importo ? Number(formRegistrazione.importo) : null
  if (importo !== null && (Number.isNaN(importo) || importo <= 0)) {
    erroreRegistrazione.value = "L'importo deve essere maggiore di zero"
    return
  }
  registrazioneInCorso.value = true
  try {
    const { data } = await apiClient.post<Pagamento>(`/api/appuntamenti/${riga.appuntamento.id}/pagamento`, { importo })
    pagamenti.value.push(data)
    registrazioneAppId.value = null
    await applicaFiltro()
  } catch (e: any) {
    erroreRegistrazione.value = messaggioErrore(e, 'Non è stato possibile registrare il pagamento')
  } finally {
    registrazioneInCorso.value = false
  }
}

async function rimborsa(pagamento: Pagamento) {
  delete erroreRiga[pagamento.id]
  if (!confirm('Vuoi segnare questo pagamento come rimborsato?')) return
  try {
    const { data } = await apiClient.patch<Pagamento>(`/api/pagamenti/${pagamento.id}/rimborsa`)
    Object.assign(pagamento, data)
    await applicaFiltro()
  } catch (e: any) {
    erroreRiga[pagamento.id] = messaggioErrore(e, 'Non è stato possibile rimborsare il pagamento')
  }
}
</script>
