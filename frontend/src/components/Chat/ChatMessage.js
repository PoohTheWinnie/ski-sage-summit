export default function ChatMessage({ message, isStreaming }) {
  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} w-full`}>
      <div
        className={`w-full rounded-md p-4 whitespace-pre-wrap break-words ${
          message.role === 'user'
            ? 'bg-gradient-to-r from-[#2c5282] to-[#4299e1] text-white' 
            : 'bg-[#f1f5f9] text-[#1a202c]'
        }`}
      >
        {message.content}
        {isStreaming && <span className="inline-block w-1 h-4 ml-1 bg-[#1a202c] animate-pulse"/>}
      </div>
    </div>
  );
} 