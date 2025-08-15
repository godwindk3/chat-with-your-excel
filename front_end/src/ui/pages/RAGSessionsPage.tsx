import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listRAGSessions, deleteRAGSession, deleteRAGFile } from '../../shared/api'
import type { RAGSessionResponse } from '../../shared/types'

export const RAGSessionsPage: React.FC = () => {
  const [sessions, setSessions] = useState<RAGSessionResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)
  const [deletingFileId, setDeletingFileId] = useState<string | null>(null)

  useEffect(() => {
    loadSessions()
  }, [])

  const loadSessions = async () => {
    try {
      setLoading(true)
      const sessionList = await listRAGSessions()
      setSessions(sessionList)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load sessions')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteSession = async (sessionId: string) => {
    if (!confirm('Are you sure you want to delete this session? This action cannot be undone.')) {
      return
    }

    try {
      setDeletingId(sessionId)
      await deleteRAGSession(sessionId)
      setSessions(prev => prev.filter(s => s.sessionId !== sessionId))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete session')
    } finally {
      setDeletingId(null)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString()
  }

  const handleDeleteFile = async (fileId: string, filename: string) => {
    if (!confirm(`Delete file "${filename}"?\n\nThis will delete the file and ALL related sessions permanently.`)) {
      return
    }

    try {
      setDeletingFileId(fileId)
      await deleteRAGFile(fileId)
      
      // Remove all sessions related to this file
      setSessions(prev => prev.filter(s => s.fileId !== fileId))
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete file')
    } finally {
      setDeletingFileId(null)
    }
  }

  if (loading) {
    return (
      <div className="main">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading RAG sessions...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="main">
      <div className="sessions-container">
        <div className="sessions-header">
          <h2>RAG Chat Sessions</h2>
          <p>Manage your document chat sessions</p>
          <div className="header-actions">
            <Link to="/rag" className="btn primary">
              Upload New Document
            </Link>
            <Link to="/rag/chat" className="btn">
              Start Chat
            </Link>
          </div>
        </div>

        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={() => setError(null)} className="close-btn">×</button>
          </div>
        )}

        {sessions.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📄</div>
            <h3>No RAG sessions yet</h3>
            <p>Upload a document to start your first RAG chat session</p>
            <Link to="/rag" className="btn primary">
              Upload Document
            </Link>
          </div>
        ) : (
          <div className="sessions-grid">
            {sessions.map(session => (
              <div key={session.sessionId} className="session-card">
                <div className="session-card-header">
                  <div className="session-icon">💬</div>
                  <div className="session-info">
                    <h3 className="session-name">{session.sessionName}</h3>
                    <p className="session-file">📄 {session.filename}</p>
                  </div>
                </div>

                <div className="session-meta">
                  <div className="meta-item">
                    <span className="meta-label">Created:</span>
                    <span className="meta-value">{formatDate(session.createdAt)}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">File ID:</span>
                    <span className="meta-value session-id">{session.fileId}</span>
                  </div>
                </div>

                <div className="session-actions">
                  <Link
                    to={`/rag/chat?sessionId=${session.sessionId}`}
                    className="btn primary small"
                  >
                    Open Chat
                  </Link>
                  <button
                    onClick={() => handleDeleteSession(session.sessionId)}
                    disabled={deletingId === session.sessionId}
                    className="btn danger small"
                    title="Delete session only"
                  >
                    {deletingId === session.sessionId ? 'Deleting...' : 'Delete Session'}
                  </button>
                  <button
                    onClick={() => handleDeleteFile(session.fileId, session.filename)}
                    disabled={deletingFileId === session.fileId}
                    className="btn danger small"
                    title="Delete file and all related sessions"
                  >
                    {deletingFileId === session.fileId ? 'Deleting...' : '🗑️ Delete File'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="sessions-stats">
          <div className="stat-item">
            <div className="stat-number">{sessions.length}</div>
            <div className="stat-label">Total Sessions</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">
              {new Set(sessions.map(s => s.fileId)).size}
            </div>
            <div className="stat-label">Unique Documents</div>
          </div>
        </div>
      </div>
    </div>
  )
}
