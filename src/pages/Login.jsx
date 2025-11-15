import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE || ''

export default function Login({ setToken, setUsername }){
  const [username, setUser] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  const navigate = useNavigate()

  async function onSubmit(e){
    setMsg('')
    try{
      const res = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, password})
      })
      const data = await res.json()
      if(res.ok){
        setToken(data.access_token)
        setUsername(data.username)
        navigate('/entries')
      } else {
        setMsg(data.error || data.message || 'Login failed')
      }
    }catch(err){ setMsg(String(err)) }
  }

  return (
    <div className="panel" style={{maxWidth:560}}>
      <div className="h-title">Login</div>
      <form onSubmit={onSubmit} style={{marginTop:12}}>
        <div className="form-row">
          <label>Username</label>
          <input className="input" value={username} onChange={e=>setUser(e.target.value)} />
        </div>
        <div className="form-row">
          <label>Password</label>
          <input className="input" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        </div>
        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <button className="btn" type="submit">Login</button>
          <div className="small muted">{msg}</div>
        </div>
      </form>
    </div>
  )
}
