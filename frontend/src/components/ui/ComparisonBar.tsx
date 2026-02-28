interface ComparisonBarProps {
  label: string
  value: number
  unit: string
  maxValue: number
  color: string
  isBelow: boolean
}

export default function ComparisonBar({ label, value, unit, maxValue, color, isBelow }: ComparisonBarProps) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between items-center">
        <span className="text-xs text-gray-500">{label}</span>
        <span className="text-xs text-gray-700 font-medium flex items-center gap-1">
          {value} {unit}
          {isBelow ? (
            <span className="text-red-400">★</span>
          ) : (
            <span className="text-green-400">★</span>
          )}
        </span>
      </div>
      <div className="w-full h-3 rounded-full overflow-hidden bg-gray-100">
        <div className="h-full rounded-full" style={{ width: `${(value / maxValue) * 100}%`, background: color }} />
      </div>
    </div>
  )
}
