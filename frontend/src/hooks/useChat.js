import { useState, useRef, useEffect, useCallback } from 'react';

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatId, setChatId] = useState(null);
  const isMounted = useRef(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  useEffect(() => {
    console.log(messages);
  }, [messages]);

  const handleSubmit = useCallback(async (e, modelType) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const userInput = input; // Store a copy to avoid closure issues
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Use absolute URL for production
      const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/chat`;
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userInput,
          modelType: modelType,
          chatId: chatId
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to get response');
      }

      const data = await response.json();
      
      if (isMounted.current) {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: data.response 
        }]);
      }
    } catch (error) {
      console.error('Chat Error:', error);
      if (isMounted.current) {
        setError(error.message);
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: 'Sorry, there was an error processing your request.' 
        }]);
      }
    } finally {
      if (isMounted.current) {
        setIsLoading(false);
      }
    }
  }, [input, chatId]);

  return {
    messages,
    setMessages,
    input,
    setInput,
    isLoading,
    error,
    chatId,
    setChatId,
    handleSubmit
  };
} 