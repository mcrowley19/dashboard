import { useSearchParams } from "react-router-dom";
import Navbar from "../components/Navbar";
import PatientHistoryCard from "../sections/PatientHistoryCard";
import MedicationsCard from "../sections/MedicationsCard";
import InteractionsCard from "../sections/InteractionsCard";
import HistorySummaryCard from "../sections/HistorySummaryCard";
import FamilyHistoryCard from "../sections/FamilyHistoryCard";

const DEFAULT_PATIENT_ID = "BIO-20231205";

export default function MetricareDashboard() {
  const [searchParams] = useSearchParams();
  const patientId = searchParams.get("patient") || DEFAULT_PATIENT_ID;

  return (
    <div
      className="min-h-screen bg-slate-50"
      style={{ fontFamily: "'DM Sans', sans-serif" }}
    >
      <Navbar />

      <div className="p-6 max-w-[1400px] mx-auto">
        <div className="grid grid-cols-12 gap-5">
          <PatientHistoryCard patientId={patientId} />
          <HistorySummaryCard patientId={patientId} />
          <MedicationsCard patientId={patientId} />
          <InteractionsCard patientId={patientId} />
          <FamilyHistoryCard patientId={patientId} />
        </div>
      </div>
    </div>
  );
}
