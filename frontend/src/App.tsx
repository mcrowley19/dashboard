import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import ClearVaultDashboard from './pages/ClearVaultDashboard'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<ClearVaultDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
