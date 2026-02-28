import { useState } from "react";

const NAV_ITEMS = [
  {
    label: "Home",
    icon: (
      <svg
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        <polyline points="9 22 9 12 15 12 15 22" />
      </svg>
    ),
  },
  {
    label: "Documents",
    icon: (
      <svg
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
      </svg>
    ),
  },
  {
    label: "Analytics",
    icon: (
      <svg
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <line x1="18" y1="20" x2="18" y2="10" />
        <line x1="12" y1="20" x2="12" y2="4" />
        <line x1="6" y1="20" x2="6" y2="14" />
      </svg>
    ),
  },
  {
    label: "Database",
    icon: (
      <svg
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <ellipse cx="12" cy="5" rx="9" ry="3" />
        <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" />
        <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      </svg>
    ),
  },
];

// Mock patient data for search
const PATIENTS = [
  { id: "BIO-20240112", name: "John Doe", dob: "Jan 12, 1984", initials: "JD" },
  {
    id: "BIO-20231205",
    name: "Sarah Miller",
    dob: "Dec 5, 1991",
    initials: "SM",
  },
  {
    id: "BIO-20240308",
    name: "Robert Chen",
    dob: "Mar 8, 1976",
    initials: "RC",
  },
  {
    id: "BIO-20240521",
    name: "Emily Watson",
    dob: "May 21, 1989",
    initials: "EW",
  },
];

export default function Navbar({ activeTab = "Analytics" }) {
  const [currentPatient, setCurrentPatient] = useState(PATIENTS[0]);
  const [query, setQuery] = useState("");
  const [showResults, setShowResults] = useState(false);

  const filtered = query.trim()
    ? PATIENTS.filter(
        (p) =>
          p.name.toLowerCase().includes(query.toLowerCase()) ||
          p.id.toLowerCase().includes(query.toLowerCase()),
      )
    : PATIENTS;

  return (
    <nav className="flex items-center justify-between px-6 py-2.5 bg-white border-b border-slate-200">
      <div className="flex items-center gap-8">
        {/* Brand */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-50 border border-emerald-200 flex items-center justify-center">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              className="text-emerald-500"
            >
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" opacity="0.5" />
              <path d="M2 12l10 5 10-5" opacity="0.75" />
            </svg>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-[15px] font-semibold text-slate-800 tracking-tight">
              BioSync
            </span>
          </div>
        </div>

        {/* Divider */}
        <div className="w-px h-5 bg-slate-200" />

        {/* Navigation tabs */}
        <div className="flex items-center gap-0.5">
          {NAV_ITEMS.map(({ label, icon }) => {
            const isActive = label === activeTab;
            return (
              <button
                key={label}
                className={`
                  group relative flex items-center gap-2 px-4 py-2 rounded-lg text-[13px] font-medium transition-all duration-200
                  ${
                    isActive
                      ? "text-slate-800 bg-slate-100 border border-slate-200"
                      : "text-slate-400 border border-transparent hover:text-slate-600 hover:bg-slate-50"
                  }
                `}
              >
                <span
                  className={`transition-colors ${isActive ? "text-emerald-500" : "text-slate-300 group-hover:text-slate-400"}`}
                >
                  {icon}
                </span>
                {label}
                {isActive && (
                  <div className="absolute inset-x-3 -bottom-[13px] h-px bg-gradient-to-r from-transparent via-emerald-400 to-transparent" />
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Patient search */}
        <div className="relative">
          <div className="flex items-center gap-2 w-56 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 focus-within:border-emerald-300 focus-within:ring-2 focus-within:ring-emerald-100 transition-all">
            <svg
              width="13"
              height="13"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-slate-400 shrink-0"
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              placeholder="Search patients..."
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                setShowResults(true);
              }}
              onFocus={() => setShowResults(true)}
              onBlur={() => setTimeout(() => setShowResults(false), 150)}
              className="w-full bg-transparent text-[12px] text-slate-700 placeholder-slate-400 outline-none"
            />
          </div>

          {showResults && (
            <div className="absolute top-full mt-1.5 left-0 w-64 bg-white border border-slate-200 rounded-xl shadow-lg shadow-slate-100 overflow-hidden z-50">
              {filtered.length === 0 ? (
                <p className="px-3 py-2.5 text-[12px] text-slate-400">
                  No patients found
                </p>
              ) : (
                filtered.map((patient) => (
                  <button
                    key={patient.id}
                    onMouseDown={() => {
                      setCurrentPatient(patient);
                      setQuery("");
                      setShowResults(false);
                    }}
                    className="w-full flex items-center gap-2.5 px-3 py-2 hover:bg-slate-50 transition-colors text-left"
                  >
                    <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-[10px] shrink-0">
                      {patient.initials}
                    </div>
                    <div>
                      <p className="text-[12px] font-semibold text-slate-700 leading-none mb-0.5">
                        {patient.name}
                      </p>
                      <p className="text-[11px] text-slate-400">{patient.id}</p>
                    </div>
                  </button>
                ))
              )}
            </div>
          )}
        </div>

        {/* Divider */}
        <div className="w-px h-5 bg-slate-200" />

        {/* Current patient info */}
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-[10px] shrink-0">
            {currentPatient.initials}
          </div>
          <div>
            <p className="text-[12px] font-semibold text-slate-700 leading-none mb-0.5">
              {currentPatient.name}
            </p>
            <p className="text-[11px] text-slate-400 leading-none">
              #{currentPatient.id} · DOB: {currentPatient.dob}
            </p>
          </div>
        </div>
      </div>
    </nav>
  );
}
