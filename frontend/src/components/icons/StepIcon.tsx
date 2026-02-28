import type { ReactNode } from 'react'

type StepType = 'diagnostic' | 'specialist' | 'lifestyle' | 'monitoring'

interface StepIconProps {
  type: StepType
}

const icons: Record<StepType, ReactNode> = {
  diagnostic: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 2h6l3 7H6L9 2z" /><circle cx="12" cy="15" r="5" /><path d="M12 12v6" /><path d="M9 15h6" />
    </svg>
  ),
  specialist: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
    </svg>
  ),
  lifestyle: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  ),
  monitoring: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />
    </svg>
  ),
}

export default function StepIcon({ type }: StepIconProps) {
  return (
    <div className="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center text-gray-600">
      {icons[type]}
    </div>
  )
}
