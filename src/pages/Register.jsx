// ============================================
// REGISTER.JSX - New User Registration Page
// ============================================
// This page allows new users to create an account
// After successful registration, user is redirected to login page

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

// Get API base URL from environment variables
const API_BASE = import.meta.env.VITE_API_BASE || ''

// Main register component
export default function Register(){
  // State variables to store form inputs
  const [email, setEmail] = useState('') // User's email
  const [username, setUser] = useState('') // Chosen username
  const [password, setPassword] = useState('') // Chosen password
  const [msg, setMsg] = useState('') // Success/error messages
  const navigate = useNavigate() // Hook to navigate between pages

  // Function that runs when user submits the registration form
  async function onSubmit(e){
    e.preventDefault() // Prevent page refresh
    setMsg('') // Clear any previous messages
    
    try{
      // Send POST request to register endpoint
      const res = await fetch(`${API_BASE}/register`, {
        method:'POST', // POST method sends data to server
        headers: {'Content-Type':'application/json'}, // Tell server we're sending JSON
        body: JSON.stringify({email, username, password}) // Convert form data to JSON
      })
      
      // Parse server response
      const data = await res.json()
      
      // Check if registration was successful
      if(res.ok){
        setMsg('Registered — you can login') // Show success message
        navigate('/login') // Redirect to login page
      } else {
        // Registration failed - show error message
        setMsg(data.error || data.message || 'Register failed')
      }
    }catch(err){ 
      // If request fails completely
      setMsg(String(err)) 
    }
  }

  // Return JSX - the HTML-like code that displays the registration form
  return (
    <div className="panel" style={{maxWidth:560, margin:'0 auto'}}>
      <div className="h-title">Register</div>
      
      {/* Registration form */}
      <form onSubmit={onSubmit} style={{marginTop:12}}>
        
        {/* Email input field */}
        <div className="form-row">
          <label>Email</label>
          <input 
            className="input" 
            value={email} 
            onChange={e=>setEmail(e.target.value)} 
          />
        </div>
        
        {/* Username input field */}
        <div className="form-row">
          <label>Username</label>
          <input 
            className="input" 
            value={username} 
            onChange={e=>setUser(e.target.value)} 
          />
        </div>
        
        {/* Password input field */}
        <div className="form-row">
          <label>Password</label>
          <input 
            className="input" 
            type="password" 
            value={password} 
            onChange={e=>setPassword(e.target.value)} 
          />
        </div>
        
        {/* Submit button and message display */}
        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <button className="btn">Register</button>
          <div className="small muted">{msg}</div>
        </div>
      </form>
    </div>
  )
}
