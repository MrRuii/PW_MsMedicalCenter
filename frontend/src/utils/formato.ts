export function formatData(data: string): string {
  const d = new Date(`${data}T00:00:00`)
  return d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' })
}

export function formatOra(ora: string): string {
  return ora.slice(0, 5)
}

export function formatDataOra(dataOra: string): string {
  const d = new Date(dataOra)
  return d.toLocaleDateString('it-IT', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatPrezzo(prezzo: number): string {
  return `€ ${prezzo.toFixed(2)}`
}

export function formatMese(mese: string): string {
  const d = new Date(`${mese}-01T00:00:00`)
  return d.toLocaleDateString('it-IT', { month: 'short', year: 'numeric' })
}
