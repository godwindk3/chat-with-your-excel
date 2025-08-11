import React, { useEffect, useState } from 'react'
import { listFiles } from '../api'
import type { FileInfo } from '../types'

interface FilePickerProps {
  selectedFileId?: string | null
  onFileSelect: (file: FileInfo) => void
  onError?: (error: string) => void
}

export const FilePicker: React.FC<FilePickerProps> = ({
  selectedFileId,
  onFileSelect,
  onError,
}) => {
  const [files, setFiles] = useState<FileInfo[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadFiles()
  }, [])

  const loadFiles = async () => {
    setLoading(true)
    try {
      const fileList = await listFiles()
      setFiles(fileList)
    } catch (err: any) {
      onError?.(err?.message || 'Failed to load files')
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString()
  }

  if (loading) {
    return (
      <div style={{ padding: 16, textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
        Loading files...
      </div>
    )
  }

  if (files.length === 0) {
    return (
      <div style={{ padding: 16, textAlign: 'center', color: 'var(--muted)', fontSize: '13px' }}>
        No files found in storage.<br />
        Upload a file first to see it here.
      </div>
    )
  }

  return (
    <div className="filePicker">
      {files.map((file) => (
        <div
          key={file.fileId}
          className={`filePickerItem ${selectedFileId === file.fileId ? 'selected' : ''}`}
          onClick={() => onFileSelect(file)}
        >
          <div className="filePickerInfo">
            <div className="filePickerName">{file.filename}</div>
            <div className="filePickerMeta">
              {formatFileSize(file.size)} • {formatDate(file.uploadedAt)}
            </div>
          </div>
          {selectedFileId === file.fileId && (
            <div style={{ color: 'var(--primary)', fontSize: '12px' }}>✓</div>
          )}
        </div>
      ))}
    </div>
  )
}
