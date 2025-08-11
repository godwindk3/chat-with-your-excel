import React, { useEffect, useState } from 'react'
import { listFiles, deleteFile } from '../../shared/api'
import type { FileInfo } from '../../shared/types'

export const FilesPage: React.FC = () => {
  const [files, setFiles] = useState<FileInfo[]>([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadFiles()
  }, [])

  const loadFiles = async () => {
    setLoading(true)
    setError('')
    try {
      const fileList = await listFiles()
      setFiles(fileList)
    } catch (err: any) {
      setError(err?.message || 'Failed to load files')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteFile = async (fileId: string) => {
    if (!confirm('Delete this file? This will also delete all related sessions. This cannot be undone.')) return
    
    try {
      await deleteFile(fileId)
      setFiles(files.filter(f => f.fileId !== fileId))
    } catch (err: any) {
      setError(err?.message || 'Failed to delete file')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  return (
    <div className="grid">
      <div className="card">
        <div className="sectionTitle">File Management</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div className="fileInfo">{files.length} files in storage</div>
          <button className="btn" onClick={loadFiles} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
        
        <div className="grid">
          {files.map((file) => (
            <div key={file.fileId} className="card" style={{ padding: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontWeight: 500, fontSize: '14px', marginBottom: 4 }}>
                    {file.filename}
                  </div>
                  <div className="footerNote">
                    ID: {file.fileId.slice(0, 8)}... • {formatFileSize(file.size)} • {formatDate(file.uploadedAt)}
                  </div>
                </div>
                <button 
                  className="btn deleteBtn" 
                  onClick={() => handleDeleteFile(file.fileId)}
                  style={{ marginLeft: 12 }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
          
          {files.length === 0 && !loading && (
            <div style={{ 
              padding: 32, 
              textAlign: 'center', 
              color: 'var(--muted)', 
              fontSize: '14px' 
            }}>
              No files found in storage.<br />
              Upload files from the Chat page to see them here.
            </div>
          )}
        </div>
      </div>
      
      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}
