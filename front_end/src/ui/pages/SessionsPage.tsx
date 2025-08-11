import React, { useEffect, useState } from 'react'
import { listSessions, getHistory } from '../../shared/api'
import type { SessionSummary, HistoryResponse } from '../../shared/types'

export const SessionsPage: React.FC = () => {
  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [selected, setSelected] = useState<HistoryResponse | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    listSessions().then(setSessions).catch((e) => setError(e.message))
  }, [])

  const handleLoad = async (sid: string) => {
    setError('')
    try {
      setSelected(await getHistory(sid))
    } catch (e: any) {
      setError(e?.message || 'Load failed')
    }
  }

  return (
    <div className="grid">
      <div className="card">
        <div className="sectionTitle">Sessions</div>
        <div className="grid">
          {sessions.map((s) => (
            <div key={s.sessionId} className="actions" style={{ justifyContent: 'space-between' }}>
              <div>
                <div>{s.sheetName}</div>
                <div className="footerNote">{new Date(s.createdAt).toLocaleString()} • {s.messagesCount} msgs</div>
              </div>
              <div>
                <button className="btn" onClick={() => handleLoad(s.sessionId)}>Open</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selected && (
        <div className="card">
          <div className="sectionTitle">History</div>
          <div className="chat">
            {selected.messages.map((m, idx) => (
              <div key={idx} className={`messageRow ${m.role}`}>
                <div className={`bubble ${m.role}`}>{m.content}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}


