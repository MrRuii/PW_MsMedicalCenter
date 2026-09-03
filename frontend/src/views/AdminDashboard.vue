<template>
  <div class="flex flex-col gap-6">
    <div class="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
      <h1 class="text-2xl font-semibold text-gray-900">Area amministratore</h1>
      <p class="mt-2 text-gray-500">Da qui puoi gestire gli utenti registrati.</p>
    </div>

    <div class="grid gap-4 sm:grid-cols-2">
      <router-link
        to="/admin/utenti"
        class="group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:border-accent-300 hover:shadow-md"
      >
        <span class="flex h-10 w-10 items-center justify-center rounded-md bg-accent-100 text-accent-800">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-1a4 4 0 0 0-3-3.87M9 20H4v-1a4 4 0 0 1 3-3.87m5-3.13a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7-3a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm-14 0a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
          </svg>
        </span>
        <span class="mt-4 block font-medium text-gray-900 group-hover:text-accent-800">Gestione utenti</span>
        <span class="mt-1 block text-sm text-gray-500">Elenco utenti, modifica dati e stato attivo</span>
      </router-link>

      <router-link
        to="/admin/nuovo-medico"
        class="group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:border-primary-300 hover:shadow-md"
      >
        <span class="flex h-10 w-10 items-center justify-center rounded-md bg-primary-100 text-primary-700">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7ZM4 20c0-3.5 3.5-6 8-6s8 2.5 8 6M18 8v4m2-2h-4" />
          </svg>
        </span>
        <span class="mt-4 block font-medium text-gray-900 group-hover:text-primary-700">Crea medico</span>
        <span class="mt-1 block text-sm text-gray-500">Nuovo account medico e sue specialità</span>
      </router-link>

      <router-link
        to="/admin/dashboard"
        class="group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:border-accent-300 hover:shadow-md"
      >
        <span class="flex h-10 w-10 items-center justify-center rounded-md bg-accent-100 text-accent-800">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18M7 15l4-5 3 3 5-7" />
          </svg>
        </span>
        <span class="mt-4 block font-medium text-gray-900 group-hover:text-accent-800">Dashboard incassi</span>
        <span class="mt-1 block text-sm text-gray-500">KPI, andamento incassi e registrazione pagamenti</span>
      </router-link>
    </div>
  </div>
</template>
