import CalendarIcon from "../components/icons/CalendarIcon";

export default function PatientHistoryCard() {
  const HISTORY = [
    {
      type: "diagnostic" as const,
      label: "Went to Roscommon",
      date: "Jan 2025",
      items: [
        "Can cause you to want to do BESS",
        "Lunacy",
        "Play gracefully with ideas",
      ],
    },
  ];

  return (
    <div
      className="col-span-8 bg-white rounded-2xl relative flex flex-col border border-slate-100"
      style={{
        height: 380,
        boxShadow:
          "inset 4px 0 0 #3B82F6, 0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-4 pb-3 shrink-0 border-b border-slate-50 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center text-blue-500 shrink-0">
          <CalendarIcon />
        </div>
        <h3 className="text-slate-800 text-sm font-semibold tracking-tight">
          Patient History
        </h3>
      </div>

      {/* Timeline list */}
      <div className="flex flex-col overflow-y-auto flex-1 divide-y divide-slate-50">
        {HISTORY.map(({ type, label, date, items }) => (
          <div
            key={type}
            className="flex gap-3 px-5 py-3 hover:bg-slate-50/70 transition-colors"
          >
            {/* Timeline dot */}
            <div className="shrink-0 mt-1 w-2 h-2 rounded-full bg-blue-300 ring-2 ring-blue-100" />

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-semibold text-slate-800">
                  {label}
                </span>
                {date && (
                  <span className="text-[10px] bg-blue-50 text-blue-500 border border-blue-100 rounded-full px-2 py-0.5 font-medium shrink-0">
                    {date}
                  </span>
                )}
              </div>
              <ul className="text-[11px] text-slate-400 space-y-0.5 list-disc list-inside">
                {items.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
        <div className="flex flex-col items-center justify-center gap-1"></div>
      </div>
    </div>
  );
}
