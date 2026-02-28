interface SparklineChartProps {
  data: number[]
}

export default function SparklineChart({ data }: SparklineChartProps) {
  const width = 320
  const height = 60
  const padding = 4

  const maxVal = Math.max(...data)
  const minVal = Math.min(...data)
  const range = maxVal - minVal || 1

  const points = data.map((d, i) => ({
    x: padding + (i / (data.length - 1)) * (width - padding * 2),
    y: padding + (1 - (d - minVal) / range) * (height - padding * 2),
  }))

  const pathD = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ')
  const areaD = `${pathD} L ${points[points.length - 1].x} ${height} L ${points[0].x} ${height} Z`

  const highlight = points[22]

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-16">
      <defs>
        <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="rgba(74,222,175,0.25)" />
          <stop offset="100%" stopColor="rgba(74,222,175,0)" />
        </linearGradient>
      </defs>
      <path d={areaD} fill="url(#sparkFill)" />
      <path d={pathD} fill="none" stroke="#4adeaf" strokeWidth="1.5" />
      {highlight && (
        <>
          <circle cx={highlight.x} cy={highlight.y} r="10" fill="rgba(45,55,72,0.9)" stroke="#4adeaf" strokeWidth="1.5" />
          <text x={highlight.x} y={highlight.y - 2} textAnchor="middle" fill="white" fontSize="7" fontWeight="600">81</text>
          <text x={highlight.x} y={highlight.y + 6} textAnchor="middle" fill="#9ca3af" fontSize="5">Mar 24</text>
        </>
      )}
    </svg>
  )
}
