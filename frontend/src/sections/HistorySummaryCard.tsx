import { useEffect, useState } from "react";
import { fetchPatientSummary, type SummaryItem } from "../api/client";

/** Renders summary text: **bold** = bold, ***bold*** = red and bold. Only interprets ** and ***. */
function SummaryWithBold({ text }: { text: string }) {
  const partRegex = /\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*/g;
  let pos = 0;
  let match;
  const parts: { type: "normal" | "bold" | "severe"; text: string }[] = [];
  while ((match = partRegex.exec(text)) !== null) {
    if (match.index > pos) parts.push({ type: "normal", text: text.slice(pos, match.index) });
    if (match[1] !== undefined) {
      parts.push({ type: "severe", text: match[1] });
    } else {
      parts.push({ type: "bold", text: match[2] ?? "" });
    }
    pos = match.index + match[0].length;
  }
  if (pos < text.length) parts.push({ type: "normal", text: text.slice(pos) });

  return (
    <>
      {parts.map((seg, i) => {
        if (seg.type === "normal") return seg.text;
        if (seg.type === "severe") {
          return (
            <strong key={i} className="font-semibold text-red-600">
              {seg.text}
            </strong>
          );
        }
        return (
          <strong key={i} className="font-semibold text-slate-700">
            {seg.text}
          </strong>
        );
      })}
    </>
  );
}

export default function HistorySummaryCard({ patientId }: { patientId: string }) {
  const [items, setItems] = useState<SummaryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    fetchPatientSummary(patientId)
      .then((data) => {
        if (!cancelled) setItems(data);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof Error ? e.message : "Failed to load summary");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [patientId]);

  return (
    <div
      className="col-span-4 bg-white rounded-2xl flex flex-col border border-slate-100"
      style={{
        height: 380,
        boxShadow:
          "inset 4px 0 0 #6366F1, 0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.04)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-4 pb-3 shrink-0 border-b border-slate-50 flex items-center gap-2.5">
        <div className="w-7 h-7 rounded-lg bg-indigo-50 flex items-center justify-center shrink-0">
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#6366F1"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 2l1.68 5.16A2 2 0 0 0 15.06 8.5L20 10l-4.94 1.5a2 2 0 0 0-1.38 1.34L12 18l-1.68-5.16A2 2 0 0 0 8.94 11.5L4 10l4.94-1.5a2 2 0 0 0 1.38-1.34L12 2z" />
            <path d="M19 2v4M21 4h-4" />
            <path d="M5 18v3M6.5 19.5h-3" />
          </svg>
        </div>
        <h3 className="text-slate-800 text-sm font-semibold tracking-tight">
          AI Summary
        </h3>
        <span className="ml-auto inline-flex items-center gap-1 text-[10px] font-semibold text-indigo-500 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-full">
          ✦ AI
        </span>
      </div>

      {/* Body */}
      <div className="flex-1 overflow-y-auto overflow-x-hidden min-h-0 w-full px-5 py-4">
        {loading && (
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <span className="inline-block w-4 h-4 border-2 border-indigo-200 border-t-indigo-500 rounded-full animate-spin" />
            Generating summary…
          </div>
        )}
        {error && (
          <div className="text-xs text-red-600">
            {error}
          </div>
        )}
        {!loading && !error && items.length === 0 && (
          <div className="text-xs text-slate-400">No summary available.</div>
        )}
        {!loading && !error && items.length > 0 && items.map(({ summary }, i) => (
          <div
            key={i}
            className="text-xs text-slate-500 break-words leading-relaxed"
          >
            {summary && <SummaryWithBold text={summary} />}
          </div>
        ))}
      </div>
    </div>
  );
}
