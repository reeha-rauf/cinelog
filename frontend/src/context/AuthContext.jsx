import { createContext, useContext, useState, useEffect } from 'react'
import { getCurrentUser, logout as apiLogout } from '../api'

const AuthContext = createContext(null)

// Wrap the app in this once. Any component inside can call useAuth() to get the login state.
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Ask the backend "who am I?" once, when the app first loads
  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  // Call after a successful login so the whole app updates
  async function refreshUser() {
    setUser(await getCurrentUser())
  }

  async function logout() {
    await apiLogout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, refreshUser, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
