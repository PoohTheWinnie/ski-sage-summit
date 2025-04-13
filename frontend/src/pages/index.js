import { useState } from 'react';
import Sidebar from '../components/Sidebar/Sidebar';
import ChatArea from '../components/Chat/ChatArea';
import useChat from '../hooks/useChat';

export default function Home() {
  const [selectedConversation, setSelectedConversation] = useState('New Chat');
  const {
    messages,
    setMessages,
    input,
    setInput,
    isLoading,
    currentStreamingMessage,
    handleSubmit
  } = useChat();

  return (
    <div className="flex h-screen bg-[#f8fafc]">
      <Sidebar 
        selectedConversation={selectedConversation}
        setSelectedConversation={setSelectedConversation}
        setMessages={setMessages}
      />
      <div className="flex-1 flex flex-col items-center justify-center">
        {
          messages.length === 0 && (
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-blue-900 mb-3">
                Your Ultimate Skiing Encyclopedia
              </h1>
            </div>
          )
        }

        {/* Centered Chat Area */}
        <div className="w-full max-w-3xl px-4">
          <ChatArea 
            messages={messages}
            currentStreamingMessage={currentStreamingMessage}
            selectedConversation={selectedConversation}
            input={input}
            setInput={setInput}
            handleSubmit={handleSubmit}
            isLoading={isLoading}
          />
        </div>
      </div>
    </div>
  );
} 