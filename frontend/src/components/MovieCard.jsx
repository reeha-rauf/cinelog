import { Link } from 'react-router-dom'

const POSTER_BASE = 'https://image.tmdb.org/t/p/w342'

// Gradient fallbacks so movies without a poster still look intentional
const GRADIENTS = [
  'linear-gradient(160deg, #5a1730, #1a0710)',
  'linear-gradient(160deg, #164a3a, #08160f)',
  'linear-gradient(160deg, #6b2a14, #1c0b06)',
  'linear-gradient(160deg, #2a3f5c, #0b121c)',
  'linear-gradient(160deg, #4a1d5c, #14081c)',
]

// A poster with the title underneath. Links to the movie detail page.
function MovieCard({ tmdbId, title, posterPath, subtitle }) {
  return (
    <Link to={`/movies/${tmdbId}`} className="movie-card">
      {posterPath ? (
        <img src={POSTER_BASE + posterPath} alt={title} />
      ) : (
        <div className="movie-card-empty" style={{ background: GRADIENTS[tmdbId % GRADIENTS.length] }}>
          <span>{title}</span>
        </div>
      )}
      <div className="movie-card-title">{title}</div>
      {subtitle && <div className="muted movie-card-sub">{subtitle}</div>}
    </Link>
  )
}

export default MovieCard
