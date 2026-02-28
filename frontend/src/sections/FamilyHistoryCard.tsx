import { useEffect, useState } from "react";
import {
  fetchPatientFamilyHistory,
  type FamilyHistoryEntry,
} from "../api/client";

export default function FamilyHistoryCard({
  patientId,
}: {
  patientId: string;
}) {
  const [familyHistory, setFamilyHistory] = useState<FamilyHistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchPatientFamilyHistory(patientId)
      .then(setFamilyHistory)
      .catch((e) =>
        setError(
          e instanceof Error ? e.message : "Failed to load family history",
        ),
      )
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [patientId]);

  return (
    <div
      className="col-span-4 row-span-2 bg-white rounded-2xl flex flex-col border border-slate-100"
      style={{
        height: 380,
        boxShadow:
          "inset 4px 0 0 #b8148aff, 0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-4 pb-3 shrink-0  border-slate-50 flex items-center gap-2.5">
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
            <circle cx="12" cy="7" r="4" />
            <path d="M5 21v-1a7 7 0 0 1 14 0v1" />
          </svg>
        </div>
        <h3 className="text-slate-800 text-sm font-semibold tracking-tight">
          Family History
        </h3>
      </div>

      <div className="flex flex-col gap-4 overflow-y-auto flex-1 px-5 py-4">
        {loading && (
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span className="inline-block w-4 h-4 border-2 border-teal-200 border-t-teal-500 rounded-full animate-spin" />
            Loading…
          </div>
        )}
        {error && <div className="text-xs text-red-600">{error}</div>}
        {!loading &&
          !error &&
          familyHistory.map(({ label, relation, conditions }) => (
            <div key={label} className="flex gap-3">
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
                  {(conditions ?? []).map((condition) => (
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
