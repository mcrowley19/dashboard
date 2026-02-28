import Navbar from "../components/Navbar";
import PatientHistoryCard from "../sections/PatientHistoryCard";
import MedicationsCard from "../sections/MedicationsCard";
import InteractionsCard from "../sections/InteractionsCard";
import HistorySummaryCard from "../sections/HistorySummaryCard";
import FamilyHistoryCard from "../sections/FamilyHistoryCard";

export default function ClearVaultDashboard() {
  return (
    <div
      className="min-h-screen bg-slate-50"
      style={{ fontFamily: "'DM Sans', sans-serif" }}
    >
      <Navbar />

      <div className="p-6 max-w-[1400px] mx-auto">
        <div className="grid grid-cols-12 gap-5">
          <PatientHistoryCard />
          <HistorySummaryCard />
          <MedicationsCard />
          <InteractionsCard />
          <FamilyHistoryCard />
        </div>
      </div>
    </div>
  );
}
