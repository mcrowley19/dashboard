import SymmetryBars from '../components/charts/SymmetryBars'
import Badge from '../components/ui/Badge'

export default function BrainSymmetryCard() {
  return (
    <div className="col-span-4 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-900 text-sm font-semibold">Brain Symmetry Index</h3>
        <Badge label="Normal" />
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-3">0.96</p>
      <SymmetryBars />
    </div>
  )
}
