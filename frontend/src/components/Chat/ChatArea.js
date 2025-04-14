import { useState, useEffect, useRef } from 'react';
import { ScrollShadow } from "@nextui-org/scroll-shadow";
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import LoadingMessage from './LoadingMessage';
import UserMessage from './UserMessage';

export default function ChatArea({ 
  messages, 
  input,
  setInput,
  handleSubmit,
  isLoading 
}) {
  const [selectedModel, setSelectedModel] = useState('encyclopedia');
  const hasMessages = messages.length > 0 || isLoading;
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSubmitWithModel = (e) => {
    e.preventDefault();
    handleSubmit(e, selectedModel);
  };

  return (
    <div className="flex flex-col h-full w-full overflow-hidden">
      {/* Empty State with Centered Content */}
      {hasMessages ? (
        <>
          <ScrollShadow
            ref={messagesContainerRef}
            className="flex-1 w-full overflow-y-auto overflow-x-hidden"
            hideScrollBar={true}
          >
            <div className="w-full h-full flex flex-col items-center">
              <div className="w-full max-w-xl space-y-4 p-6">
                {messages.map((message, index) => (
                  message.role === 'user' ? (
                    <UserMessage key={index} message={message} />
                  ) : (
                    <ChatMessage 
                      key={index} 
                      message={message} 
                      isStreaming={false}
                    />
                  )
                ))}
                {isLoading && (
                  <div className="flex justify-center">
                    <LoadingMessage variant="default" lines={3} />
                  </div>
                )}
              </div>
            </div>
          </ScrollShadow>
          <div className="w-full border-t border-gray-100 flex-shrink-0">
            <div className="max-w-xl mx-auto px-4 py-4">
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
          <h1 className="text-4xl font-bold mb-3" style={{ color: '#1B3B4B' }}>
            Your Ultimate Skiing Buddy
          </h1>
          <div className="w-full max-w-xl px-4">
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