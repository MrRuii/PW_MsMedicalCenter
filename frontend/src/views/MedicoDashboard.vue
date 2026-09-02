<template>
  <div class="flex flex-col gap-6">
    <div class="rounded-lg border border-gray-200 bg-white p-8 shadow-sm">
      <h1 class="text-2xl font-semibold text-gray-900">Area medico</h1>
      <p class="mt-2 text-gray-500">Da qui puoi consultare la tua agenda e gestire le tue disponibilità.</p>
    </div>

    <div class="grid gap-4 sm:grid-cols-2">
      <router-link
        to="/medico/agenda"
        class="group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:border-primary-300 hover:shadow-md"
      >
        <span class="flex h-10 w-10 items-center justify-center rounded-md bg-primary-100 text-primary-700">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2m-6 9 2 2 4-4" />
          </svg>
        </span>
        <span class="mt-4 block font-medium text-gray-900 group-hover:text-primary-700">La mia agenda</span>
        <span class="mt-1 block text-sm text-gray-500">Appuntamenti del giorno e della settimana</span>
      </router-link>

      <router-link
        to="/medico/disponibilita"
        class="group rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition hover:border-accent-300 hover:shadow-md"
      >
        <span class="flex h-10 w-10 items-center justify-center rounded-md bg-accent-100 text-accent-800">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2Z" />
          </svg>
        </span>
        <span class="mt-4 block font-medium text-gray-900 group-hover:text-accent-800">Le mie disponibilità</span>
        <span class="mt-1 block text-sm text-gray-500">Crea, modifica ed elimina le tue fasce orarie</span>
      </router-link>
    </div>
  </div>
</template>
