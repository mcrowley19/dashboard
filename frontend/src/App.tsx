import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import MetricareDashboard from './pages/MetricareDashboard'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<MetricareDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
