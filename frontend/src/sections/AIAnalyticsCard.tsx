import GaugeChart from '../components/charts/GaugeChart'
import ProgressBar from '../components/ui/ProgressBar'
import CalendarIcon from '../components/icons/CalendarIcon'

export default function AIAnalyticsCard() {
  return (
    <div className="col-span-4 bg-gray-950 rounded-2xl p-5 flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h3 className="text-white text-base font-semibold">AI Analytics Insights</h3>
        <span className="flex items-center gap-1.5 text-[11px] text-gray-400 bg-gray-800 rounded-lg px-3 py-1.5">
          <CalendarIcon />
          26 Mar - 24 Apr, 2025
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-gray-900 rounded-xl p-3.5">
          <p className="text-[11px] text-gray-300 font-semibold mb-0.5">Neurodegenerative Risk</p>
          <p className="text-[10px] text-gray-500 leading-tight mb-2">No signs of cognitive decline or neurodegenerative disease.</p>
          <p className="text-2xl font-bold text-white mb-2">12%</p>
          <ProgressBar value={12} color="red" />
        </div>
        <div className="bg-gray-900 rounded-xl p-3.5">
          <p className="text-[11px] text-gray-300 font-semibold mb-0.5">Chronic Disease Markers</p>
          <p className="text-[10px] text-gray-500 leading-tight mb-2">Inflammation elevated—further monitoring advised.</p>
          <p className="text-2xl font-bold text-white mb-2">30%</p>
          <ProgressBar value={30} color="orange" />
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center">
        <GaugeChart value={22} />
      </div>
    </div>
  )
}
