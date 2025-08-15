import React, { useState, useEffect, useRef } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { 
  createRAGSession, askRAGDocument, getRAGSessionMessages, listRAGSessions 
} from '../../shared/api'
import type { RAGSessionResponse, Message } from '../../shared/types'

export const RAGChatPage: React.FC = () => {
  const [searchParams] = useSearchParams()
  const [sessions, setSessions] = useState<RAGSessionResponse[]>([])
  const [selectedSession, setSelectedSession] = useState<RAGSessionResponse | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [newSessionName, setNewSessionName] = useState('')
  const [showNewSessionForm, setShowNewSessionForm] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const fileId = searchParams.get('fileId')
  const filename = searchParams.get('filename')
  const sessionId = searchParams.get('sessionId')

  useEffect(() => {
    loadSessions()
  }, [])

  useEffect(() => {
    // If sessionId is provided in URL, select that session
    if (sessionId && sessions.length > 0) {
      const session = sessions.find(s => s.sessionId === sessionId)
      if (session) {
        setSelectedSession(session)
      }
    }
  }, [sessionId, sessions])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (selectedSession) {
      loadMessages(selectedSession.sessionId)
    }
  }, [selectedSession])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadSessions = async () => {
    try {
      const sessionList = await listRAGSessions()
      setSessions(sessionList)
    } catch (err) {
      setError('Failed to load sessions')
    }
  }

  const loadMessages = async (sessionId: string) => {
    try {
      const messageList = await getRAGSessionMessages(sessionId)
      setMessages(messageList)
    } catch (err) {
      setError('Failed to load messages')
    }
  }

  const createNewSession = async () => {
    if (!fileId || !newSessionName.trim()) return

    setCreating(true)
    setError(null)

    try {
      const session = await createRAGSession({
        fileId: fileId,
        sessionName: newSessionName.trim()
      })
      
      setSessions(prev => [session, ...prev])
      setSelectedSession(session)
      setMessages([])
      setNewSessionName('')
      setShowNewSessionForm(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create session')
    } finally {
      setCreating(false)
    }
  }

  const sendMessage = async () => {
    if (!selectedSession || !inputMessage.trim() || loading) return

    const question = inputMessage.trim()
    setInputMessage('')
    setLoading(true)
    setError(null)

    // Add user message to UI immediately
    const userMessage: Message = {
      role: 'user',
      content: question,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])

    try {
      const response = await askRAGDocument(selectedSession.sessionId, { question })
      setMessages(prev => [...prev, response])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message')
      // Remove the user message if the request failed
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="main">
      <div className="chat-container">
        {/* Sidebar */}
        <div className="chat-sidebar">
          <div className="sidebar-header">
            <h3>RAG Sessions</h3>
            {fileId && (
              <button 
                className="btn small"
                onClick={() => setShowNewSessionForm(!showNewSessionForm)}
                disabled={creating}
              >
                + New Session
              </button>
            )}
          </div>

          {showNewSessionForm && (
            <div className="new-session-form">
              <input
                type="text"
                placeholder="Session name"
                value={newSessionName}
                onChange={(e) => setNewSessionName(e.target.value)}
                disabled={creating}
              />
              <div className="form-actions">
                <button 
                  className="btn small primary"
                  onClick={createNewSession}
                  disabled={creating || !newSessionName.trim()}
                >
                  {creating ? 'Creating...' : 'Create'}
                </button>
                <button 
                  className="btn small"
                  onClick={() => setShowNewSessionForm(false)}
                  disabled={creating}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          <div className="sessions-list">
            {sessions.map(session => (
              <div
                key={session.sessionId}
                className={`session-item ${selectedSession?.sessionId === session.sessionId ? 'active' : ''}`}
                onClick={() => setSelectedSession(session)}
              >
                <div className="session-name">{session.sessionName}</div>
                <div className="session-file">{session.filename}</div>
                <div className="session-date">
                  {new Date(session.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>

          {!fileId && (
            <div className="sidebar-help">
              <p>To start a new session:</p>
              <Link to="/rag" className="btn">Upload Document</Link>
            </div>
          )}
        </div>

        {/* Chat Area */}
        <div className="chat-area">
          {selectedSession ? (
            <>
              <div className="chat-header">
                <div className="session-info">
                  <h3>{selectedSession.sessionName}</h3>
                  <p>📄 {selectedSession.filename}</p>
                </div>
              </div>

              <div className="messages-container">
                {messages.map((message, index) => (
                  <div key={index} className={`message ${message.role}`}>
                    <div className="message-content">
                      {message.content}
                    </div>
                    <div className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="message assistant loading">
                    <div className="message-content">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              <div className="chat-input-container">
                {error && (
                  <div className="error-message">{error}</div>
                )}
                <div className="chat-input">
                  <textarea
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask a question about the document..."
                    disabled={loading}
                    rows={3}
                  />
                  <button
                    onClick={sendMessage}
                    disabled={loading || !inputMessage.trim()}
                    className="send-btn"
                  >
                    {loading ? '⏳' : '➤'}
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="chat-placeholder">
              <div className="placeholder-content">
                <div className="placeholder-icon">💬</div>
                <h3>Select a session to start chatting</h3>
                <p>Choose an existing session or create a new one to chat with your documents</p>
                {!fileId && (
                  <Link to="/rag" className="btn primary">
                    Upload a Document
                  </Link>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
