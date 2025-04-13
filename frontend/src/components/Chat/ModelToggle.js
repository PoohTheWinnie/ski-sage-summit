export default function ModelToggle({ selectedModel, setSelectedModel }) {
  return (
    <div className="flex items-center gap-3 mb-3">
      <div className="flex rounded-lg border border-[#e2e8f0] p-0.5 bg-[#f8fafc]">
        <button
          onClick={() => setSelectedModel('encyclopedia')}
          className={`px-4 py-1.5 text-sm rounded-md transition-all ${
            selectedModel === 'encyclopedia'
              ? 'bg-white text-[#2c5282] shadow-sm font-medium'
              : 'text-[#64748b] hover:text-[#2c5282]'
          }`}
        >
          Encyclopedia Mode
        </button>
        <button
          onClick={() => setSelectedModel('map')}
          className={`px-4 py-1.5 text-sm rounded-md transition-all ${
            selectedModel === 'map'
              ? 'bg-white text-[#2c5282] shadow-sm font-medium'
              : 'text-[#64748b] hover:text-[#2c5282]'
          }`}
        >
          Map Mode
        </button>
      </div>
    </div>
  );
} 