interface GaugeChartProps {
  value: number
  max?: number
}

export default function GaugeChart({ value, max = 40 }: GaugeChartProps) {
  const percentage = value / max
  const startAngle = Math.PI * 0.75
  const endAngle = Math.PI * 2.25
  const currentAngle = startAngle + (endAngle - startAngle) * percentage
  const segments = 30

  const segmentElements = Array.from({ length: segments }, (_, i) => {
    const ratio = i / segments
    const angle = startAngle + (endAngle - startAngle) * ratio
    const x1 = 50 + 38 * Math.cos(angle)
    const y1 = 50 + 38 * Math.sin(angle)
    const x2 = 50 + 46 * Math.cos(angle)
    const y2 = 50 + 46 * Math.sin(angle)

    let color: string
    if (ratio < 0.33) color = '#22c55e'
    else if (ratio < 0.66) color = '#f59e0b'
    else color = '#ef4444'

    const isActive = angle <= currentAngle

    return (
      <line
        key={i}
        x1={x1} y1={y1} x2={x2} y2={y2}
        stroke={isActive ? color : 'rgba(255,255,255,0.1)'}
        strokeWidth="3"
        strokeLinecap="round"
      />
    )
  })

  return (
    <svg viewBox="0 0 100 80" className="w-full h-full">
      {segmentElements}
      <text x="50" y="58" textAnchor="middle" fill="white" fontSize="18" fontWeight="bold" fontFamily="sans-serif">
        {value}
      </text>
    </svg>
  )
}
