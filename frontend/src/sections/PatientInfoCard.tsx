export default function PatientInfoCard() {
  return (
    <div className="bg-white border-b border-slate-100 px-8 py-3">
      <div className="max-w-[1400px] mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center text-white font-bold text-sm shrink-0 shadow-sm">
            JD
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-800 leading-none mb-0.5">
              John Doe
            </p>
            <p className="text-xs text-slate-400">
              Patient #BIO-20240112 · DOB: Jan 12, 1984
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
