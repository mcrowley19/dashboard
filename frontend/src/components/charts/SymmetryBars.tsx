export default function SymmetryBars() {
  const leftBars = Array.from({ length: 20 }, () => 0.3 + Math.random() * 0.7)
  const rightBars = Array.from({ length: 20 }, () => 0.3 + Math.random() * 0.7)

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="flex items-end gap-[2px] h-16 justify-center">
        {leftBars.map((h, i) => (
          <div
            key={`l-${i}`}
            className="w-[6px] rounded-sm"
            style={{ height: `${h * 100}%`, backgroundColor: `rgba(249, 115, 22, ${0.5 + h * 0.5})` }}
          />
        ))}
        <div className="w-2" />
        {rightBars.map((h, i) => (
          <div
            key={`r-${i}`}
            className="w-[6px] rounded-sm"
            style={{ height: `${h * 100}%`, backgroundColor: `rgba(249, 115, 22, ${0.5 + h * 0.5})` }}
          />
        ))}
      </div>
      <div className="flex justify-between w-full text-xs text-gray-400 px-2">
        <span>Left Hemisphere</span>
        <span>Right Hemisphere</span>
      </div>
    </div>
  )
}
