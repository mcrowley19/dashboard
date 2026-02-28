import StepIcon from '../components/icons/StepIcon'

const STEPS = [
  {
    type: 'diagnostic' as const,
    label: 'Diagnostic',
    period: 'May - June',
    items: ['Repeat MRI in 3–6 months', 'Cognitive test recommended', 'Confirm markers via blood test'],
  },
  {
    type: 'specialist' as const,
    label: 'Specialist',
    period: 'July',
    items: ['Consult a neurologist (early risk detected)', 'Optional: sleep specialist review', 'Refer to mental health professional'],
  },
  {
    type: 'lifestyle' as const,
    label: 'Lifestyle',
    period: 'Permanent',
    items: ['Start brain-healthy diet', 'Try cognitive training apps', 'Increase aerobic activity'],
  },
  {
    type: 'monitoring' as const,
    label: 'Monitoring',
    period: null,
    items: ['Set re-scan reminder', 'Enable weekly memory checks', 'Activate real-time trend tracking for key biomarkers'],
  },
]

export default function NextStepsCard() {
  return (
    <div className="col-span-4 row-span-2 bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-gray-900 text-base font-semibold">Suggested Next Steps</h3>
        <button className="text-xs font-medium text-gray-600 border border-gray-200 rounded-full px-3 py-1.5 hover:bg-gray-50 transition-colors">
          Create Plan +
        </button>
      </div>

      <div className="flex flex-col gap-4">
        {STEPS.map(({ type, label, period, items }) => (
          <div key={type} className="flex gap-3">
            <StepIcon type={type} />
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-gray-900">{label}</span>
                {period && (
                  <span className="text-[10px] bg-gray-100 text-gray-500 rounded-full px-2 py-0.5">{period}</span>
                )}
              </div>
              <ul className="text-[11px] text-gray-500 space-y-0.5 list-disc list-inside">
                {items.map(item => <li key={item}>{item}</li>)}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
