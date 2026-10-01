const API_BASE = 'http://localhost:8000';

export async function signup(username, email, password) {
    const res = await fetch(`${API_BASE}/auth/signup`,{
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
    });
    if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Signup failed');
  }
  return res.json();
}

export async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    credentials: 'include',
    body: formData,
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'Login failed');
  }
  return res.json();
}

export async function getCurrentUser() {
  const res = await fetch(`${API_BASE}/auth/me`, {
    credentials: 'include',
  });
  if (!res.ok) return null;
  return res.json();
}

export async function getFeed() {
  const res = await fetch(`${API_BASE}/logs/feed`, {
    credentials: 'include',
  });
  if (!res.ok) {
    throw new Error('Failed to load feed');
  }
  return res.json();
}

export async function searchMovies(query) {
  const res = await fetch(`${API_BASE}/movies/search?query=${encodeURIComponent(query)}`, {
    credentials: 'include',
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || 'Search failed');
  }
  return res.json();
}

export async function getMovie(tmdbId) {
  const res = await fetch(`${API_BASE}/movies/${tmdbId}`, {
    credentials: 'include',
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to load movie');
  }
  return res.json();
}

export async function logout() {
  await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
}