import { useState, useEffect, useRef } from 'react';
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
  const hasMessages = messages.length > 0 || currentStreamingMessage;
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage, isLoading]);

  const handleSubmitWithModel = (e) => {
    e.preventDefault();
    handleSubmit(e, selectedModel);
  };

  return (
    <div className="flex-1 flex flex-col h-full max-h-screen">
      {/* Empty State with Centered Content */}
      {hasMessages ? (
        <>
          {/* Messages Container - Set explicit height and enable scrolling */}
          <div className="flex-1 overflow-y-auto min-h-0 scrollbar-hide">
            <div className="max-w-3xl mx-auto space-y-6 p-6">
              {messages.map((message, index) => (
                <div key={index} className="flex justify-center">
                  <div className="w-full">
                    <ChatMessage message={message} isStreaming={false} />
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start w-full">
                  <div className="bg-[#f1f5f9] rounded-md p-4 max-w-[600px] flex items-center space-x-2">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} /> {/* Scroll anchor */}
            </div>
          </div>

          {/* Input Area - Fixed at bottom */}
          <div className="w-full border-t border-gray-100">
            <div className="max-w-3xl mx-auto px-6 py-4">
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
        </>
      ) : (
        <div className="flex-1 flex flex-col items-center justify-center">
          <div className="w-full max-w-3xl px-6">
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
      )}
    </div>
  );
} 