import React, { useEffect, useMemo, useState } from 'react'

type UploadResponse = { fileId: string; filename: string; sheetNames: string[] }
type CreateSessionResponse = { sessionId: string; fileId: string; sheetName: string; createdAt: string }
type Message = { role: 'user' | 'assistant'; content: string; timestamp: string }
type HistoryResponse = { sessionId: string; fileId: string; sheetName: string; messages: Message[] }
type SessionSummary = { sessionId: string; fileId: string; sheetName: string; createdAt: string; messagesCount: number; lastMessageAt: string }

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

export const App: React.FC = () => {
  const [fileId, setFileId] = useState<string | null>(null)
  const [sheets, setSheets] = useState<string[]>([])
  const [selectedSheet, setSelectedSheet] = useState<string>('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [question, setQuestion] = useState<string>('')
  const [messages, setMessages] = useState<Message[]>([])
  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const canStart = useMemo(() => !!fileId && !!selectedSheet, [fileId, selectedSheet])
  const canSend = useMemo(() => !!sessionId && !!question.trim(), [sessionId, question])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    setError('')
    setMessages([])
    setSessionId(null)
    const form = new FormData()
    form.append('file', e.target.files[0])
    try {
      const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(await res.text())
      const data = (await res.json()) as UploadResponse
      setFileId(data.fileId)
      setSheets(data.sheetNames)
      setSelectedSheet(data.sheetNames[0] ?? '')
    } catch (err: any) {
      setError(err?.message ?? 'Upload failed')
    }
  }

  const handleStartSession = async () => {
    if (!canStart) return
    setLoading(true)
    setError('')
    setMessages([])
    try {
      const res = await fetch(`${API_BASE}/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileId, sheetName: selectedSheet })
      })
      if (!res.ok) throw new Error(await res.text())
      const data = (await res.json()) as CreateSessionResponse
      setSessionId(data.sessionId)
      // fetch history (empty initially)
      const hres = await fetch(`${API_BASE}/session/${data.sessionId}`)
      const h = (await hres.json()) as HistoryResponse
      setMessages(h.messages || [])
      // refresh sessions list
      try { const sres = await fetch(`${API_BASE}/sessions?fileId=${encodeURIComponent(data.fileId)}`); setSessions(await sres.json()); } catch {}
    } catch (err: any) {
      setError(err?.message ?? 'Start session failed')
    } finally {
      setLoading(false)
    }
  }

  const handleSend = async () => {
    if (!canSend || !sessionId) return
    const q = question.trim()
    setQuestion('')
    setMessages((m) => [...m, { role: 'user', content: q, timestamp: new Date().toISOString() }])
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE}/session/${sessionId}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      })
      if (!res.ok) throw new Error(await res.text())
      const msg = (await res.json()) as Message
      setMessages((m) => [...m, msg])
      // refresh session list quick (lastMessageAt)
      try { const sres = await fetch(`${API_BASE}/sessions?fileId=${encodeURIComponent(fileId || '')}`); setSessions(await sres.json()); } catch {}
    } catch (err: any) {
      setError(err?.message ?? 'Send failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLoadSession = async (sid: string) => {
    setSessionId(sid)
    setLoading(true)
    setError('')
    try {
      const hres = await fetch(`${API_BASE}/session/${sid}`)
      if (!hres.ok) throw new Error(await hres.text())
      const h = (await hres.json()) as HistoryResponse
      setMessages(h.messages || [])
      // set file + sheet context from summary if possible
      setFileId(h.fileId)
      setSelectedSheet(h.sheetName)
    } catch (err: any) {
      setError(err?.message ?? 'Load session failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <div className="brand">
          <div className="logo" />
          <div>
            <div className="title">Excel Analysis</div>
            <div className="subtitle">Upload Excel, pick a sheet and ask your data</div>
          </div>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <div className="sectionTitle">1. Upload</div>
          <label className="label">Upload Excel (.xlsx/.xls)</label>
          <input className="fileInput" type="file" accept=".xlsx,.xls" onChange={handleUpload} />
          {fileId && (
            <div className="fileInfo" style={{ marginTop: 8 }}>File uploaded. Select a sheet below.</div>
          )}
        </div>

        <div className="card">
          <div className="sectionTitle">2. Configure & Start</div>
          <div className="row">
            <div>
              <label className="label">Select sheet</label>
              <select className="select" value={selectedSheet} onChange={(e) => setSelectedSheet(e.target.value)}>
                {sheets.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="label">Session</label>
              <div className="actions">
                <button className="btn" onClick={() => { setFileId(null); setSheets([]); setSelectedSheet(''); setSessionId(null); setMessages([]); setError(''); }}>Reset</button>
                <button className="btn btnPrimary" onClick={handleStartSession} disabled={!canStart || loading}>
                  {loading ? 'Starting…' : (sessionId ? 'Restart' : 'Start')}
                </button>
              </div>
            </div>
          </div>
          <div className="footerNote">Tip: If your file contains a sheet named "Mô tả trường thông tin", it will be used to improve analysis.</div>
        </div>

        <div className="card">
          <div className="sectionTitle">Past Sessions</div>
          <div className="grid">
            <div className="row" style={{ gridTemplateColumns: '1fr 1fr' }}>
              <div className="actions">
                <button className="btn" onClick={async () => { try { const sres = await fetch(`${API_BASE}/sessions`); setSessions(await sres.json()); } catch {} }}>All</button>
                <button className="btn" onClick={async () => { try { const sres = await fetch(`${API_BASE}/sessions?fileId=${encodeURIComponent(fileId || '')}`); setSessions(await sres.json()); } catch {} }}>For current file</button>
              </div>
              <div className="fileInfo" style={{ alignSelf: 'end' }}>{sessions.length} found</div>
            </div>
            {sessions.map((s) => (
              <div key={s.sessionId} className="actions" style={{ justifyContent: 'space-between' }}>
                <div>
                  <div>{s.sheetName}</div>
                  <div className="footerNote">{new Date(s.createdAt).toLocaleString()} • {s.messagesCount} msgs</div>
                </div>
                <div>
                  <button className="btn" onClick={() => handleLoadSession(s.sessionId)}>Load</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <div className="sectionTitle">3. Chat</div>
          <div className="chat">
            {messages.map((m, idx) => (
              <div key={idx} className={`messageRow ${m.role}`}>
                <div className={`bubble ${m.role}`}>{m.content}</div>
              </div>
            ))}
          </div>
          <div className="chatInputRow">
            <input className="input" placeholder={sessionId ? 'Type your question…' : 'Start session first'} value={question} onChange={(e) => setQuestion(e.target.value)} disabled={!sessionId || loading} />
            <button className="btn btnPrimary" onClick={handleSend} disabled={!canSend || loading}>{loading ? 'Sending…' : 'Send'}</button>
          </div>
        </div>

        {error && (<div className="card alert alertError">{error}</div>)}
      </div>
    </div>
  )
}


