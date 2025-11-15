// ============================================
// APP.JSX - Main Application Component
// ============================================
// This file controls the overall structure of the app including:
// - Navigation bar at the top
// - User authentication (login/logout)
// - Routing to different pages
// - Managing global state (token, username)

// Import React and hooks for managing state and side effects
import React, { useState, useEffect } from 'react'

// Import routing components to navigate between pages
import { Routes, Route, Link, useNavigate } from 'react-router-dom'

// Import all our page components
import Register from './pages/Register.jsx'
import Login from './pages/Login.jsx'
import Entries from './pages/Entries.jsx'
import Snippets from './pages/Snippets.jsx'

// ============================================
// HOME COMPONENT - Landing Page
// ============================================
// This is what users see when they first visit the app
function Home({ token }) {
  // useNavigate hook allows us to programmatically change pages
  const navigate = useNavigate()
  
  // useEffect runs code after the component displays
  // If user is already logged in (has token), redirect to entries page
  useEffect(() => {
    if (token) {
      navigate('/entries')
    }
  }, [token, navigate]) // Runs whenever token or navigate changes
  
  // Return JSX - the HTML-like code that displays on screen
  return (
    <div className="panel">
      <div className="h-title">Welcome to Dev-Log!</div>
      <p>Please login or register to start tracking your development journey.</p>
      <div style={{ marginTop: '16px', display: 'flex', gap: '8px' }}>
        {/* Link components work like <a> tags but don't refresh the page */}
        <Link to="/login"><button className="btn">Login</button></Link>
        <Link to="/register"><button className="btn btn-success">Register</button></Link>
      </div>
    </div>
  )
}

// ============================================
// APP COMPONENT - Main Application Container
// ============================================
const App = () => {
    // useState creates a variable that React watches for changes
    // When it changes, React automatically updates the page
    
    // Store authentication token - proves user is logged in
    // Try to get it from localStorage (survives page refresh), or use empty string
    const [token, setToken] = useState(localStorage.getItem('token') || '')
    
    // Store the logged-in username
    const [username, setUsername] = useState(localStorage.getItem('username') || '')
    
    // Hook to navigate between pages
    const navigate = useNavigate()

  // Save token to localStorage whenever it changes
  // This keeps user logged in even after closing the browser
  useEffect(() => {
    if (!token) return // If no token, do nothing
    localStorage.setItem('token', token)
  }, [token]) // Run this whenever token changes

  // Save username to localStorage whenever it changes
  useEffect(() => {
    if (!username) return // If no username, do nothing
    localStorage.setItem('username', username)
  }, [username]) // Run this whenever username changes

  // Function to log out the user
  const logout = () => {
    setToken('') // Clear token from state
    setUsername('') // Clear username from state
    localStorage.removeItem('token') // Remove token from localStorage
    localStorage.removeItem('username') // Remove username from localStorage
    navigate('/login') // Send user back to login page
  }

  // Function that returns headers for API requests
  // These headers tell the API who is making the request
  const apiHeaders = () => ({
    'Content-Type': 'application/json', // We're sending JSON data
    ...(token ? { Authorization: `Bearer ${token}` } : {}) // Add token if user is logged in
  })

    // Main render - this is what displays on the screen
    return (
        <div className='app-root'>
        {/* Navigation bar at the top of every page */}
        <nav className="nav">
        <div className="nav-left">DEV-LOG</div>
        <div className="nav-right">
          {/* Navigation links */}
          <Link to="/">Home</Link>
          <Link to="/entries">Entries</Link>
          <Link to="/snippets">Snippets</Link>
          
          {/* Show different options based on login status */}
          {token ? (
            // If logged in, show logout button with username
            <button className="btn-link" onClick={logout}>Logout ({username})</button>
          ) : (
            // If not logged in, show login and register links
            <>
              <Link to="/login">Login</Link>
              <Link to="/register">Register</Link>
            </>
          )}
        </div>
        </nav>
        
        {/* Main content area where different pages are displayed */}
        <main>
            {/* Routes component decides which page to show based on URL */}
            <Routes>
                {/* Home page at "/" */}
                <Route path="/" element={<Home token={token} />} />
                
                {/* Login page - pass functions to update token and username */}
               <Route path="/login" element={<Login setToken={setToken} setUsername={setUsername} />} />
               
               {/* Register page */}
               <Route path="/register" element={<Register/>} />
               
               {/* Entries page - pass API headers function and token */}
                <Route path="/entries" element={<Entries apiHeaders={apiHeaders} token={token} />} />
                
                {/* Snippets page - pass API headers function and token */}
                <Route path="/snippets" element={<Snippets apiHeaders={apiHeaders} token={token} />} />
            </Routes>
            </main>
        </div>
    )
}

// Export App so other files can import and use it
export default App
