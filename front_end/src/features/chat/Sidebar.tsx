import React, { useEffect, useState } from 'react'
import { listSessions, uploadFile, deleteSession, getFileInfo } from '../../shared/api'
import { FilePicker } from '../../shared/components/FilePicker'
import type { SessionSummary, FileInfo } from '../../shared/types'

interface SidebarProps {
  sessions: SessionSummary[]
  setSessions: (sessions: SessionSummary[]) => void
  currentSessionId: string | null
  onLoadSession: (sessionId: string) => void
  onNewSession: () => void
  fileId: string | null
  setFileId: (fileId: string | null) => void
  setSheets: (sheets: string[]) => void
  setSelectedSheet: (sheet: string) => void
  setError: (error: string) => void
  onSessionDeleted?: (sessionId: string) => void
}

export const Sidebar: React.FC<SidebarProps> = ({
  sessions,
  setSessions,
  currentSessionId,
  onLoadSession,
  onNewSession,
  fileId,
  setFileId,
  setSheets,
  setSelectedSheet,
  setError,
  onSessionDeleted,
}) => {
  const [uploadMode, setUploadMode] = useState<'upload' | 'select'>('upload')

  useEffect(() => {
    listSessions().then(setSessions).catch(() => {})
  }, [setSessions])

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    setError('')
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

  const refreshSessions = async (forCurrentFile: boolean = false) => {
    try {
      const s = await listSessions(forCurrentFile ? fileId : undefined)
      setSessions(s)
    } catch (err) {
      setError('Failed to load sessions')
    }
  }

  const handleFileSelect = async (file: FileInfo) => {
    setError('')
    try {
      const res = await getFileInfo(file.fileId)
      setFileId(res.fileId)
      setSheets(res.sheetNames)
      setSelectedSheet(res.sheetNames[0] || '')
      const s = await listSessions(res.fileId)
      setSessions(s)
    } catch (err: any) {
      setError(err?.message || 'Failed to load file info')
    }
  }

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    if (!confirm('Delete this session? This cannot be undone.')) return
    
    try {
      await deleteSession(sessionId)
      setSessions(sessions.filter(s => s.sessionId !== sessionId))
      if (currentSessionId === sessionId) {
        onSessionDeleted?.(sessionId)
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to delete session')
    }
  }

  return (
    <div className="sidebar">
      <div className="sidebarHeader">
        <div className="sidebarTitle">Chat Sessions</div>
        <button className="btn newSessionBtn btnPrimary" onClick={onNewSession}>
          + New Session
        </button>
        
        <div style={{ marginBottom: 12 }}>
          <div className="uploadTabs" style={{ marginBottom: 8 }}>
            <button 
              className={`uploadTab ${uploadMode === 'upload' ? 'active' : ''}`}
              onClick={() => setUploadMode('upload')}
            >
              Upload
            </button>
            <button 
              className={`uploadTab ${uploadMode === 'select' ? 'active' : ''}`}
              onClick={() => setUploadMode('select')}
            >
              Storage
            </button>
          </div>

          {uploadMode === 'upload' ? (
            <>
              <label className="label">Upload Excel</label>
              <input 
                className="fileInput" 
                type="file" 
                accept=".xlsx,.xls" 
                onChange={handleUpload}
                style={{ fontSize: '11px', padding: '6px 8px' }}
              />
            </>
          ) : (
            <>
              <label className="label">Select from storage</label>
              <FilePicker 
                selectedFileId={fileId}
                onFileSelect={handleFileSelect}
                onError={setError}
              />
            </>
          )}
        </div>
        
        <div className="actions" style={{ gap: '4px' }}>
          <button className="btn" onClick={() => refreshSessions(false)} style={{ fontSize: '11px', padding: '4px 8px' }}>
            All
          </button>
          <button className="btn" onClick={() => refreshSessions(true)} style={{ fontSize: '11px', padding: '4px 8px' }}>
            Current File
          </button>
        </div>
      </div>
      
      <div className="sessionsList">
        {sessions.map((session) => (
          <div
            key={session.sessionId}
            className={`sessionItem ${currentSessionId === session.sessionId ? 'active' : ''}`}
            onClick={() => onLoadSession(session.sessionId)}
          >
            <div className="sessionItemContent">
              <div className="sessionInfo">
                <div className="sessionTitle">{session.sheetName}</div>
                <div className="sessionMeta">
                  {new Date(session.createdAt).toLocaleDateString()} • {session.messagesCount} msgs
                </div>
              </div>
              <div className="sessionActions">
                <button 
                  className="btn deleteBtn" 
                  onClick={(e) => handleDeleteSession(session.sessionId, e)}
                  title="Delete session"
                >
                  ×
                </button>
              </div>
            </div>
          </div>
        ))}
        {sessions.length === 0 && (
          <div style={{ padding: 16, textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
            No sessions found.<br />Upload a file to start.
          </div>
        )}
      </div>
    </div>
  )
}