import { useEffect, useRef } from 'react';

export default function ChatMessage({ message, isStreaming }) {
  const contentRef = useRef(null);
  const measureRef = useRef(null);

  useEffect(() => {
    adjustWidth();
    // Add resize listener to handle window resizing
    window.addEventListener('resize', adjustWidth);
    return () => window.removeEventListener('resize', adjustWidth);
  }, [message.content]);

  const adjustWidth = () => {
    const content = contentRef.current;
    const measure = measureRef.current;
    
    if (content && measure) {
      // Reset width to get natural content width
      content.style.width = 'auto';
      measure.textContent = message.content;
      
      const lines = message.content.split('\n');
      const parentWidth = content.parentElement.offsetWidth;
      const maxWidth = Math.min(parentWidth, 600); // Maximum width of 600px
      
      if (lines.length > 1) {
        // Use full width (with max-width) for multiline messages
        content.style.width = `${maxWidth}px`;
      } else {
        // For single line, adjust to content width
        const contentWidth = measure.offsetWidth;
        const minWidth = 10; // Minimum width
        content.style.width = `${Math.min(Math.max(contentWidth + 5, minWidth), maxWidth)}px`;
      }
    }
  };

  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} w-full`}>
      {/* Hidden measure element */}
      <div
        ref={measureRef}
        className="absolute invisible whitespace-pre p-4"
        style={{ fontFamily: 'inherit' }}
      />
      
      <div
        ref={contentRef}
        className={`rounded-md p-4 whitespace-pre-wrap break-words transition-all duration-200 ${
          message.role === 'user'
            ? 'bg-gradient-to-r from-[#2c5282] to-[#4299e1] text-white' 
            : 'bg-[#f1f5f9] text-[#1a202c]'
        }`}
        style={{ width: 'auto' }}
      >
        {message.content}
        {isStreaming && (
          <span className="inline-block w-1 h-4 ml-1 bg-[#1a202c] animate-pulse"/>
        )}
      </div>
    </div>
  );
} 