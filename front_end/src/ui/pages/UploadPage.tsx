import React, { useState } from 'react'
import { uploadFile, getFileInfo } from '../../shared/api'
import { FilePicker } from '../../shared/components/FilePicker'
import type { FileInfo } from '../../shared/types'

export const UploadPage: React.FC = () => {
  const [uploadMode, setUploadMode] = useState<'upload' | 'select'>('upload')
  const [fileId, setFileId] = useState<string | null>(null)
  const [filename, setFilename] = useState<string>('')
  const [sheetNames, setSheetNames] = useState<string[]>([])
  const [error, setError] = useState<string>('')

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    setError('')
    try {
      const res = await uploadFile(e.target.files[0])
      setFileId(res.fileId)
      setFilename(res.filename)
      setSheetNames(res.sheetNames)
    } catch (err: any) {
      setError(err?.message || 'Upload failed')
    }
  }

  const handleFileSelect = async (file: FileInfo) => {
    setError('')
    try {
      const res = await getFileInfo(file.fileId)
      setFileId(res.fileId)
      setFilename(res.filename)
      setSheetNames(res.sheetNames)
    } catch (err: any) {
      setError(err?.message || 'Failed to load file info')
    }
  }

  const handleReset = () => {
    setFileId(null)
    setFilename('')
    setSheetNames([])
    setError('')
  }

  return (
    <div className="grid">
      <div className="card">
        <div className="sectionTitle">Select File</div>
        
        <div className="uploadTabs">
          <button 
            className={`uploadTab ${uploadMode === 'upload' ? 'active' : ''}`}
            onClick={() => setUploadMode('upload')}
          >
            Upload New
          </button>
          <button 
            className={`uploadTab ${uploadMode === 'select' ? 'active' : ''}`}
            onClick={() => setUploadMode('select')}
          >
            From Storage
          </button>
        </div>

        {uploadMode === 'upload' ? (
          <div className="uploadOption">
            <label className="label">Upload Excel (.xlsx/.xls)</label>
            <input className="fileInput" type="file" accept=".xlsx,.xls" onChange={handleUpload} />
          </div>
        ) : (
          <div className="uploadOption">
            <label className="label">Select from storage</label>
            <FilePicker 
              selectedFileId={fileId}
              onFileSelect={handleFileSelect}
              onError={setError}
            />
          </div>
        )}

        {fileId && (
          <div className="fileInfo" style={{ marginTop: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div>Selected: {filename}</div>
                <div className="footerNote">FileId: {fileId}</div>
                <div className="footerNote">Sheets: {sheetNames.join(', ')}</div>
              </div>
              <button className="btn" onClick={handleReset} style={{ fontSize: '12px', padding: '6px 10px' }}>
                Clear
              </button>
            </div>
          </div>
        )}
      </div>
      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}


