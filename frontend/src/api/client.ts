/**
 * Backend API base URL. Set VITE_API_URL in .env for production.
 */
const API_BASE =
  (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, "") ||
  "http://localhost:8000";

export function getApiBase(): string {
  return API_BASE;
}

export type SummaryItem = { type: "diagnostic"; summary: string };

export type HistoryEntry = {
  type: "diagnostic";
  label: string;
  date?: string;
  items: string[];
};

/**
 * Fetches patient clinical history from the backend.
 */
export async function fetchPatientHistory(patientId: string): Promise<HistoryEntry[]> {
  const base = getApiBase();
  const res = await fetch(`${base}/patient/${patientId}/history`);
  if (!res.ok) throw new Error("Failed to load patient history");
  const data = (await res.json()) as HistoryEntry[];
  return data;
}

export type MedicationEntry = {
  type: "diagnostic";
  label: string;
  conflicts?: string[];
  items: string[];
  /** Set when OpenFDA description is implemented on the backend. */
  description?: string | null;
};

/**
 * Fetches patient medications from the backend (OpenFDA-ready; description not yet implemented).
 */
export async function fetchPatientMedications(patientId: string): Promise<MedicationEntry[]> {
  const base = getApiBase();
  const res = await fetch(`${base}/patient/${patientId}/medications`);
  if (!res.ok) throw new Error("Failed to load medications");
  const data = (await res.json()) as MedicationEntry[];
  return data;
}

export type ContraindicationEntry = {
  type: "diagnostic";
  label: string;
  severity: string;
  items: string[];
  /** Set when OpenFDA description is implemented on the backend. */
  description?: string | null;
};

/**
 * Fetches potential contraindications from the backend (OpenFDA; description not yet implemented).
 */
export async function fetchContraindications(patientId: string): Promise<ContraindicationEntry[]> {
  const base = getApiBase();
  const res = await fetch(`${base}/patient/${patientId}/contraindications`);
  if (!res.ok) throw new Error("Failed to load contraindications");
  const data = (await res.json()) as ContraindicationEntry[];
  return data;
}

/**
 * Fetches patient info, history, medications, family history, and contraindications,
 * then calls the backend to generate an AI summary that considers all of these.
 * Returns the summary items array.
 */
export async function fetchPatientSummary(patientId: string): Promise<SummaryItem[]> {
  const base = getApiBase();

  const [patientRes, historyRes, medsRes, familyRes, contraRes] = await Promise.all([
    fetch(`${base}/patient/${patientId}`),
    fetch(`${base}/patient/${patientId}/history`),
    fetch(`${base}/patient/${patientId}/medications`),
    fetch(`${base}/patient/${patientId}/family_history`),
    fetch(`${base}/patient/${patientId}/contraindications`),
  ]);

  if (!patientRes.ok || !historyRes.ok || !medsRes.ok) {
    throw new Error("Failed to load patient data");
  }

  const patient = (await patientRes.json()) as { name: string };
  const history = (await historyRes.json()) as Array<{ label: string; date?: string; items?: string[] }>;
  const medications = (await medsRes.json()) as Array<{ label: string; items?: string[] }>;
  const familyHistory = familyRes.ok
    ? ((await familyRes.json()) as Array<{ label: string; relation?: string; conditions?: string[] }>)
    : [];
  const contraindications = contraRes.ok
    ? ((await contraRes.json()) as Array<{ label: string; severity?: string; items?: string[] }>)
    : [];

  const summaryRes = await fetch(`${base}/patient/summary`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      patient_name: patient.name,
      history: history.map((h) => ({
        label: h.label,
        date: h.date ?? "",
        items: h.items ?? [],
      })),
      medications: medications.map((m) => ({
        label: m.label,
        items: m.items ?? [],
      })),
      family_history: familyHistory.map((f) => ({
        label: f.label,
        relation: f.relation ?? "",
        conditions: f.conditions ?? [],
      })),
      contraindications: contraindications.map((c) => ({
        label: c.label,
        severity: c.severity ?? "",
        items: c.items ?? [],
      })),
    }),
  });

  if (!summaryRes.ok) {
    const err = await summaryRes.json().catch(() => ({ detail: summaryRes.statusText }));
    throw new Error(typeof err.detail === "string" ? err.detail : "Failed to generate summary");
  }

  const data = (await summaryRes.json()) as SummaryItem[];
  return data;
}
