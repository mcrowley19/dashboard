type ProgressBarColor = 'green' | 'red' | 'orange'

interface ProgressBarProps {
  value: number
  max?: number
  color?: ProgressBarColor
}

export default function ProgressBar({ value, max = 100, color = 'green' }: ProgressBarProps) {
  const percentage = (value / max) * 100
  const tracks: Record<ProgressBarColor, string> = {
    green: 'bg-gradient-to-r from-green-500 to-green-400',
    red: 'bg-gradient-to-r from-green-500 via-yellow-400 to-red-500',
    orange: 'bg-gradient-to-r from-green-500 via-yellow-400 to-red-500',
  }

  return (
    <div className="relative w-full h-2 rounded-full bg-gray-200 overflow-visible">
      <div className={`h-full rounded-full ${tracks[color]}`} style={{ width: '100%' }} />
      <div
        className="absolute top-1/2 -translate-y-1/2 w-3.5 h-3.5 rounded-full bg-white border-2 border-green-500 shadow-md"
        style={{ left: `${Math.min(percentage, 97)}%` }}
      />
    </div>
  )
}
