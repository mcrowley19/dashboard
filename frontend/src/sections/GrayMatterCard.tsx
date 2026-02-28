import Badge from '../components/ui/Badge'
import ComparisonBar from '../components/ui/ComparisonBar'

export default function GrayMatterCard() {
  return (
    <div className="col-span-4 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-900 text-sm font-semibold">Gray Matter Volume</h3>
        <Badge label="Normal" />
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-4">
        715 <span className="text-base font-normal text-gray-400">cm³</span>
      </p>
      <div className="space-y-3">
        <ComparisonBar
          label="Average"
          value={730}
          unit="cm³"
          maxValue={1000}
          color="linear-gradient(to right, #22c55e, #16a34a)"
          isBelow={false}
        />
        <ComparisonBar
          label="Your Result"
          value={715}
          unit="cm³"
          maxValue={1000}
          color="linear-gradient(to right, #22c55e, #15803d)"
          isBelow={false}
        />
      </div>
    </div>
  )
}
