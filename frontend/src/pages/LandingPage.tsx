import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import LandingScene from '../components/landing/LandingScene'

const tiles = [
  {
    title: 'The problem with today’s medical dashboards',
    body: 'Most medical dashboards are messy, outdated, and overloaded. Information is buried in tabs, legacy systems don’t talk to each other, and critical patient history is scattered across multiple tools. Clinicians waste time clicking, scrolling, and reconciling data instead of focusing on care.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
      </svg>
    ),
  },
  {
    title: 'Patient history in one place',
    body: 'Metricare brings a patient’s full history into one coherent timeline. Diagnoses, medications, labs, imaging, notes, and referrals are organized chronologically and by category. You see the full picture at a glance instead of hunting through separate modules.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
      </svg>
    ),
  },
  {
    title: 'AI that keeps your dashboard up to date',
    body: 'We use AI to keep the dashboard current and relevant. It surfaces the most important information for each visit, highlights changes since the last encounter, and suggests follow-ups or gaps in care. The view stays clean and actionable instead of bloated.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM12 10.5a.75.75 0 01.75.75v.75h.75a.75.75 0 010 1.5h-.75v.75a.75.75 0 01-1.5 0v-.75h-.75a.75.75 0 010-1.5h.75v-.75a.75.75 0 01.75-.75z" />
      </svg>
    ),
  },
  {
    title: 'Built for clarity, not clutter',
    body: 'Every part of Metricare is designed to reduce noise. We avoid endless dropdowns, duplicate entries, and redundant alerts. The dashboard prioritizes what matters for the current encounter while still giving you quick access to the full record when you need it.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
      </svg>
    ),
  },
  {
    title: 'Who it’s for',
    body: 'Metricare is for care teams tired of juggling multiple tools and outdated interfaces. Whether you’re in primary care, specialty practice, or a health system, the platform adapts to your workflow and integrates with your existing systems.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
      </svg>
    ),
  },
  {
    title: 'What’s next',
    body: 'We’re continuously improving Metricare based on feedback from clinicians. New integrations, smarter AI summaries, and more flexible views are in the pipeline. Our focus: a medical dashboard that is up to date, easy to use, and free of mess and bloat.',
    icon: (
      <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
      </svg>
    ),
  },
]

export default function LandingPage() {
  const [showBackToTop, setShowBackToTop] = useState(false)

  useEffect(() => {
    const onScroll = () => setShowBackToTop(window.scrollY > 400)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })
  return (
    <div className="relative w-full bg-white" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      {/* Hero */}
      <section className="relative min-h-screen w-full overflow-hidden bg-white">
        <LandingScene />
        <div className="absolute inset-0 flex flex-col items-start justify-center pl-[12%] pr-[8%] md:pl-[14%] max-w-xl text-left pointer-events-none">
          <div className="pointer-events-auto">
            <h1
              className="text-5xl sm:text-6xl md:text-7xl font-bold tracking-tight text-gray-900 opacity-0 animate-fly-in"
              style={{ animationDelay: '0.15s' }}
            >
              Metricare
            </h1>
            <p
              className="mt-4 text-lg sm:text-xl text-gray-600 max-w-md opacity-0 animate-fade-in-up"
              style={{ animationDelay: '0.28s' }}
            >
              Patient history and AI in one place. A medical dashboard that stays clear and up to date.
            </p>
            <div
              className="mt-10 flex flex-row flex-nowrap items-center gap-4 opacity-0 animate-fade-in-up"
              style={{ animationDelay: '0.42s' }}
            >
              <Link
                to="/dashboard"
                className="rounded-full bg-gray-900 px-8 py-3.5 text-base font-semibold text-white shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 focus:ring-offset-gray-50 transition pointer-events-auto hover:scale-[1.02] active:scale-[0.98] inline-flex items-center gap-2 whitespace-nowrap"
              >
                Open dashboard
                <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
                </svg>
              </Link>
              <a
                href="#about"
                className="rounded-full border border-gray-300 bg-white px-8 py-3.5 text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 focus:ring-offset-gray-50 transition pointer-events-auto hover:scale-[1.02] active:scale-[0.98] inline-flex items-center gap-2 whitespace-nowrap"
              >
                Learn more
                <svg className="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                </svg>
              </a>
            </div>
          </div>
        </div>
        <div
          className="absolute bottom-6 left-[12%] md:left-[14%] text-left text-gray-500 text-sm opacity-0 animate-fade-in"
          style={{ animationDelay: '0.58s' }}
        >
          Scroll or tap to explore
        </div>
      </section>

      {/* About */}
      <section id="about" className="relative py-16 md:py-24 px-6 md:px-10 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-14">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight">About Metricare</h2>
            <p className="mt-4 text-gray-600 text-lg leading-relaxed">
              A medical dashboard built for the way clinicians work today. Patient history, real-time data, and AI in one up-to-date view—without the clutter and bloat.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 md:gap-6">
            {tiles.map((tile, i) => (
              <article
                key={i}
                className="group rounded-2xl bg-gray-50 border border-gray-100 p-6 md:p-7 shadow-sm hover:shadow-md hover:border-gray-200 transition-all duration-200"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-white border border-gray-100 flex items-center justify-center group-hover:border-gray-200 transition-colors">
                    {tile.icon}
                  </div>
                  <div className="min-w-0 flex-1">
                    <h3 className="text-base md:text-lg font-semibold text-gray-900 leading-snug">
                      {tile.title}
                    </h3>
                    <p className="mt-2 text-sm md:text-base text-gray-600 leading-relaxed">
                      {tile.body}
                    </p>
                  </div>
                </div>
              </article>
            ))}
          </div>

          <div className="mt-14 pt-8 border-t border-gray-100 text-center">
            <p className="text-gray-500 text-sm">
              Placeholder content. Metricare is a medical dashboard for patient history with AI integration, built to replace messy and bloated legacy systems.
            </p>
          </div>
        </div>
      </section>

      {/* Back to top */}
      <button
        type="button"
        onClick={scrollToTop}
        aria-label="Back to top"
        className={`fixed bottom-6 right-6 z-50 w-12 h-12 rounded-full bg-gray-900 text-white shadow-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 focus:ring-offset-gray-50 transition-all duration-300 flex items-center justify-center cursor-pointer ${
          showBackToTop ? 'opacity-100 translate-y-0' : 'opacity-0 pointer-events-none translate-y-2'
        }`}
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 15.75l7.5-7.5 7.5 7.5" />
        </svg>
      </button>
    </div>
  )
}
