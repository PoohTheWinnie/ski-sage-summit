import Image from 'next/image';

export default function Sidebar({ selectedConversation, setSelectedConversation, setMessages }) {
  return (
    <div className="w-80 bg-white border-r border-[#e2e8f0] p-6 flex flex-col">
      {/* Logo and Title Area */}
      <div className="mb-8 flex flex-col items-center">
        <div className="w-12 h-12 mb-3 flex items-center justify-center">
          <Image src="/logo.png" alt="Ski Sage Summit Logo" width={48} height={48} />
        </div>
        <h1 className="text-2xl font-bold text-[#1a202c] tracking-tight">Ski Sage</h1>
      </div>
      
      {/* New Chat Button */}
      <button 
        className="flex items-center gap-3 w-full rounded-full px-4 py-3 text-[#2c5282] hover:bg-[#f1f5f9] transition-colors"
        onClick={() => {
          setMessages([]);
          setSelectedConversation('New Chat');
        }}
      >
        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-r from-[#2c5282] to-[#4299e1] text-white">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 3.33334V12.6667" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M3.33331 8H12.6666" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </div>
        <span className="font-medium">New chat</span>
      </button>
      
      {/* Recent Conversations */}
      <div className="flex-1 overflow-y-auto mt-6">
        {selectedConversation !== 'New Chat' && (
          <div className="space-y-1">
            <button
              className="w-full text-left p-3 rounded-lg bg-[#f1f5f9] text-[#1a202c] font-medium"
              onClick={() => setSelectedConversation(selectedConversation)}
            >
              {selectedConversation}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}