import { useState, useEffect } from "react";
import { Link, useSearchParams, useNavigate } from "react-router-dom";
import { fetchPatients, type Patient } from "../api/client";

const DEFAULT_PATIENT_ID = "BIO-20231205";

export default function Navbar() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [currentPatient, setCurrentPatient] = useState<Patient | null>(null);
  const [query, setQuery] = useState("");
  const [showResults, setShowResults] = useState(false);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const patientIdFromUrl = searchParams.get("patient") || DEFAULT_PATIENT_ID;

  useEffect(() => {
    let cancelled = false;
    fetchPatients()
      .then((list) => {
        if (!cancelled) setPatients(list);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    const match = patients.find((p) => p.id === patientIdFromUrl);
    setCurrentPatient(match ?? patients[0] ?? null);
  }, [patients, patientIdFromUrl]);

  const filtered = query.trim()
    ? patients.filter(
        (p) =>
          p.name.toLowerCase().includes(query.toLowerCase()) ||
          p.id.toLowerCase().includes(query.toLowerCase()),
      )
    : patients;

  return (
    <nav className="flex items-center justify-between px-6 py-2.5 bg-white border-b border-slate-200">
      <div className="flex items-center gap-8">
        {/* Brand */}
        <Link
          to="/"
          className="flex items-center gap-2.5 hover:opacity-80 transition-opacity"
          aria-label="Metricare home"
        >
          <div className="w-8 h-8 rounded-lg bg-blue-50 border border-blue-200 flex items-center justify-center">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="#3B82F6"
            >
              <path d="M12 21.593c-5.63-5.539-11-10.297-11-14.402 0-3.791 3.068-5.191 5.281-5.191 1.312 0 4.151.501 5.719 4.457 1.59-3.968 4.464-4.447 5.726-4.447 2.54 0 5.274 1.621 5.274 5.181 0 4.069-5.136 8.625-11 14.402z" />
            </svg>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-[15px] font-semibold text-slate-800 tracking-tight">
              Metricare
            </span>
          </div>
        </Link>
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
                      navigate(`/dashboard?patient=${encodeURIComponent(patient.id)}`);
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
          {currentPatient ? (
            <>
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
            </>
          ) : (
            <span className="text-[12px] text-slate-400">Loading patients…</span>
          )}
        </div>
      </div>
    </nav>
  );
}
