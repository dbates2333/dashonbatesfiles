import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Navigation from './components/Navigation'
import RepWorkspace from './pages/RepWorkspace'
import CROCommandView from './pages/CROCommandView'

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-900 flex flex-col">
        <Navigation />
        <main className="flex-1 overflow-hidden">
          <Routes>
            <Route path="/" element={<Navigate to="/command" replace />} />
            <Route path="/command" element={<CROCommandView />} />
            <Route path="/workspace" element={<RepWorkspace />} />
            <Route path="/workspace/:dealId" element={<RepWorkspace />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}
