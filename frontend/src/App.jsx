import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import Layout from './components/Layout'
import SignupPage from './pages/SignupPage'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import SearchPage from './pages/SearchPage'
import MovieDetailPage from './pages/MovieDetailPage'

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/movies/:id" element={<MovieDetailPage />} />
        </Route>
      </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
