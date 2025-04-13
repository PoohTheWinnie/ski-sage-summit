import React, { useMemo, useCallback } from 'react';
import Image from 'next/image';
import { CalendarDays } from 'lucide-react';

const Sidebar = ({ 
  conversations, 
  selectedConversationId, 
  setSelectedConversationId,
  startNewChat,
  deleteConversation
}) => {
  // Helper to format the date
  const formatDate = useCallback((dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }, []);

  // Handle conversation selection
  const handleSelectConversation = useCallback((id) => {
    setSelectedConversationId(id);
  }, [setSelectedConversationId]);

  // Handle conversation deletion with stopPropagation to prevent selection
  const handleDeleteConversation = useCallback((e, id) => {
    e.stopPropagation();
    deleteConversation(id);
  }, [deleteConversation]);

  // Memoize conversation list to prevent unnecessary renders
  const conversationsList = useMemo(() => {
    return conversations.map((conversation) => (
      <div 
        key={conversation.id}
        className={`group relative rounded-lg transition-colors overflow-hidden ${
          selectedConversationId === conversation.id 
            ? 'bg-white' 
            : 'hover:bg-white/60'
        }`}
      >
        <button
          className="w-full text-left p-3 pr-9"
          style={{ color: '#0F2634' }}
          onClick={() => handleSelectConversation(conversation.id)}
        >
          <div className="font-medium truncate">
            {conversation.title}
          </div>
          <div className="flex items-center gap-1 mt-1 text-xs text-gray-500">
            <CalendarDays size={12} />
            <span>{formatDate(conversation.createdAt)}</span>
          </div>
        </button>
        
        {/* Delete button */}
        <button
          className="absolute right-2 top-1/2 -translate-y-1/2 p-1 opacity-0 group-hover:opacity-100 hover:bg-gray-100 rounded transition-opacity"
          onClick={(e) => handleDeleteConversation(e, conversation.id)}
          aria-label="Delete conversation"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 4H13M5.5 4V3C5.5 2.44772 5.94772 2 6.5 2H9.5C10.0523 2 10.5 2.44772 10.5 3V4M12 4V13C12 13.5523 11.5523 14 11 14H5C4.44772 14 4 13.5523 4 13V4H12Z" stroke="#0F2634" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </div>
    ));
  }, [conversations, selectedConversationId, handleSelectConversation, handleDeleteConversation, formatDate]);

  return (
    <div className="w-80 p-6 flex flex-col" style={{ backgroundColor: '#E6EEF2' }}>
      {/* Logo and Title Area */}
      <div className="mb-8 flex flex-col items-center">
        <div className="w-12 h-12 mb-3 flex items-center justify-center">
          <Image src="/logo.png" alt="Ski Sage Summit Logo" width={48} height={48} />
        </div>
        <h1 className="text-2xl font-bold tracking-tight" style={{ color: '#0F2634' }}>Ski Sage</h1>
      </div>
      
      {/* New Chat Button */}
      <button 
        className="flex items-center gap-3 w-full rounded-full px-4 py-3 hover:bg-white transition-colors"
        style={{ color: '#1B3B4B' }}
        onClick={startNewChat}
      >
        <div className="flex items-center justify-center w-8 h-8 rounded-full text-white" 
             style={{ background: 'linear-gradient(to right, #1B3B4B, #2C5D7C)' }}>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 3.33334V12.6667" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M3.33331 8H12.6666" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </div>
        <span className="font-medium">New chat</span>
      </button>
      
      {/* Recent Conversations */}
      <div className="flex-1 overflow-y-auto mt-6 space-y-2">
        {conversationsList}
      </div>
    </div>
  );
};

export default React.memo(Sidebar);