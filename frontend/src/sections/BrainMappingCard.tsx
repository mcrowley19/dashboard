import BrainHeatmap from '../components/charts/BrainHeatmap'
import BrainThumbnail from '../components/ui/BrainThumbnail'

export default function BrainMappingCard() {
  return (
    <div className="col-span-8 bg-gray-950 rounded-2xl p-5 relative overflow-hidden" style={{ minHeight: 380 }}>
      <h3 className="text-white text-base font-semibold mb-3">Brain Mapping</h3>
      <div className="flex gap-4">
        <div className="flex flex-col gap-3 z-10">
          <BrainThumbnail view="top" index={0} />
          <BrainThumbnail view="front" index={1} />
          <BrainThumbnail view="side" index={2} />
        </div>
        <div className="flex-1 flex items-center justify-center relative">
          <BrainHeatmap />
        </div>
        <div className="flex flex-col items-center justify-center gap-1">
          <span className="text-[10px] text-red-400 font-medium">0.50 —</span>
          <div
            className="w-2.5 rounded-full"
            style={{ height: 160, background: 'linear-gradient(to bottom, #ef4444, #f97316, #eab308, #22c55e, #064e3b)' }}
          />
          <span className="text-[10px] text-gray-400 font-medium mt-0.5">0.25 —</span>
          <div
            className="w-2.5 rounded-full mt-1"
            style={{ height: 40, background: 'linear-gradient(to bottom, #22c55e, #064e3b)' }}
          />
          <span className="text-[10px] text-green-800 font-medium mt-0.5">0.01 —</span>
        </div>
      </div>
    </div>
  )
}
