import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import StarRating from '../components/StarRating'
import { getMovie } from '../api'

const POSTER_BASE = 'https://image.tmdb.org/t/p/w500'
const BACKDROP_BASE = 'https://image.tmdb.org/t/p/w1280'

function MovieDetailPage() {
  // useParams reads the :id from the URL (/movies/27205 -> id = "27205")
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError('')
    getMovie(id)
      .then((data) => { if (!cancelled) setMovie(data) })
      .catch((err) => { if (!cancelled) setError(err.message) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [id])

  if (loading) return <div className="skeleton detail-skeleton" />

  if (error || !movie) {
    return <div className="empty">{error || 'Movie not found.'} <Link to="/search">Back to search</Link></div>
  }

  const director = movie.credits?.crew?.find((c) => c.job === 'Director')?.name
  const year = movie.release_date ? movie.release_date.slice(0, 4) : null
  // TMDB rates out of 10; our stars are out of 5
  const stars = Math.round((movie.vote_average || 0) / 2)

  const heroStyle = movie.backdrop_path
    ? {
        backgroundImage: `linear-gradient(90deg, rgba(18,6,10,0.95) 25%, rgba(18,6,10,0.6)), url(${BACKDROP_BASE + movie.backdrop_path})`,
      }
    : undefined

  return (
    <section className="detail-hero" style={heroStyle}>
      {movie.poster_path ? (
        <img className="detail-poster" src={POSTER_BASE + movie.poster_path} alt={movie.title} />
      ) : (
        <div className="detail-poster movie-card-empty"><span>{movie.title}</span></div>
      )}
      <div>
        <h1>
          {movie.title}
          {year && <span className="muted detail-year"> ({year})</span>}
        </h1>
        {movie.tagline && <p className="muted"><em>{movie.tagline}</em></p>}
        <div className="row">
          {movie.genres?.map((g) => <span key={g.id} className="badge">{g.name}</span>)}
          {movie.runtime > 0 && <span className="muted">{movie.runtime} min</span>}
          {director && <span className="muted">Directed by {director}</span>}
        </div>
        {movie.vote_count > 0 && (
          <div className="row detail-avg">
            <StarRating value={stars} />
            <span className="muted">{(movie.vote_average / 2).toFixed(1)} / 5 on TMDB</span>
          </div>
        )}
        <p className="detail-overview">{movie.overview || 'No overview available.'}</p>
      </div>
    </section>
  )
}

export default MovieDetailPage
