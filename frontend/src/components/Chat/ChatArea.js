import { useState } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

export default function ChatArea({ 
  messages, 
  currentStreamingMessage, 
  selectedConversation,
  input,
  setInput,
  handleSubmit,
  isLoading 
}) {
  const [selectedModel, setSelectedModel] = useState('encyclopedia');

  // Wrap the handleSubmit to include the model type
  const handleSubmitWithModel = (e) => {
    e.preventDefault();
    handleSubmit(e, selectedModel);
  };

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Chat Header */}
      <div className="px-6 py-4 border-b border-[#e2e8f0] bg-white/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="max-w-3xl mx-auto w-full">
          <h2 className="text-[#1a202c] font-medium">{selectedConversation}</h2>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} isStreaming={false} />
          ))}
          {currentStreamingMessage && (
            <ChatMessage 
              message={{ role: 'assistant', content: currentStreamingMessage }} 
              isStreaming={true} 
            />
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-[#e2e8f0] bg-white">
        <div className="max-w-3xl mx-auto w-full px-6 py-4">
          <ChatInput 
            input={input}
            setInput={setInput}
            handleSubmit={handleSubmitWithModel}
            isLoading={isLoading}
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
          />
        </div>
      </div>
    </div>
  );
} 