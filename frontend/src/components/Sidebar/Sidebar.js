import Image from 'next/image';

export default function Sidebar({ selectedConversation, setSelectedConversation, setMessages }) {
  return (
    <div className="w-80 bg-white border-r border-[#e2e8f0] p-6 flex flex-col">
      {/* Logo and Title Area */}
      <div className="mb-8 flex flex-col items-center">
        <div className="w-12 h-12 mb-3 rounded-xl bg-gradient-to-br from-[#2c5282] to-[#4299e1] flex items-center justify-center">
          <Image src="/logo.png" alt="Ski Sage Summit Logo" width={48} height={48} />
        </div>
        <h1 className="text-2xl font-bold text-[#1a202c] tracking-tight">Ski Sage</h1>
      </div>
      
      <button 
        className="w-full bg-gradient-to-r from-[#2c5282] to-[#4299e1] text-white rounded-xl p-3.5 mb-6 transition-all hover:shadow-lg hover:opacity-90 font-medium"
        onClick={() => {
          setMessages([]);
          setSelectedConversation('New Chat');
        }}
      >
        New Conversation
      </button>
      
      {/* Recent Conversations */}
      <div className="flex-1 overflow-y-auto">
        <h2 className="text-sm font-medium text-[#64748b] uppercase tracking-wider mb-3">Recent Chats</h2>
        <div className="space-y-1">
          {['Ski Equipment Guide', 'Trail Recommendations', 'Weather Analysis'].map((chat) => (
            <button
              key={chat}
              className={`w-full text-left p-3 rounded-lg transition-all ${
                selectedConversation === chat 
                  ? 'bg-[#f1f5f9] text-[#1a202c] font-medium' 
                  : 'hover:bg-[#f8fafc] text-[#64748b]'
              }`}
              onClick={() => setSelectedConversation(chat)}
            >
              {chat}
            </button>
          ))}
        </div>
      </div>

      {/* Settings Area */}
      <div className="pt-4 border-t border-[#e2e8f0]">
        <button className="w-full text-left p-3 rounded-lg hover:bg-[#f8fafc] text-[#64748b] flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Settings
        </button>
      </div>
    </div>
  );
} 