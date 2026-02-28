import Navbar from '../components/Navbar'
import BrainMappingCard from '../sections/BrainMappingCard'
import AIAnalyticsCard from '../sections/AIAnalyticsCard'
import NeuralActivityCard from '../sections/NeuralActivityCard'
import BrainSymmetryCard from '../sections/BrainSymmetryCard'
import NextStepsCard from '../sections/NextStepsCard'
import HippocampalVolumeCard from '../sections/HippocampalVolumeCard'
import GrayMatterCard from '../sections/GrayMatterCard'

export default function BioSyncDashboard() {
  return (
    <div className="min-h-screen bg-gray-50" style={{ fontFamily: "'DM Sans', sans-serif" }}>
      <Navbar />
      <div className="p-6 max-w-[1400px] mx-auto">
        <div className="grid grid-cols-12 gap-5">
          <BrainMappingCard />
          <AIAnalyticsCard />
          <NeuralActivityCard />
          <BrainSymmetryCard />
          <NextStepsCard />
          <HippocampalVolumeCard />
          <GrayMatterCard />
        </div>
      </div>
    </div>
  )
}
