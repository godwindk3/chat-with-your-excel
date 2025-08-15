import React from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'

export const RootLayout: React.FC = () => {
  return (
    <div className="container">
      <div className="header">
        <div className="brand">
          <div className="logo" />
          <div>
            <div className="title">Excel Analysis</div>
            <div className="subtitle">Upload, chat, and review sessions</div>
          </div>
        </div>
        <nav className="actions">
          <div className="nav-group">
            <span className="nav-label">Excel Analysis</span>
            <NavLink className="btn" to="/">Upload</NavLink>
            <NavLink className="btn" to="/chat">Chat</NavLink>
            <NavLink className="btn" to="/sessions">Sessions</NavLink>
            <NavLink className="btn" to="/files">Files</NavLink>
          </div>
          <div className="nav-group">
            <span className="nav-label">RAG Chat</span>
            <NavLink className="btn" to="/rag">RAG Upload</NavLink>
            <NavLink className="btn" to="/rag/chat">RAG Chat</NavLink>
            <NavLink className="btn" to="/rag/sessions">RAG Sessions</NavLink>
          </div>
        </nav>
      </div>
      <Outlet />
    </div>
  )
}


