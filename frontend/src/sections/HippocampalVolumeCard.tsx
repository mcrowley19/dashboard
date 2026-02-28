import Badge from '../components/ui/Badge'
import ComparisonBar from '../components/ui/ComparisonBar'

export default function HippocampalVolumeCard() {
  return (
    <div className="col-span-4 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-900 text-sm font-semibold">Hippocampal Volume</h3>
        <Badge label="Moderate" variant="moderate" />
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-4">
        1.2 <span className="text-base font-normal text-gray-400">cm³</span>
      </p>
      <div className="space-y-3">
        <ComparisonBar
          label="Average"
          value={1.15}
          unit="cm³"
          maxValue={2}
          color="linear-gradient(to right, #f59e0b, #f97316)"
          isBelow
        />
        <ComparisonBar
          label="Your Result"
          value={1.2}
          unit="cm³"
          maxValue={2}
          color="linear-gradient(to right, #f97316, #ea580c)"
          isBelow={false}
        />
      </div>
    </div>
  )
}
