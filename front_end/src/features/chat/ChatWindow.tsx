import React from 'react'
import type { Message } from '../../shared/types'

interface ChatWindowProps {
  fileId: string | null
  sheets: string[]
  selectedSheet: string
  setSelectedSheet: (sheet: string) => void
  sessionId: string | null
  messages: Message[]
  question: string
  setQuestion: (question: string) => void
  loading: boolean
  onStartSession: () => void
  onSendMessage: () => void
  onReset: () => void
  canStart: boolean
  canSend: boolean
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  fileId,
  sheets,
  selectedSheet,
  setSelectedSheet,
  sessionId,
  messages,
  question,
  setQuestion,
  loading,
  onStartSession,
  onSendMessage,
  onReset,
  canStart,
  canSend,
}) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && canSend) {
      e.preventDefault()
      onSendMessage()
    }
  }

  return (
    <div className="chatWindow">
      <div className="chatHeader">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <div style={{ fontSize: '14px', fontWeight: 600 }}>
              {sessionId ? `Chat: ${selectedSheet}` : 'Configure Session'}
            </div>
            <div style={{ fontSize: '12px', color: 'var(--muted)' }}>
              {fileId ? `File: ${fileId.slice(0, 8)}...` : 'No file selected'}
            </div>
          </div>
          <div className="actions">
            <button className="btn" onClick={onReset} style={{ fontSize: '12px', padding: '6px 10px' }}>
              Reset
            </button>
          </div>
        </div>
        
        {!sessionId && (
          <div style={{ marginTop: 12 }}>
            <div className="row">
              <div>
                <label className="label">Select sheet</label>
                <select 
                  className="select" 
                  value={selectedSheet} 
                  onChange={(e) => setSelectedSheet(e.target.value)}
                  style={{ fontSize: '13px' }}
                >
                  {sheets.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              <div style={{ display: 'flex', alignItems: 'end' }}>
                <button 
                  className="btn btnPrimary" 
                  onClick={onStartSession} 
                  disabled={!canStart || loading}
                  style={{ fontSize: '13px' }}
                >
                  {loading ? 'Starting…' : 'Start Session'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="chatArea">
        {sessionId ? (
          <div className="chat">
            {messages.map((m, idx) => (
              <div key={idx} className={`messageRow ${m.role}`}>
                <div className={`bubble ${m.role}`}>{m.content}</div>
              </div>
            ))}
            {loading && (
              <div className="messageRow assistant">
                <div className="bubble assistant">Thinking...</div>
              </div>
            )}
          </div>
        ) : (
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center', 
            height: '100%',
            color: 'var(--muted)',
            fontSize: '14px',
            textAlign: 'center'
          }}>
            Upload a file and select a sheet to start chatting
          </div>
        )}
      </div>

      {sessionId && (
        <div className="chatInput">
          <div className="chatInputRow">
            <input
              className="input"
              placeholder="Type your question…"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
            />
            <button
              className="btn btnPrimary"
              onClick={onSendMessage}
              disabled={!canSend || loading}
            >
              {loading ? 'Sending…' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}