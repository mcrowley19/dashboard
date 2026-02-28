const FAMILY_HISTORY = [
  {
    type: "diagnostic" as const,
    label: "Oscar Wilde",
    relation: "Father",
    conditions: ["Heart disease", "Cancer", "plague"],
  },
];

export default function FamilyHistoryCard() {
  return (
    <div
      className="col-span-4 row-span-2 bg-white rounded-2xl flex flex-col border border-slate-100"
      style={{
        height: 380,
        boxShadow:
          "inset 4px 0 0 #14B8A6, 0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-4 pb-3 shrink-0 border-b border-slate-50 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded-lg bg-teal-50 flex items-center justify-center shrink-0">
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#14B8A6"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M10.5 1.5C8.01 1.5 6 3.51 6 6v12c0 2.49 2.01 4.5 4.5 4.5S15 20.49 15 18V6c0-2.49-2.01-4.5-4.5-4.5z" />
            <line x1="6" y1="12" x2="15" y2="12" />
          </svg>
        </div>
        <h3 className="text-slate-800 text-sm font-semibold tracking-tight">
          Family History
        </h3>
      </div>

      <div className="flex flex-col gap-4 overflow-y-auto flex-1 px-5 py-4">
        {FAMILY_HISTORY.map(({ type, label, relation, conditions }) => (
          <div key={type} className="flex gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-xs font-semibold text-slate-800">
                  {label}
                </span>
              </div>
              <div className="flex items-center gap-2 mb-1.5">
                <span className="text-xs font-semibold text-slate-800">
                  {relation}
                </span>
              </div>
              <ul className="text-[11px] text-slate-400 space-y-0.5 list-disc list-inside">
                {conditions.map((condition) => (
                  <li key={condition}>{condition}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
