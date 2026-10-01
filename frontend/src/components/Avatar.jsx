// Circle with the first letter of the username (the backend has no avatar images)
function Avatar({ username, size = 36 }) {
  return (
    <span className="avatar" style={{ width: size, height: size, fontSize: size * 0.45 }}>
      {username ? username[0].toUpperCase() : '?'}
    </span>
  )
}

export default Avatar
