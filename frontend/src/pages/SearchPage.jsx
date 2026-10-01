import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import MovieCard from '../components/MovieCard'
import { searchMovies } from '../api'

function SearchPage() {
  // The submitted search lives in the URL (/search?q=inception), so results are linkable and survive refresh
  const [params, setParams] = useSearchParams()
  const query = params.get('q') || ''

  // What's typed in the box, kept separate so we only search on submit
  const [input, setInput] = useState(query)
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Re-runs whenever the URL's query changes (new search, back button, nav bar search)
  useEffect(() => {
    setInput(query)
    if (!query) {
      setResults([])
      return
    }
    let cancelled = false
    setLoading(true)
    setError('')
    searchMovies(query)
      .then((data) => { if (!cancelled) setResults(data) })
      .catch((err) => { if (!cancelled) setError(err.message) })
      .finally(() => { if (!cancelled) setLoading(false) })
    // If the query changes mid-request, ignore the stale response
    return () => { cancelled = true }
  }, [query])

  function handleSubmit(e) {
    e.preventDefault()
    const q = input.trim()
    setParams(q ? { q } : {})
  }

  return (
    <div>
      <h1>Search</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          className="search-input"
          type="search"
          placeholder="Search for a movie..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          autoFocus
        />
        <button type="submit" className="btn">Search</button>
      </form>

      {error && <p className="error">{error}</p>}

      {loading && (
        <div className="movie-grid search-results">
          {[...Array(8)].map((_, i) => <div key={i} className="skeleton skeleton-poster" />)}
        </div>
      )}

      {!loading && !error && !query && (
        <div className="empty search-results">Type a title above to find a movie.</div>
      )}

      {!loading && !error && query && results.length === 0 && (
        <div className="empty search-results">No movies found for "{query}".</div>
      )}

      {!loading && results.length > 0 && (
        <>
          <h2 className="section-title">{results.length} results for "{query}"</h2>
          <div className="movie-grid">
            {results.map((m) => (
              <MovieCard
                key={m.id}
                tmdbId={m.id}
                title={m.title}
                posterPath={m.poster_path}
                subtitle={m.release_date ? m.release_date.slice(0, 4) : ''}
              />
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default SearchPage
