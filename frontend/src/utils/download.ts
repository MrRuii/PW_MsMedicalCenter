import apiClient from '../api/client'

export async function scaricaReferto(id: number, nomeFallback: string): Promise<void> {
  const response = await apiClient.get(`/api/referti/${id}/file`, { responseType: 'blob' })
  const disposition = response.headers['content-disposition'] as string | undefined
  const match = disposition?.match(/filename="?([^"]+)"?/)
  const nomeFile = match?.[1] ?? nomeFallback

  const url = window.URL.createObjectURL(response.data as Blob)
  const link = document.createElement('a')
  link.href = url
  link.download = nomeFile
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
