// ============================================
// LOGIN.JSX - User Login Page
// ============================================
// This page allows existing users to log into the app
// When login is successful, we receive a token from the server

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

// Get API base URL from environment variables (configured in .env file)
const API_BASE = import.meta.env.VITE_API_BASE || ''

// Main login component
// Receives setToken and setUsername functions from parent (App.jsx)
export default function Login({ setToken, setUsername }){
  // State variables - these store data that can change
  // When these change, React automatically re-renders the component
  
  const [usernameOrEmail, setUsernameOrEmail] = useState('') // Store username or email input
  const [password, setPassword] = useState('') // Store password input
  const [msg, setMsg] = useState('') // Store success/error messages
  const navigate = useNavigate() // Hook to navigate to different pages

  // Function that runs when user submits the login form
  async function onSubmit(e){
    e.preventDefault() // Prevent form from refreshing the page (default behavior)
    setMsg('') // Clear any previous messages
    
    try{
      // Determine if input is email or username using regex validation
      const emailRegex = /^[\w\. ]+@[\w\. ]+\.\w+$/
      const isEmail = emailRegex.test(usernameOrEmail)
      const payload = isEmail 
        ? { email: usernameOrEmail, password }
        : { username: usernameOrEmail, password }
      
      // Make HTTP POST request to login endpoint
      const res = await fetch(`${API_BASE}/api/login`, {
        method: 'POST', // POST method to send data
        headers: {'Content-Type':'application/json'}, // Tell server we're sending JSON
        body: JSON.stringify(payload) // Convert data to JSON string
      })
      
      // Parse the response from server as JSON
      const data = await res.json()
      
      // Check if login was successful
      if(res.ok){
        // Success! Save token and username to parent component
        setToken(data.access_token) // This token proves we're logged in
        setUsername(data.username) // Save username to display in nav
        navigate('/entries') // Redirect to entries page
      } else {
        // Login failed - show error message
        setMsg(data.error || data.message || 'Login failed')
      }
    }catch(err){ 
      // If request completely fails (network error, etc)
      setMsg(String(err)) 
    }
  }

  // Return JSX - the HTML-like code that displays the login form
  return (
    <div className="panel" style={{maxWidth:560, margin:'0 auto'}}>
      <div className="h-title">Login</div>
      
      {/* Form - when submitted, calls onSubmit function */}
      <form onSubmit={onSubmit} style={{marginTop:12}}>
        
        {/* Username or Email input field */}
        <div className="form-row">
          <label>Username or Email</label>
          {/* value={usernameOrEmail} shows current state */}
          {/* onChange updates state when user types */}
          <input 
            className="input" 
            value={usernameOrEmail} 
            onChange={e=>setUsernameOrEmail(e.target.value)} 
            placeholder="Enter username or email"
          />
        </div>
        
        {/* Password input field */}
        <div className="form-row">
          <label>Password</label>
          {/* type="password" hides the password text */}
          <input 
            className="input" 
            type="password" 
            value={password} 
            onChange={e=>setPassword(e.target.value)} 
            placeholder='Enter Password'
          />
        </div>
        
        {/* Submit button and message display */}
        <div style={{display:'flex',gap:8,alignItems:'center'}}>
          <button className="btn" type="submit">Login</button>
          {/* Display success/error message if exists */}
          <div className="small muted">{msg}</div>
        </div>
      </form>
    </div>
  )
}
