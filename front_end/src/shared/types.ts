export type UploadResponse = { fileId: string; filename: string; sheetNames: string[] }
export type CreateSessionResponse = { sessionId: string; fileId: string; sheetName: string; createdAt: string }
export type Message = { role: 'user' | 'assistant'; content: string; timestamp: string }
export type HistoryResponse = { sessionId: string; fileId: string; sheetName: string; messages: Message[] }
export type SessionSummary = { sessionId: string; fileId: string; sheetName: string; createdAt: string; messagesCount: number; lastMessageAt: string; sessionType?: string }
export type FileInfo = { fileId: string; filename: string; size: number; uploadedAt: number }

// RAG Types
export type RAGUploadResponse = { fileId: string; filename: string; message: string }
export type RAGSessionRequest = { fileId: string; sessionName: string }
export type RAGSessionResponse = { sessionId: string; sessionName: string; fileId: string; filename: string; createdAt: string }
export type RAGQueryRequest = { fileId: string; question: string }
export type RAGQueryResponse = { answer: string }
export type RAGAskRequest = { question: string }
export type RAGFileInfo = { fileId: string; filename: string; fullFilename: string; size: number; uploadedAt: number; fileType: string }


