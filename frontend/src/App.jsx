import { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState('loading...')

  useEffect(() => {
    fetch('http://localhost:8000/')
      .then(res => res.json())
      .then(data => setStatus(data.status))
      .catch(() => setStatus('failed to connect'))
  }, [])

  return (
    <div>
      <h1>Cinelog</h1>
      <p>Backend status: {status}</p>
    </div>
  )
}

export default App