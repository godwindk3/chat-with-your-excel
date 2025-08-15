import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { uploadRAGFile } from '../../shared/api'
import type { RAGUploadResponse } from '../../shared/types'

export const RAGUploadPage: React.FC = () => {
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<RAGUploadResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="main">
      <div className="upload-container">
        <div className="upload-section">
          <div className="upload-header">
            <div className="upload-icon">📄</div>
            <h2>Upload Document for RAG</h2>
            <p>Upload text documents (.txt, .docx, .pdf) to chat with using RAG technology</p>
          </div>

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
