type BadgeVariant = 'normal' | 'moderate'

interface BadgeProps {
  label: string
  variant?: BadgeVariant
}

export default function Badge({ label, variant = 'normal' }: BadgeProps) {
  const styles: Record<BadgeVariant, string> = {
    normal: 'bg-green-50 text-green-700 border-green-200',
    moderate: 'bg-amber-50 text-amber-700 border-amber-200',
  }
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium border ${styles[variant]}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${variant === 'normal' ? 'bg-green-500' : 'bg-amber-500'}`} />
      {label}
    </span>
  )
}
