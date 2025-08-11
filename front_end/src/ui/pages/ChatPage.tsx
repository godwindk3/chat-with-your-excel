import React, { useMemo, useState } from 'react'
import { ask, createSession, getHistory, uploadFile, listSessions } from '../../shared/api'
import type { Message, SessionSummary } from '../../shared/types'

export const ChatPage: React.FC = () => {
  const [fileId, setFileId] = useState<string | null>(null)
  const [sheets, setSheets] = useState<string[]>([])
  const [selectedSheet, setSelectedSheet] = useState<string>('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [question, setQuestion] = useState<string>('')
  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const canStart = useMemo(() => !!fileId && !!selectedSheet, [fileId, selectedSheet])
  const canSend = useMemo(() => !!sessionId && !!question.trim(), [sessionId, question])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    setError('')
    setMessages([])
    setSessionId(null)
    try {
      const res = await uploadFile(e.target.files[0])
      setFileId(res.fileId)
      setSheets(res.sheetNames)
      setSelectedSheet(res.sheetNames[0] || '')
      const s = await listSessions(res.fileId)
      setSessions(s)
    } catch (err: any) {
      setError(err?.message || 'Upload failed')
    }
  }

  const handleStart = async () => {
    if (!canStart) return
    setLoading(true)
    setError('')
    setMessages([])
    try {
      const s = await createSession(fileId!, selectedSheet)
      setSessionId(s.sessionId)
      const h = await getHistory(s.sessionId)
      setMessages(h.messages || [])
      setSessions(await listSessions(s.fileId))
    } catch (err: any) {
      setError(err?.message || 'Start session failed')
    } finally { setLoading(false) }
  }

  const handleSend = async () => {
    if (!canSend || !sessionId) return
    const q = question.trim()
    setQuestion('')
    setMessages((m) => [...m, { role: 'user', content: q, timestamp: new Date().toISOString() }])
    setLoading(true)
    setError('')
    try {
      const msg = await ask(sessionId, q)
      setMessages((m) => [...m, msg])
      setSessions(await listSessions(fileId || undefined))
    } catch (err: any) {
      setError(err?.message || 'Send failed')
    } finally { setLoading(false) }
  }

  const handleLoadSession = async (sid: string) => {
    setLoading(true)
    setError('')
    try {
      const h = await getHistory(sid)
      setSessionId(h.sessionId)
      setFileId(h.fileId)
      setSelectedSheet(h.sheetName)
      setMessages(h.messages || [])
    } catch (err: any) {
      setError(err?.message || 'Load session failed')
    } finally { setLoading(false) }
  }

  return (
    <div className="grid">
      <div className="card">
        <div className="sectionTitle">1. Upload</div>
        <label className="label">Upload Excel (.xlsx/.xls)</label>
        <input className="fileInput" type="file" accept=".xlsx,.xls" onChange={handleUpload} />
      </div>

      <div className="card">
        <div className="sectionTitle">2. Configure & Start</div>
        <div className="row">
          <div>
            <label className="label">Select sheet</label>
            <select className="select" value={selectedSheet} onChange={(e) => setSelectedSheet(e.target.value)}>
              {sheets.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Session</label>
            <div className="actions">
              <button className="btn" onClick={() => { setFileId(null); setSheets([]); setSelectedSheet(''); setSessionId(null); setMessages([]); setError(''); }}>Reset</button>
              <button className="btn btnPrimary" onClick={handleStart} disabled={!canStart || loading}>{loading ? 'Starting…' : (sessionId ? 'Restart' : 'Start')}</button>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="sectionTitle">Past Sessions</div>
        <div className="grid">
          <div className="row" style={{ gridTemplateColumns: '1fr 1fr' }}>
            <div className="actions">
              <button className="btn" onClick={async () => setSessions(await listSessions())}>All</button>
              <button className="btn" onClick={async () => setSessions(await listSessions(fileId || undefined))}>For current file</button>
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

      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}


