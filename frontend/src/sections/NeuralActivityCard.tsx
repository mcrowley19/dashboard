import SparklineChart from '../components/charts/SparklineChart'
import Badge from '../components/ui/Badge'

const SPARK_DATA = [78, 80, 79, 81, 77, 78, 82, 80, 79, 83, 81, 80, 82, 84, 80, 79, 81, 83, 82, 80, 79, 81, 81, 82, 83, 80, 79, 81]
const DATE_LABELS = [1, 5, 9, 13, 17, 21, 25, 27]

export default function NeuralActivityCard() {
  return (
    <div className="col-span-4 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-gray-900 text-sm font-semibold">Neural Activity Index</h3>
        <Badge label="Normal" />
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-1">
        82 <span className="text-base font-normal text-gray-400">/100</span>
      </p>
      <SparklineChart data={SPARK_DATA} />
      <div className="flex justify-between text-[10px] text-gray-400 mt-1 px-1">
        {DATE_LABELS.map(n => <span key={n}>{n}</span>)}
      </div>
    </div>
  )
}
