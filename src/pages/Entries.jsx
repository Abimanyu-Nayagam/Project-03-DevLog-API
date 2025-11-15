// ============================================
// ENTRIES.JSX - Dev Log Entries Page
// ============================================
// This page allows users to:
// - Create new dev log entries
// - View all their entries (collapsed list)
// - Edit existing entries
// - Delete entries
// - Search and filter entries
// - Export entries as Markdown or JSON

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

// Get API base URL from environment variables
const API_BASE = import.meta.env.VITE_API_BASE || ''

// Main Entries component
// Receives apiHeaders (function) and token from parent (App.jsx)
export default function Entries({ apiHeaders, token }) {
  const navigate = useNavigate() // Hook to navigate between pages
  
  // ============================================
  // STATE VARIABLES - Store component data
  // ============================================
  
  // List of all entries fetched from server
  const [entriesList, setEntriesList] = useState([])
  
  // Loading state - shows spinner while fetching data
  const [loading, setLoading] = useState(false)
  
  // Success/error messages to display to user
  const [message, setMessage] = useState('')
  
  // Form fields for creating/editing entries
  const [title, setTitle] = useState('') // Entry title
  const [content, setContent] = useState('') // Entry content/body
  const [tags, setTags] = useState('') // Comma-separated tags
  
  // Edit mode - stores ID of entry being edited (null = creating new)
  const [editId, setEditId] = useState(null)
  
  // Search and filter functionality
  const [searchTerm, setSearchTerm] = useState('') // Search input value
  const [filterType, setFilterType] = useState('all') // all, tag, or title
  
  // Expanded entry ID - which entry is currently expanded (null = all collapsed)
  const [expandedId, setExpandedId] = useState(null)
  
  // Auto-generation loading states
  const [generatingTitle, setGeneratingTitle] = useState(false)
  const [generatingTags, setGeneratingTags] = useState(false)

  // ============================================
  // AUTO-GENERATE FUNCTIONS - AI-powered field generation
  // ============================================
  
  // Auto-generate title based on content
  async function autoGenerateTitle() {
    if (!content) {
      setMessage('Please enter content first before generating title')
      return
    }
    
    setGeneratingTitle(true)
    setMessage('')
    
    try {
      // Call backend autogen endpoint (to be implemented by other developer)
      const res = await fetch(`${API_BASE}/autogen/title`, {
        method: 'POST',
        headers: apiHeaders(),
        body: JSON.stringify({ content })
      })
      const data = await res.json()
      
      if (res.ok) {
        setTitle(data.title || data.generated_title || '') // Update title field
        setMessage('Title generated successfully!')
      } else {
        setMessage(data.error || 'Failed to generate title')
      }
    } catch (err) {
      setMessage('Error generating title: ' + err)
    }
    
    setGeneratingTitle(false)
  }
  
  // Auto-generate tags based on content
  async function autoGenerateTags() {
    if (!content) {
      setMessage('Please enter content first before generating tags')
      return
    }
    
    setGeneratingTags(true)
    setMessage('')
    
    try {
      // Call backend autogen endpoint (to be implemented by other developer)
      const res = await fetch(`${API_BASE}/autogen/tags`, {
        method: 'POST',
        headers: apiHeaders(),
        body: JSON.stringify({ content })
      })
      const data = await res.json()
      
      if (res.ok) {
        setTags(data.tags || data.generated_tags || '') // Update tags field
        setMessage('Tags generated successfully!')
      } else {
        setMessage(data.error || 'Failed to generate tags')
      }
    } catch (err) {
      setMessage('Error generating tags: ' + err)
    }
    
    setGeneratingTags(false)
  }

  // ============================================
  // FETCH ENTRIES - Load data when page loads
  // ============================================
  // useEffect runs after component displays
  // This runs once when component mounts (loads) if token exists
  useEffect(() => {
    if (token && apiHeaders) {
      fetchEntries() // Call function to get entries from server
    }
  }, [token]) // Dependency array - run when token changes

  // Function to fetch all entries from the API
  async function fetchEntries() {
    if (!apiHeaders) return // Safety check - don't run if no auth headers
    
    setLoading(true) // Show loading spinner
    setMessage('') // Clear any previous messages
    
    try {
      // Make GET request to fetch entries
      const res = await fetch(`${API_BASE}/api/v1/entries`, {
        headers: apiHeaders() // Include authentication token in headers
      })
      
      // Parse response as JSON
      const data = await res.json()
      
      // Check if request was successful
      if (res.ok) {
        // API might return array directly or wrapped in object
        const entriesArray = Array.isArray(data) ? data : (data.entries || [])
        setEntriesList(entriesArray) // Update state with fetched entries
      } else {
        // Request failed - show error message
        setMessage(data.error || 'Failed to fetch entries')
      }
    } catch (err) {
      // Network error or other exception
      setMessage('Error: ' + err)
    }
    setLoading(false) // Hide loading spinner
  }

  // ============================================
  // CREATE ENTRY - Add new entry to database
  // ============================================
  async function createEntry(e) {
    e.preventDefault() // Prevent form from refreshing page
    setMessage('') // Clear previous messages
    
    // Validate required fields
    if (!title || !content) {
      setMessage('Title and content are required')
      return // Exit function if validation fails
    }

    try {
      // Send POST request to create new entry
      const res = await fetch(`${API_BASE}/api/v1/entries`, {
        method: 'POST', // POST = create new resource
        headers: apiHeaders(), // Include authentication token
        body: JSON.stringify({ title, content, tags }) // Convert data to JSON string
      })
      const data = await res.json() // Parse response
      
      if (res.ok) {
        // Success! Show message and clear form
        setMessage('Entry created successfully!')
        setTitle('') // Clear title input
        setContent('') // Clear content textarea
        setTags('') // Clear tags input
        fetchEntries() // Refresh list to show new entry
      } else {
        // Failed - show error from server
        setMessage(data.error || 'Failed to create entry')
      }
    } catch (err) {
      // Network error or exception
      setMessage('Error: ' + err)
    }
  }

  // ============================================
  // UPDATE ENTRY - Edit existing entry
  // ============================================
  async function updateEntry(e) {
    e.preventDefault() // Prevent form refresh
    setMessage('') // Clear messages
    
    // Validate required fields
    if (!title || !content) {
      setMessage('Title and content are required')
      return
    }

    try {
      // Send PATCH request to update entry
      const res = await fetch(`${API_BASE}/api/v1/entries`, {
        method: 'PATCH', // PATCH = update existing resource
        headers: apiHeaders(), // Auth token
        body: JSON.stringify({ id: editId, title, content, tags }) // Include entry ID
      })
      const data = await res.json()
      
      if (res.ok) {
        // Success! Clear form and exit edit mode
        setMessage('Entry updated successfully!')
        setTitle('') // Clear inputs
        setContent('')
        setTags('')
        setEditId(null) // Exit edit mode (back to create mode)
        fetchEntries() // Refresh list with updated entry
      } else {
        setMessage(data.error || 'Failed to update entry')
      }
    } catch (err) {
      setMessage('Error: ' + err)
    }
  }

  // ============================================
  // DELETE ENTRY - Remove entry from database
  // ============================================
  async function deleteEntry(id) {
    // Ask user to confirm deletion (prevents accidental deletes)
    if (!confirm('Are you sure you want to delete this entry?')) return
    
    setMessage('') // Clear messages
    try {
      // Send DELETE request with entry ID in URL
      const res = await fetch(`${API_BASE}/api/v1/entries/${id}`, {
        method: 'DELETE', // DELETE = remove resource
        headers: apiHeaders() // Auth token
      })
      const data = await res.json()
      
      if (res.ok) {
        // Success! Show message and refresh list
        setMessage('Entry deleted successfully!')
        fetchEntries() // Refresh to show entry is gone
      } else {
        setMessage(data.error || 'Failed to delete entry')
      }
    } catch (err) {
      setMessage('Error: ' + err)
    }
  }

  // ============================================
  // EDIT MODE FUNCTIONS
  // ============================================
  
  // Start editing an entry - populate form with entry data
  function startEdit(entry) {
    setEditId(entry.id) // Set edit mode with this entry's ID
    setTitle(entry.title) // Fill in form fields with entry data
    setContent(entry.content)
    setTags(entry.tags || '') // Use existing tags or empty string
    window.scrollTo({ top: 0, behavior: 'smooth' }) // Scroll to top to show form
  }

  // Cancel editing - clear form and exit edit mode
  function cancelEdit() {
    setEditId(null) // Exit edit mode (back to create mode)
    setTitle('') // Clear all form fields
    setContent('')
    setTags('')
  }

  // ============================================
  // SEARCH ENTRIES - Find entries by keyword
  // ============================================
  async function searchEntries() {
    // If search box is empty, just show all entries
    if (!searchTerm) {
      fetchEntries() // Reload all entries
      return
    }
    
    setLoading(true) // Show spinner
    setMessage('') // Clear messages
    try {
      // Send GET request with search query in URL
      const res = await fetch(`${API_BASE}/api/v1/entries/search?q=${searchTerm}`, {
        headers: apiHeaders() // Auth token
      })
      const data = await res.json()
      
      if (res.ok) {
        // Success! Display matching entries
        const entriesArray = Array.isArray(data) ? data : (data.entries || [])
        setEntriesList(entriesArray)
      } else {
        setMessage(data.error || 'Search failed')
      }
    } catch (err) {
      setMessage('Error: ' + err)
    }
    setLoading(false) // Hide spinner
  }

  // ============================================
  // FILTER ENTRIES - Filter by tag or title
  // ============================================
  async function filterEntries() {
    // Validate: user must enter something to filter by
    if (!searchTerm) {
      setMessage('Please enter a filter value')
      return
    }
    
    setLoading(true) // Show spinner
    setMessage('') // Clear messages
    
    try {
      let url = '' // Build URL based on filter type
      if (filterType === 'tag') {
        // Filter by tag: /api/v1/entries/filter/tag/{tagname}
        url = `${API_BASE}/api/v1/entries/filter/tag/${searchTerm}`
      } else if (filterType === 'title') {
        // Filter by title: /api/v1/entries/filter/title/{titletext}
        url = `${API_BASE}/api/v1/entries/filter/title/${searchTerm}`
      } else {
        // If 'all' selected, just do regular search
        searchEntries()
        return
      }
      
      // Send GET request to filter endpoint
      const res = await fetch(url, { headers: apiHeaders() })
      const data = await res.json()
      
      if (res.ok) {
        // Success! Display filtered entries
        const entriesArray = Array.isArray(data) ? data : (data.entries || [])
        setEntriesList(entriesArray)
      } else {
        setMessage(data.error || 'Filter failed')
      }
    } catch (err) {
      setMessage('Error: ' + err)
    }
    setLoading(false) // Hide spinner
  }

  // ============================================
  // EXPORT FUNCTIONS - Download entry as file
  // ============================================
  
  // Export entry as Markdown file
  async function exportMarkdown(id) {
    // Fetch file with auth headers, then download as blob
    try {
      const res = await fetch(`${API_BASE}/export-entry-md/v1/${id}`, {
        headers: apiHeaders() // Include auth token
      })
      if (res.ok) {
        const blob = await res.blob() // Get file data
        const url = window.URL.createObjectURL(blob) // Create download URL
        const a = document.createElement('a') // Create download link
        a.href = url
        a.download = `Entry-${id}.md` // Set filename
        a.click() // Trigger download
        window.URL.revokeObjectURL(url) // Clean up
      } else {
        setMessage('Export failed')
      }
    } catch (err) {
      setMessage('Export error: ' + err)
    }
  }

  // Export entry as JSON file
  async function exportJSON(id) {
    // Fetch file with auth headers, then download as blob
    try {
      const res = await fetch(`${API_BASE}/export-entry-json/v1/${id}`, {
        headers: apiHeaders() // Include auth token
      })
      if (res.ok) {
        const blob = await res.blob() // Get file data
        const url = window.URL.createObjectURL(blob) // Create download URL
        const a = document.createElement('a') // Create download link
        a.href = url
        a.download = `Entry-${id}.json` // Set filename
        a.click() // Trigger download
        window.URL.revokeObjectURL(url) // Clean up
      } else {
        setMessage('Export failed')
      }
    } catch (err) {
      setMessage('Export error: ' + err)
    }
  }

  // ============================================
  // RENDER - Authentication Check
  // ============================================
  
  // If user is not logged in, show message and login button
  if (!token) {
    return (
      <div className="panel">
        <div className="h-title">Authentication Required</div>
        <p>Please login to view and manage your entries.</p>
        <button className="btn" onClick={() => navigate('/login')}>Go to Login</button>
      </div>
    )
  }

  // ============================================
  // RENDER - Loading State
  // ============================================
  
  // If data is loading and no entries shown yet, display loading message
  if (loading && entriesList.length === 0) {
    return (
      <div className="panel">
        <div className="loading">Loading your entries...</div>
      </div>
    )
  }

  // ============================================
  // RENDER - Main Page Content (JSX)
  // ============================================
  // JSX = JavaScript XML - looks like HTML but is JavaScript
  
  return (
    <div>
      {/* Form Panel - Create or Edit Entry */}
      <div className="panel">
        {/* Title changes based on whether we're creating or editing */}
        <div className="h-title">{editId ? 'Edit Entry' : 'Create New Entry'}</div>
        
        {/* 
          Form submission:
          - If editId exists, call updateEntry function
          - If editId is null, call createEntry function
        */}
        <form onSubmit={editId ? updateEntry : createEntry}>
          {/* Content Textarea - Place first so user enters content before generating other fields */}
          <div className="form-row">
            <label>Content</label>
            <textarea 
              className="input" 
              value={content} // Controlled input
              onChange={e => setContent(e.target.value)} // Update state
              placeholder="Write your dev log entry here..."
              rows="6" // Taller textarea for content
            />
            <div className="small muted" style={{ marginTop: '4px' }}>
              💡 Tip: Enter your content first, then use Auto-Generate buttons for title and tags
            </div>
          </div>
          
          {/* Title Input with Auto-Generate Button */}
          <div className="form-row">
            <label>Title</label>
            <div className="input-with-button">
              <input 
                className="input" 
                value={title} // Controlled input - value from state
                onChange={e => setTitle(e.target.value)} // Update state on change
                placeholder="Enter entry title or auto-generate"
              />
              <button 
                className="btn btn-small btn-success" 
                type="button" 
                onClick={autoGenerateTitle}
                disabled={generatingTitle || !content}
                style={{ marginLeft: '8px' }}
              >
                {generatingTitle ? '⏳ Generating...' : '✨ Auto-Generate'}
              </button>
            </div>
          </div>
          
          {/* Tags Input with Auto-Generate Button */}
          <div className="form-row">
            <label>Tags (comma separated)</label>
            <div className="input-with-button">
              <input 
                className="input" 
                value={tags} // Controlled input
                onChange={e => setTags(e.target.value)} // Update state
                placeholder="react, javascript, bug-fix or auto-generate"
              />
              <button 
                className="btn btn-small btn-success" 
                type="button" 
                onClick={autoGenerateTags}
                disabled={generatingTags || !content}
                style={{ marginLeft: '8px' }}
              >
                {generatingTags ? '⏳ Generating...' : '✨ Auto-Generate'}
              </button>
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex flex-gap">
            {/* Submit button - text changes based on mode */}
            <button className="btn" type="submit">
              {editId ? 'Update Entry' : 'Create Entry'}
            </button>
            
            {/* Cancel button - only show in edit mode */}
            {editId && (
              <button className="btn btn-danger" type="button" onClick={cancelEdit}>
                Cancel Edit
              </button>
            )}
            
            {/* Success/error message display */}
            {message && <div className="small muted">{message}</div>}
          </div>
        </form>
      </div>

      {/* Search & Filter Panel */}
      <div className="panel">
        <div className="h-title">Search & Filter Entries</div>
        
        {/* Filter Type Dropdown */}
        <div className="form-row">
          <label>Filter Type</label>
          <select 
            className="input" 
            value={filterType} // Current filter type
            onChange={e => setFilterType(e.target.value)} // Update filter type
          >
            {/* Dropdown options */}
            <option value="all">Search All</option>
            <option value="tag">Filter by Tag</option>
            <option value="title">Filter by Title</option>
          </select>
        </div>
        
        {/* Search Bar */}
        <div className="search-bar">
          {/* Search/Filter Input */}
          <input 
            className="input" 
            value={searchTerm} // Search text
            onChange={e => setSearchTerm(e.target.value)} // Update search text
            placeholder={
              // Placeholder text changes based on filter type
              filterType === 'tag' ? 'Enter tag (e.g. react)' :
              filterType === 'title' ? 'Enter title keyword' :
              'Search by title or content...'
            }
            // Allow pressing Enter key to search/filter
            onKeyPress={e => e.key === 'Enter' && (filterType === 'all' ? searchEntries() : filterEntries())}
          />
          
          {/* Search/Filter Button */}
          <button className="btn" onClick={filterType === 'all' ? searchEntries : filterEntries}>
            {filterType === 'all' ? 'Search' : 'Filter'}
          </button>
          
          {/* Clear Button - reset search and show all entries */}
          <button className="btn btn-danger" onClick={() => { setSearchTerm(''); fetchEntries(); }}>
            Clear
          </button>
        </div>
      </div>

      {/* Entries List Panel */}
      <div className="panel">
        <div className="h-title">My Dev Log Entries ({entriesList.length})</div>
        
        {/* Show loading spinner if data is loading */}
        {loading && <div className="loading">Loading entries...</div>}
        
        {/* Show message if no entries found */}
        {!loading && entriesList.length === 0 && (
          <div className="muted">No entries found. Create your first one!</div>
        )}
        
        {/* 
          Map through entries and display each one
          .map() creates a list item for each entry in the array
        */}
        {!loading && entriesList.map(entry => {
          // Check if this entry is currently expanded
          const isExpanded = expandedId === entry.id
          
          return (
            <div key={entry.id} className="item">
              {/* 
                Entry Header - Clickable to expand/collapse
                Shows title and created date
              */}
              <div 
                className="item-header" 
                style={{ cursor: 'pointer' }} // Show pointer cursor on hover
                onClick={() => setExpandedId(isExpanded ? null : entry.id)} // Toggle expand
              >
                <div className="item-title">
                  {/* Arrow icon changes based on expanded state */}
                  {isExpanded ? '▼' : '▶'} {entry.title}
                </div>
                <div className="muted small">
                  {/* Format date in readable format */}
                  {new Date(entry.created_at).toLocaleDateString()}
                </div>
              </div>
              
              {/* 
                Entry Details - Only show when expanded
                && means "if isExpanded is true, show this"
              */}
              {isExpanded && (
                <>
                  {/* Entry content/body */}
                  <div className="item-content">{entry.content}</div>
                  
                  {/* Tags section */}
                  <div className="item-meta">
                    {entry.tags && (
                      <div>
                        {/* Split tags by comma and display each as a badge */}
                        {entry.tags.split(',').map((tag, i) => (
                          <span key={i} className="tag">{tag.trim()}</span>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  {/* Action buttons for entry */}
                  <div className="item-actions" style={{ marginTop: '12px' }}>
                    {/* 
                      Edit button - calls startEdit function
                      e.stopPropagation() prevents click from collapsing entry
                    */}
                    <button className="btn btn-small" onClick={(e) => { e.stopPropagation(); startEdit(entry); }}>
                      Edit
                    </button>
                    
                    {/* Export Markdown button */}
                    <button className="btn btn-small btn-success" onClick={(e) => { e.stopPropagation(); exportMarkdown(entry.id); }}>
                      Export MD
                    </button>
                    
                    {/* Export JSON button */}
                    <button className="btn btn-small btn-success" onClick={(e) => { e.stopPropagation(); exportJSON(entry.id); }}>
                      Export JSON
                    </button>
                    
                    {/* Delete button - removes entry from database */}
                    <button className="btn btn-small btn-danger" onClick={(e) => { e.stopPropagation(); deleteEntry(entry.id); }}>
                      Delete
                    </button>
                  </div>
                </>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
