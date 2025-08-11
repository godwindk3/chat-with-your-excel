export type UploadResponse = { fileId: string; filename: string; sheetNames: string[] }
export type CreateSessionResponse = { sessionId: string; fileId: string; sheetName: string; createdAt: string }
export type Message = { role: 'user' | 'assistant'; content: string; timestamp: string }
export type HistoryResponse = { sessionId: string; fileId: string; sheetName: string; messages: Message[] }
export type SessionSummary = { sessionId: string; fileId: string; sheetName: string; createdAt: string; messagesCount: number; lastMessageAt: string }


