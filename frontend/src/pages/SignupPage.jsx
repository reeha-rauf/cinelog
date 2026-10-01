import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { signup } from '../api'

function SignupPage() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      await signup(username, email, password)
      navigate('/login')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-card">
      <h1>Sign Up</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="btn">Sign Up</button>
      </form>
      {error && <p className="error">{error}</p>}
      <p className="muted">Already have an account? <Link to="/login">Log in</Link></p>
    </div>
  )
}

export default SignupPage