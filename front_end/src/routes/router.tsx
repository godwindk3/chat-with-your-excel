import React from 'react'
import { createBrowserRouter } from 'react-router-dom'
import { RootLayout } from '../ui/layouts/RootLayout'
import { UploadPage } from '../ui/pages/UploadPage'
import { ChatPage } from '../ui/pages/ChatPage'
import { SessionsPage } from '../ui/pages/SessionsPage'
import { FilesPage } from '../ui/pages/FilesPage'
import { RAGUploadPage } from '../ui/pages/RAGUploadPage'
import { RAGChatPage } from '../ui/pages/RAGChatPage'
import { RAGSessionsPage } from '../ui/pages/RAGSessionsPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      { index: true, element: <UploadPage /> },
      { path: 'chat', element: <ChatPage /> },
      { path: 'sessions', element: <SessionsPage /> },
      { path: 'files', element: <FilesPage /> },
      // RAG Routes
      { path: 'rag', element: <RAGUploadPage /> },
      { path: 'rag/chat', element: <RAGChatPage /> },
      { path: 'rag/sessions', element: <RAGSessionsPage /> },
    ],
  },
])


