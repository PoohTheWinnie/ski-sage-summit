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
  );
} 