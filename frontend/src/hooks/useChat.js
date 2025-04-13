import { useState, useRef, useEffect } from 'react';

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState('');
  const isMounted = useRef(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  const handleSubmit = async (e, modelType) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: input,
          modelType: modelType
        }),
      });

      const data = await response.json();
      
      if (isMounted.current) {
        setMessages(prev => [...prev, { 
          role: 'assistant', 
          content: data.response 
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      if (isMounted.current) {
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
  };

  return {
    messages,
    setMessages,
    input,
    setInput,
    isLoading,
    currentStreamingMessage,
    handleSubmit
  };
} 