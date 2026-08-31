<template>
  <div class="auth-page">
    <h1>Registrazione paziente</h1>
    <form @submit.prevent="onSubmit">
      <label>
        Email
        <input v-model="form.email" type="email" required />
      </label>
      <label>
        Password
        <input v-model="form.password" type="password" required minlength="8" />
      </label>
      <label>
        Nome
        <input v-model="form.nome" required />
      </label>
      <label>
        Cognome
        <input v-model="form.cognome" required />
      </label>
      <label>
        Codice fiscale
        <input v-model="form.codice_fiscale" required />
      </label>
      <label>
        Data di nascita
        <input v-model="form.data_nascita" type="date" />
      </label>
      <label>
        Telefono
        <input v-model="form.telefono" />
      </label>
      <p v-if="errore">{{ errore }}</p>
      <p v-if="successo">Registrazione completata, ora puoi accedere.</p>
      <button type="submit" :disabled="caricamento">Registrati</button>
    </form>
    <p><router-link to="/login">Hai già un account? Accedi</router-link></p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import apiClient from "../api/client";

const form = reactive({
  email: "",
  password: "",
  nome: "",
  cognome: "",
  codice_fiscale: "",
  data_nascita: "",
  telefono: "",
});

const errore = ref("");
const successo = ref(false);
const caricamento = ref(false);

async function onSubmit() {
  errore.value = "";
  successo.value = false;
  caricamento.value = true;
  try {
    await apiClient.post("/api/auth/register", {
      ...form,
      data_nascita: form.data_nascita || null,
      telefono: form.telefono || null,
    });
    successo.value = true;
  } catch {
    errore.value = "Registrazione non riuscita, controlla i dati inseriti";
  } finally {
    caricamento.value = false;
  }
}
</script>
