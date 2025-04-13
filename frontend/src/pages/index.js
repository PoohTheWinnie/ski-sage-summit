import { useState, useEffect, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';
import Sidebar from '../components/Sidebar/Sidebar';
import ChatArea from '../components/Chat/ChatArea';
import useChat from '../hooks/useChat';
import useConversations from '../hooks/useConversations';

export default function Home() {
  const [selectedConversationId, setSelectedConversationId] = useState(null);
  const {
    messages,
    setMessages,
    input,
    setInput,
    isLoading,
    chatId,
    setChatId,
    handleSubmit
  } = useChat();
  
  const {
    conversations,
    addConversation,
    updateConversation,
    deleteConversation,
    getConversation
  } = useConversations();
  
  // Prevent scrolling on the document
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = '';
    };
  }, []);

  // When a user selects a conversation, load its messages and update chatId
  useEffect(() => {
    if (!selectedConversationId) {
      setChatId(null);
      return;
    }
    
    const conversation = getConversation(selectedConversationId);
    if (conversation) {
      setMessages(conversation.messages || []);
      setChatId(selectedConversationId);
    }
  }, [selectedConversationId, setChatId]);

  // Create a new chat
  const startNewChat = () => {
    setMessages([]);
    setSelectedConversationId(null);
    setChatId(null);
  };

  // Custom submit handler to create a new conversation if needed
  const handleChatSubmit = async (e, modelType) => {
    const userMessage = { role: 'user', content: input };
    
    // If this is the first message and no conversation is selected, create one
    if (messages.length === 0) {
      const id = uuidv4();
      // Create a title from the first few words of the message
      const title = input.split(' ').slice(0, 4).join(' ') + (input.length > 20 ? '...' : '');
      
      // Add the conversation with the user message already included
      addConversation(id, title, [userMessage]);
      setSelectedConversationId(id);
      setChatId(id);
    }
    
    // Submit the message
    await handleSubmit(e, modelType);
  };

  // Handle deleting a conversation
  const handleDeleteConversation = (id) => {
    deleteConversation(id);
    if (selectedConversationId === id) {
      startNewChat();
    }
  };

  // Add immediate update effect
  useEffect(() => {
    if (selectedConversationId && messages.length > 0) {
      const conversation = getConversation(selectedConversationId);
      if (conversation && JSON.stringify(conversation.messages) !== JSON.stringify(messages)) {
        updateConversation(selectedConversationId, { messages });
      }
    }
  }, [messages, selectedConversationId, updateConversation, getConversation]);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-white">
      {/* Sidebar - Fixed width */}
      <Sidebar 
        conversations={conversations}
        selectedConversationId={selectedConversationId}
        setSelectedConversationId={setSelectedConversationId}
        startNewChat={startNewChat}
        deleteConversation={handleDeleteConversation}
      />
      
      {/* Main content area - Centered */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 flex flex-col items-center justify-center overflow-hidden">
          <div className="w-full h-full max-w-2xl mx-auto overflow-hidden">
            <ChatArea 
              messages={messages}
              selectedConversation={selectedConversationId ? 
                getConversation(selectedConversationId)?.title || 'New Chat' : 
                'New Chat'
              }
              input={input}
              setInput={setInput}
              handleSubmit={handleChatSubmit}
              isLoading={isLoading}
            />
          </div>
        </div>
      </div>
    </div>
  );
} 