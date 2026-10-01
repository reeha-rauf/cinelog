import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getFeed } from '../api'
import { useAuth } from '../context/AuthContext'
import Avatar from '../components/Avatar'
import StarRating from '../components/StarRating'

const POSTER_BASE = 'https://image.tmdb.org/t/p/w185'

function HomePage() {
  const { user, loading: authLoading } = useAuth()
  const [feed, setFeed] = useState([])
  const [feedLoading, setFeedLoading] = useState(false)
  const [error, setError] = useState('')

  // Load the feed whenever the logged-in user changes (login, logout)
  useEffect(() => {
    if (!user) {
      setFeed([])
      return
    }
    setFeedLoading(true)
    setError('')
    getFeed()
      .then(setFeed)
      .catch((err) => setError(err.message))
      .finally(() => setFeedLoading(false))
  }, [user])

  if (authLoading || feedLoading) {
    return (
      <div className="feed">
        <div className="skeleton skeleton-card" />
        <div className="skeleton skeleton-card" />
      </div>
    )
  }

  if (!user) {
    return (
      <section className="hero">
        <h1>Track every film you watch.</h1>
        <p>Log what you've seen, rate and review it, and follow friends to see what they're watching.</p>
        <Link to="/signup" className="btn">Get started</Link>
        <Link to="/login" className="btn btn-outline">Log in</Link>
      </section>
    )
  }

  return (
    <div>
      <h1>Your Feed</h1>
      {error && <p className="error">{error}</p>}
      {feed.length === 0 && !error && (
        <div className="empty">Nothing here yet. Follow some people to see what they're watching.</div>
      )}
      <div className="feed">
        {feed.map((entry) => (
          <article key={entry.log_id} className="feed-card">
            {entry.poster_url ? (
              <img className="poster" src={POSTER_BASE + entry.poster_url} alt={entry.movie_title} />
            ) : (
              <div className="poster-placeholder" />
            )}
            <div>
              <div className="feed-head">
                <Avatar username={entry.username} size={28} />
                <span><strong>{entry.username}</strong> watched <strong>{entry.movie_title}</strong></span>
              </div>
              {entry.rating != null && <StarRating value={entry.rating} />}
              {entry.review && <p className="feed-review">{entry.review}</p>}
              <small className="muted">{new Date(entry.created_at).toLocaleDateString()}</small>
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}

export default HomePage
