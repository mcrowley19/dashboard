type BrainView = 'top' | 'front' | 'side'

interface BrainThumbnailProps {
  view: BrainView
  index: number
}

export default function BrainThumbnail({ view, index }: BrainThumbnailProps) {
  return (
    <div className="w-14 h-14 rounded-lg overflow-hidden border border-gray-600/30 bg-gray-900 flex items-center justify-center">
      <svg viewBox="0 0 60 60" className="w-full h-full">
        <defs>
          <radialGradient id={`thumb-${index}`} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#4ade80" stopOpacity="0.5" />
            <stop offset="50%" stopColor="#f59e0b" stopOpacity="0.3" />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>
        </defs>
        <ellipse cx="30" cy="30" rx={view === 'side' ? '18' : '22'} ry="22" fill="none" stroke="rgba(100,200,150,0.3)" strokeWidth="0.5" />
        <ellipse cx="30" cy="30" rx={view === 'side' ? '12' : '16'} ry="16" fill={`url(#thumb-${index})`} />
        {view === 'top' && (
          <line x1="30" y1="8" x2="30" y2="52" stroke="rgba(100,200,150,0.15)" strokeWidth="0.5" />
        )}
        {view === 'side' && (
          <ellipse cx="30" cy="30" rx="8" ry="14" fill="none" stroke="rgba(200,150,80,0.2)" strokeWidth="0.5" />
        )}
        {view === 'front' && (
          <>
            <ellipse cx="22" cy="28" rx="8" ry="10" fill="none" stroke="rgba(200,80,80,0.2)" strokeWidth="0.5" />
            <ellipse cx="38" cy="28" rx="8" ry="10" fill="none" stroke="rgba(200,80,80,0.2)" strokeWidth="0.5" />
          </>
        )}
      </svg>
    </div>
  )
}
