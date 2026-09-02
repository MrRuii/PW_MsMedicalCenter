const ETICHETTE_STATO: Record<string, string> = {
  prenotato: 'Prenotato',
  confermato: 'Confermato',
  completato: 'Completato',
  annullato: 'Annullato',
}

export function etichettaStato(stato: string): string {
  return ETICHETTE_STATO[stato] ?? stato
}

export function badgeClasse(stato: string): string {
  switch (stato) {
    case 'prenotato':
      return 'badge-giallo'
    case 'confermato':
      return 'badge-verde'
    case 'completato':
      return 'badge-grigio'
    case 'annullato':
      return 'badge-rosso'
    default:
      return 'badge-grigio'
  }
}

export function puoAnnullare(stato: string): boolean {
  return stato === 'prenotato' || stato === 'confermato'
}

export function puoCompletare(stato: string): boolean {
  return stato === 'prenotato' || stato === 'confermato'
}
