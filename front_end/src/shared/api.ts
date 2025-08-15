import type { 
  UploadResponse, CreateSessionResponse, HistoryResponse, SessionSummary, Message, FileInfo,
  RAGUploadResponse, RAGSessionRequest, RAGSessionResponse, RAGQueryRequest, RAGQueryResponse, RAGAskRequest, RAGFileInfo
} from './types'

export const API_BASE = (import.meta as any).env.VITE_API_BASE || 'http://localhost:8000/api'

// Helper to create headers with ngrok bypass
const createHeaders = (additionalHeaders: Record<string, string> = {}) => {
  const headers: Record<string, string> = { ...additionalHeaders }
  
  // Add ngrok bypass header if using ngrok URL
  if (API_BASE.includes('ngrok')) {
    headers['ngrok-skip-browser-warning'] = 'true'
  }
  
  return headers
}

export async function uploadFile(file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/upload`, { 
    method: 'POST', 
    headers: createHeaders(),
    body: form 
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getFileInfo(fileId: string): Promise<UploadResponse> {
  const res = await fetch(`${API_BASE}/files/${fileId}/info`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function createSession(fileId: string, sheetName: string): Promise<CreateSessionResponse> {
  const res = await fetch(`${API_BASE}/session`, {
    method: 'POST', 
    headers: createHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ fileId, sheetName })
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getHistory(sessionId: string): Promise<HistoryResponse> {
  const res = await fetch(`${API_BASE}/session/${sessionId}`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function ask(sessionId: string, question: string): Promise<Message> {
  const res = await fetch(`${API_BASE}/session/${sessionId}/ask`, {
    method: 'POST', 
    headers: createHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify({ question })
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function listSessions(fileId?: string | null): Promise<SessionSummary[]> {
  const url = fileId ? `${API_BASE}/sessions?fileId=${encodeURIComponent(fileId)}` : `${API_BASE}/sessions`
  const res = await fetch(url, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function deleteSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/session/${sessionId}`, { 
    method: 'DELETE',
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
}

export async function listFiles(): Promise<FileInfo[]> {
  const res = await fetch(`${API_BASE}/files`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function deleteFile(fileId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/files/${fileId}`, { 
    method: 'DELETE',
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
}

// RAG API Functions
export async function uploadRAGFile(file: File): Promise<RAGUploadResponse> {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API_BASE}/rag/upload`, { 
    method: 'POST', 
    headers: createHeaders(),
    body: form 
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function createRAGSession(req: RAGSessionRequest): Promise<RAGSessionResponse> {
  const res = await fetch(`${API_BASE}/rag/session`, {
    method: 'POST', 
    headers: createHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(req)
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function listRAGSessions(): Promise<RAGSessionResponse[]> {
  const res = await fetch(`${API_BASE}/rag/sessions`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getRAGSession(sessionId: string): Promise<RAGSessionResponse> {
  const res = await fetch(`${API_BASE}/rag/session/${sessionId}`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function getRAGSessionMessages(sessionId: string): Promise<Message[]> {
  const res = await fetch(`${API_BASE}/rag/session/${sessionId}/messages`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function askRAGDocument(sessionId: string, req: RAGAskRequest): Promise<Message> {
  const res = await fetch(`${API_BASE}/rag/session/${sessionId}/ask`, {
    method: 'POST', 
    headers: createHeaders({ 'Content-Type': 'application/json' }),
    body: JSON.stringify(req)
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function deleteRAGSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/rag/session/${sessionId}`, { 
    method: 'DELETE',
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
}

export async function deleteRAGFile(fileId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/rag/file/${fileId}`, { 
    method: 'DELETE',
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
}

export async function listRAGFiles(): Promise<RAGFileInfo[]> {
  const res = await fetch(`${API_BASE}/rag/files`, {
    headers: createHeaders()
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}


