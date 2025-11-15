import React, { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Register from './pages/Register.jsx'
import Login from './pages/Login.jsx'

const App = () => {
    const [token, setToken] = useState(localStorage.getItem('token') || '')
    const [username, setUsername] = useState(localStorage.getItem('username') || '')
    const navigate = useNavigate()

  useEffect(() => {
    if (!token) return
    localStorage.setItem('token', token)
  }, [token])

  useEffect(() => {
    if (!username) return
    localStorage.setItem('username', username)
  }, [username])

  const logout = () => {
    setToken('')
    setUsername('')
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  const apiHeaders = () => ({
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  })

    return (
        <div className='app-root'>
        <nav className="nav">
        <div className="nav-left">DEV-LOG</div>
        <div className="nav-right">
          <Link to="/">Home</Link>
          <Link to="/entries">Entries</Link>
          <Link to="/snippets">Snippets</Link>
          {token ? (
            <button className="btn-link" onClick={logout}>Logout ({username})</button>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
        </nav>
        <main>
            <Routes>
                <Route path="/" element={<div>Welcome to Dev-Log! Please login or register.</div>} />
               <Route path="/login" element={<Login setToken={setToken} setUsername={setUsername} />} />
               <Route path="/register" element={<Register/>} />
            </Routes>
            </main>
        </div>
    )
}

export default App
