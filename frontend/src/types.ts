export interface Specialita {
  id: number
  nome: string
  descrizione: string | null
}

export interface Prestazione {
  id: number
  specialita_id: number
  nome: string
  durata_min: number
  prezzo: number
}

export interface Sede {
  id: number
  nome: string
  citta: string
  indirizzo: string
}

export interface Medico {
  id: number
  nome: string
  cognome: string
  numero_albo: string | null
  specialita: Specialita[]
}

export interface Disponibilita {
  id: number
  medico_id: number
  sede_id: number
  data: string
  ora_inizio: string
  ora_fine: string
  libera: boolean
}

export interface PazienteBreve {
  id: number
  nome: string
  cognome: string
  telefono: string | null
}

export interface UtenteDettaglio {
  id: number
  email: string
  ruolo: string
  is_active: boolean
  created_at: string
  nome: string | null
  cognome: string | null
  telefono: string | null
  codice_fiscale: string | null
  numero_albo: string | null
}

export interface Appuntamento {
  id: number
  paziente_id: number
  paziente: PazienteBreve
  medico_id: number
  sede_id: number
  prestazione_id: number
  disponibilita_id: number
  data_ora: string
  stato: string
  created_at: string | null
}

export interface Referto {
  id: number
  appuntamento_id: number
  data: string
  descrizione: string | null
}
