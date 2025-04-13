import { useState, useEffect, useCallback, useMemo } from 'react';

export default function useConversations() {
  const [conversations, setConversations] = useState([]);

  // Load conversations from localStorage on initial render
  useEffect(() => {
    try {
      const storedConversations = localStorage.getItem('conversations');
      if (storedConversations) {
        setConversations(JSON.parse(storedConversations));
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  }, []);

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem('conversations', JSON.stringify(conversations));
    } catch (error) {
      console.error('Error saving conversations:', error);
    }
  }, [conversations]);

  // Add a new conversation
  const addConversation = useCallback((id, title, messages) => {
    const newConversation = {
      id,
      title,
      messages: messages || [],
      createdAt: new Date().toISOString(),
    };
    
    setConversations(prev => [newConversation, ...prev]);
    return newConversation;
  }, []);

  // Update an existing conversation
  const updateConversation = useCallback((id, updatedData) => {
    setConversations(prev => {
      // Check if the conversation exists and if the data is actually different
      const conversation = prev.find(c => c.id === id);
      if (!conversation) return prev;
      
      const updated = { ...conversation, ...updatedData };
      if (JSON.stringify(conversation) === JSON.stringify(updated)) {
        return prev; // No changes needed
      }
      
      return prev.map(conv => 
        conv.id === id ? updated : conv
      );
    });
  }, []);

  // Delete a conversation
  const deleteConversation = useCallback((id) => {
    setConversations(prev => prev.filter(conversation => conversation.id !== id));
  }, []);

  // Get a conversation by id - memoize to avoid re-renders
  const getConversation = useCallback((id) => {
    return conversations.find(conversation => conversation.id === id);
  }, [conversations]);

  // Memoize the return value to prevent unnecessary re-renders
  return useMemo(() => ({
    conversations,
    addConversation,
    updateConversation,
    deleteConversation,
    getConversation
  }), [conversations, addConversation, updateConversation, deleteConversation, getConversation]);
} 