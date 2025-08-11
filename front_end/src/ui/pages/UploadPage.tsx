import React, { useState } from 'react'
import { uploadFile } from '../../shared/api'

export const UploadPage: React.FC = () => {
  const [fileId, setFileId] = useState<string | null>(null)
  const [sheetNames, setSheetNames] = useState<string[]>([])
  const [error, setError] = useState<string>('')

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return
    setError('')
    try {
      const res = await uploadFile(e.target.files[0])
      setFileId(res.fileId)
      setSheetNames(res.sheetNames)
    } catch (err: any) {
      setError(err?.message || 'Upload failed')
    }
  }

  return (
    <div className="grid">
      <div className="card">
        <div className="sectionTitle">Upload</div>
        <label className="label">Upload Excel (.xlsx/.xls)</label>
        <input className="fileInput" type="file" accept=".xlsx,.xls" onChange={handleUpload} />
        {fileId && (
          <div className="fileInfo" style={{ marginTop: 8 }}>
            Uploaded. FileId: {fileId}
            <div className="footerNote">Sheets: {sheetNames.join(', ')}</div>
          </div>
        )}
      </div>
      {error && <div className="card alert alertError">{error}</div>}
    </div>
  )
}


