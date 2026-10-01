// Shows 1-5 stars. Pass onChange to make it clickable (used later for logging a watch).
function StarRating({ value = 0, onChange }) {
  return (
    <span className="stars">
      {[1, 2, 3, 4, 5].map((n) => (
        <span
          key={n}
          className={`star ${n <= value ? 'on' : ''} ${onChange ? 'clickable' : ''}`}
          onClick={onChange ? () => onChange(n) : undefined}
        >
          ★
        </span>
      ))}
    </span>
  )
}

export default StarRating
