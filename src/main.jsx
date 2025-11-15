// ============================================
// MAIN.JSX - Entry Point of the Application
// ============================================
// This is the first file that runs when the app starts.
// It sets up React and connects it to the HTML page.

// Import React library - needed to use React features
import React from 'react'

// Import createRoot - this tells React where to display our app in the HTML
import { createRoot } from 'react-dom/client'

// Import BrowserRouter - handles navigation between different pages
// Without this, clicking links would refresh the whole page
import { BrowserRouter } from 'react-router-dom'

// Import our main App component - contains all the pages and logic
import App from './App'

// Import our CSS styles to make everything look good
import './style.css'

// This finds the HTML element with id="root" and renders our React app inside it
// BrowserRouter wraps everything to enable page navigation without refreshing
createRoot(document.getElementById('root')).render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
)
