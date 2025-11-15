import React, { useEffect } from 'react'

export default function Toast({msg, onClose, duration = 3500}){
  useEffect(() => {
    const t = setTimeout(() => onClose && onClose(), duration)
    return () => clearTimeout(t)
  }, [duration, onClose])

  if(!msg) return null

  return (
    <div className="toast">{msg}</div>
  )
}
