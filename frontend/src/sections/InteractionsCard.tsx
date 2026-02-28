import { useEffect, useState } from "react";
import { fetchContraindications, type ContraindicationEntry } from "../api/client";

const SEVERITY_BADGE: Record<string, string> = {
  SEVERE: "bg-red-50 text-red-600 border border-red-100",
  MODERATE: "bg-amber-50 text-amber-600 border border-amber-100",
  LOW: "bg-green-50 text-green-600 border border-green-100",
};

export default function InteractionsCard({ patientId }: { patientId: string }) {
  const [contraindications, setContraindications] = useState<ContraindicationEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchContraindications(patientId)
      .then(setContraindications)
      .catch((e) =>
        setError(e instanceof Error ? e.message : "Failed to load contraindications")
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
          "inset 4px 0 0 #F59E0B, 0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-4 pb-3 shrink-0 border-b border-slate-50 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded-lg bg-amber-50 flex items-center justify-center shrink-0">
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#F59E0B"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </div>
        <h3 className="text-slate-800 text-sm font-semibold tracking-tight">
          Potential Contraindications
        </h3>
      </div>

      <div className="flex flex-col gap-4 overflow-y-auto flex-1 px-5 py-4">
        {loading && (
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span className="inline-block w-4 h-4 border-2 border-amber-200 border-t-amber-500 rounded-full animate-spin" />
            Loading…
          </div>
        )}
        {error && <div className="text-xs text-red-600">{error}</div>}
        {!loading && !error && contraindications.length === 0 && (
          <div className="text-xs text-slate-400">No contraindications on file.</div>
        )}
        {!loading &&
          !error &&
          contraindications.map(({ label, severity, items }, i) => (
            <div key={`${label}-${i}`} className="flex gap-3">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-xs font-semibold text-slate-800">{label}</span>
                  {severity && (
                    <span
                      className={`text-[10px] rounded-full px-2 py-0.5 font-semibold ${
                        SEVERITY_BADGE[severity] ??
                        "bg-slate-100 text-slate-500 border border-slate-200"
                      }`}
                    >
                      {severity}
                    </span>
                  )}
                </div>
                <ul className="text-[11px] text-slate-400 space-y-0.5 list-disc list-inside">
                  {(items ?? []).map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
                {/* TODO: show description when backend populates from OpenFDA */}
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}
