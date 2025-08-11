import type { UploadResponse, CreateSessionResponse, HistoryResponse, SessionSummary, Message, FileInfo } from './types'

export const API_BASE = (import.meta as any).env.VITE_API_BASE || 'http://localhost:8000/api'

export async function uploadFile(file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getFileInfo(fileId: string): Promise<UploadResponse> {
  const res = await fetch(`${API_BASE}/files/${fileId}/info`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function createSession(fileId: string, sheetName: string): Promise<CreateSessionResponse> {
  const res = await fetch(`${API_BASE}/session`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileId, sheetName })
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getHistory(sessionId: string): Promise<HistoryResponse> {
  const res = await fetch(`${API_BASE}/session/${sessionId}`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function ask(sessionId: string, question: string): Promise<Message> {
  const res = await fetch(`${API_BASE}/session/${sessionId}/ask`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function listSessions(fileId?: string | null): Promise<SessionSummary[]> {
  const url = fileId ? `${API_BASE}/sessions?fileId=${encodeURIComponent(fileId)}` : `${API_BASE}/sessions`
  const res = await fetch(url)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/session/${sessionId}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(await res.text())
}

export async function listFiles(): Promise<FileInfo[]> {
  const res = await fetch(`${API_BASE}/files`)
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function deleteFile(fileId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/files/${fileId}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(await res.text())
}


