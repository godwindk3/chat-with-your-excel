import React, { useMemo, useState } from 'react'
import { ask, createSession, getHistory, listSessions } from '../../shared/api'
import type { Message, SessionSummary } from '../../shared/types'
import { Sidebar } from '../../features/chat/Sidebar'
import { ChatWindow } from '../../features/chat/ChatWindow'

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

  const handleStartSession = async () => {
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
    } finally { 
      setLoading(false) 
    }
  }

  const handleSendMessage = async () => {
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
    } finally { 
      setLoading(false) 
    }
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
    } finally { 
      setLoading(false) 
    }
  }

  const handleNewSession = () => {
    setSessionId(null)
    setMessages([])
    setQuestion('')
    setError('')
  }

  const handleSessionDeleted = (deletedSessionId: string) => {
    if (sessionId === deletedSessionId) {
      handleNewSession()
    }
  }

  const handleReset = () => {
    setFileId(null)
    setSheets([])
    setSelectedSheet('')
    setSessionId(null)
    setMessages([])
    setError('')
    setQuestion('')
  }

  return (
    <div className="grid">
      <div className="chatLayout">
        <Sidebar
          sessions={sessions}
          setSessions={setSessions}
          currentSessionId={sessionId}
          onLoadSession={handleLoadSession}
          onNewSession={handleNewSession}
          fileId={fileId}
          setFileId={setFileId}
          setSheets={setSheets}
          setSelectedSheet={setSelectedSheet}
          setError={setError}
          onSessionDeleted={handleSessionDeleted}
        />
        <ChatWindow
          fileId={fileId}
          sheets={sheets}
          selectedSheet={selectedSheet}
          setSelectedSheet={setSelectedSheet}
          sessionId={sessionId}
          messages={messages}
          question={question}
          setQuestion={setQuestion}
          loading={loading}
          onStartSession={handleStartSession}
          onSendMessage={handleSendMessage}
          onReset={handleReset}
          canStart={canStart}
          canSend={canSend}
        />
      </div>
      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}


