import { useState, useRef, useEffect } from 'react';

export default function useChat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState('');
  const isMounted = useRef(true);
  const streamTimer = useRef(null);

  useEffect(() => {
    return () => {
      isMounted.current = false;
      if (streamTimer.current) {
        clearTimeout(streamTimer.current);
      }
    };
  }, []);

  const handleSubmit = async (e, modelType) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setCurrentStreamingMessage('');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ 
          message: input,
          modelType: modelType
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let streamingText = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim();
            
            if (data === '[DONE]') {
              if (isMounted.current) {
                // Add small delay before finalizing message
                streamTimer.current = setTimeout(() => {
                  setMessages(prev => [...prev, { 
                    role: 'assistant', 
                    content: streamingText.trim() 
                  }]);
                  setCurrentStreamingMessage('');
                }, 150);
              }
              break;
            }
            
            if (data) {
              streamingText += data + ' ';
              if (isMounted.current) {
                // Add small delay for smoother updates
                streamTimer.current = setTimeout(() => {
                  setCurrentStreamingMessage(streamingText.trim());
                }, 50);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, there was an error processing your request.' 
      }]);
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