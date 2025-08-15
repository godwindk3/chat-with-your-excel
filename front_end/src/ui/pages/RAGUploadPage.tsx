import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { uploadRAGFile, listRAGFiles } from '../../shared/api'
import type { RAGUploadResponse, RAGFileInfo } from '../../shared/types'

export const RAGUploadPage: React.FC = () => {
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<RAGUploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [ragFiles, setRAGFiles] = useState<RAGFileInfo[]>([])
  const [loadingFiles, setLoadingFiles] = useState(true)
  const [selectedTab, setSelectedTab] = useState<'upload' | 'existing'>('upload')

  useEffect(() => {
    loadRAGFiles()
  }, [])

  const loadRAGFiles = async () => {
    try {
      setLoadingFiles(true)
      const files = await listRAGFiles()
      setRAGFiles(files)
    } catch (err) {
      console.error('Failed to load RAG files:', err)
    } finally {
      setLoadingFiles(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file type
    const allowedTypes = ['.txt', '.docx', '.pdf']
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!allowedTypes.includes(fileExtension)) {
      setError('Only .txt, .docx, and .pdf files are supported for RAG')
      return
    }

    setUploading(true)
    setError(null)
    setUploadResult(null)

    try {
      const result = await uploadRAGFile(file)
      setUploadResult(result)
      // Reload files list after successful upload
      loadRAGFiles()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString()
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType) {
      case 'pdf': return '📄'
      case 'docx': return '📝'
      case 'txt': return '📄'
      default: return '📄'
    }
  }

  return (
    <div className="main">
      <div className="upload-container">
        <div className="upload-section">
          <div className="upload-header">
            <div className="upload-icon">📄</div>
            <h2>RAG Documents</h2>
            <p>Upload new documents or choose from existing ones to start chatting</p>
          </div>

          {/* Tabs */}
          <div className="upload-tabs">
            <button 
              className={`upload-tab ${selectedTab === 'upload' ? 'active' : ''}`}
              onClick={() => setSelectedTab('upload')}
            >
              📤 Upload New
            </button>
            <button 
              className={`upload-tab ${selectedTab === 'existing' ? 'active' : ''}`}
              onClick={() => setSelectedTab('existing')}
            >
              📂 Choose Existing ({ragFiles.length})
            </button>
          </div>

          {/* Upload Tab Content */}
          {selectedTab === 'upload' && (
            <div className="upload-dropzone">
            <input
              type="file"
              id="rag-file-input"
              accept=".txt,.docx,.pdf"
              onChange={handleFileUpload}
              disabled={uploading}
              style={{ display: 'none' }}
            />
            <label htmlFor="rag-file-input" className={`upload-label ${uploading ? 'uploading' : ''}`}>
              {uploading ? (
                <>
                  <div className="spinner"></div>
                  <span>Processing document...</span>
                </>
              ) : (
                <>
                  <div className="upload-icon-large">📁</div>
                  <span>Click to select a document</span>
                  <small>Supports .txt, .docx, .pdf files</small>
                </>
              )}
            </label>
            </div>
          )}

          {/* Existing Files Tab Content */}
          {selectedTab === 'existing' && (
            <div className="existing-files-section">
              {loadingFiles ? (
                <div className="loading-container">
                  <div className="spinner"></div>
                  <span>Loading documents...</span>
                </div>
              ) : ragFiles.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">📄</div>
                  <h3>No documents found</h3>
                  <p>Upload your first document to get started</p>
                  <button 
                    className="btn primary"
                    onClick={() => setSelectedTab('upload')}
                  >
                    Upload Document
                  </button>
                </div>
              ) : (
                <div className="files-grid">
                  {ragFiles.map(file => (
                    <div key={file.fileId} className="file-card">
                      <div className="file-card-header">
                        <div className="file-icon">{getFileIcon(file.fileType)}</div>
                        <div className="file-info">
                          <h4 className="file-name">{file.filename}</h4>
                          <div className="file-meta">
                            <span className="file-type">{file.fileType.toUpperCase()}</span>
                            <span className="file-size">{formatFileSize(file.size)}</span>
                            <span className="file-date">{formatDate(file.uploadedAt)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="file-actions">
                        <Link 
                          to={`/rag/chat?fileId=${file.fileId}&filename=${encodeURIComponent(file.filename)}`}
                          className="btn primary small"
                        >
                          Start Chat
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="result error">
              <h3>❌ Upload Failed</h3>
              <p>{error}</p>
            </div>
          )}

          {uploadResult && (
            <div className="result success">
              <h3>✅ Document Uploaded Successfully</h3>
              <div className="result-details">
                <p><strong>File:</strong> {uploadResult.filename}</p>
                <p><strong>File ID:</strong> {uploadResult.fileId}</p>
                <p><strong>Message:</strong> {uploadResult.message}</p>
              </div>
              <div className="result-actions">
                <Link 
                  to={`/rag/chat?fileId=${uploadResult.fileId}&filename=${uploadResult.filename}`}
                  className="btn primary"
                >
                  Start Chatting
                </Link>
                <Link to="/rag/sessions" className="btn">
                  View All Sessions
                </Link>
              </div>
            </div>
          )}
        </div>

        <div className="help-section">
          <h3>How RAG Works</h3>
          <div className="help-content">
            <div className="help-item">
              <span className="help-icon">📊</span>
              <div>
                <h4>Document Processing</h4>
                <p>Your document is processed and indexed for semantic search</p>
              </div>
            </div>
            <div className="help-item">
              <span className="help-icon">💬</span>
              <div>
                <h4>Intelligent Chat</h4>
                <p>Ask questions about your document content in natural language</p>
              </div>
            </div>
            <div className="help-item">
              <span className="help-icon">🎯</span>
              <div>
                <h4>Contextual Answers</h4>
                <p>Get accurate answers based on your document's specific content</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
