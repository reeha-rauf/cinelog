import { useState, useEffect, useRef } from 'react'
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Avatar from './Avatar'

// Wraps every page: the nav bar stays put, <Outlet /> is where the current page goes.
function Layout() {
  const [search, setSearch] = useState('')
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef(null)
  const navigate = useNavigate()
  const location = useLocation()
  const { user, loading, logout } = useAuth()

  // Close the profile menu when clicking anywhere outside it
  useEffect(() => {
    function handleClick(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  function handleSearch(e) {
    e.preventDefault()
    navigate(search.trim() ? `/search?q=${encodeURIComponent(search.trim())}` : '/search')
    setSearch('')
  }

  async function handleLogout() {
    setMenuOpen(false)
    await logout()
    navigate('/')
  }

  return (
    <>
      <header className="navbar">
        <div className="navbar-inner">
          <Link to="/" className="brand">Cine<span>log</span></Link>
          <nav className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/search">Movies</Link>
          </nav>
          <form className="nav-search" onSubmit={handleSearch}>
            <input
              type="search"
              placeholder="Search movies..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </form>
          <div className="nav-actions">
            {/* While we're still asking the backend who you are, show nothing to avoid a flash of Log in */}
            {!loading && !user && (
              <>
                <Link to="/login" className="btn btn-outline">Log in</Link>
                <Link to="/signup" className="btn">Sign up</Link>
              </>
            )}
            {!loading && user && (
              <div className="user-menu" ref={menuRef}>
                <button
                  className="user-menu-button"
                  onClick={() => setMenuOpen(!menuOpen)}
                  aria-label="Account menu"
                >
                  <Avatar username={user.username} size={36} />
                </button>
                {menuOpen && (
                  <div className="dropdown">
                    <div className="dropdown-header">
                      <div className="muted">Signed in as</div>
                      <strong>{user.username}</strong>
                    </div>
                    <button className="dropdown-item" onClick={handleLogout}>Log out</button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </header>
      <main className="container page" key={location.pathname}>
        <Outlet />
      </main>
      <footer className="footer">Cinelog · movie tracking, powered by TMDB data</footer>
    </>
  )
}

export default Layout
