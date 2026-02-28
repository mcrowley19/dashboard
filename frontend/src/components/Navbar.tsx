import { Link, useLocation } from 'react-router-dom'

const NAV_ITEMS = [
  { label: 'Home', emoji: '🏠', path: '/' },
  { label: 'Documents', emoji: '📄', path: '#' },
  { label: 'Analytics', emoji: '📊', path: '/dashboard' },
  { label: 'Database', emoji: '💾', path: '#' },
] as const

export default function Navbar() {
  const location = useLocation()
  const isActive = (path: string) => location.pathname === path || (path === '/dashboard' && location.pathname.startsWith('/dashboard'))

  return (
    <nav className="flex items-center justify-between px-8 py-3 bg-white border-b border-gray-100">
      <Link to="/" className="flex items-center gap-2 hover:opacity-90 transition">
        <div className="w-7 h-7 bg-gray-900 rounded-lg flex items-center justify-center">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
        </div>
        <span className="text-lg font-bold text-gray-900">ClearVault</span>
      </Link>

      <div className="flex items-center bg-gray-100 rounded-full p-1">
        {NAV_ITEMS.map(({ label, emoji, path }) => {
          const active = path !== '#' && isActive(path)
          const content = (
            <span className="flex items-center gap-1.5">
              <span>{emoji}</span>
              {label}
            </span>
          )
          return path === '#' ? (
            <button
              key={label}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
                active ? 'bg-gray-900 text-white shadow-sm' : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {content}
            </button>
          ) : (
            <Link
              key={label}
              to={path}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all ${
                active ? 'bg-gray-900 text-white shadow-sm' : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {content}
            </Link>
          )
        })}
      </div>

      <div className="flex items-center gap-4">
        <button className="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 hover:bg-gray-200 transition-colors">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
            <path d="M13.73 21a2 2 0 0 1-3.46 0" />
          </svg>
        </button>
        <div className="w-9 h-9 rounded-full bg-gradient-to-br from-amber-200 to-amber-400 border-2 border-white shadow-sm" />
      </div>
    </nav>
  )
}
