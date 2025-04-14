import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Image from 'next/image';

export default function ChatMessage({ message, isStreaming }) {
  const contentRef = useRef(null);
  const measureRef = useRef(null);
  const isImage = message.content.includes("https://oaidalleapiprodscus.blob.core.windows.net/");

  useEffect(() => {
    adjustWidth();
    // Add resize listener to handle window resizing
    window.addEventListener('resize', adjustWidth);
    return () => window.removeEventListener('resize', adjustWidth);
  }, [message.content]);

  const adjustWidth = () => {
    const content = contentRef.current;
    const measure = measureRef.current;
    
    if (content && measure && !isImage) {
      // Reset width to get natural content width
      content.style.width = 'auto';
      measure.textContent = message.content;
      
      const lines = message.content.split('\n');
      const parentWidth = content.parentElement.offsetWidth;
      const maxWidth = Math.min(parentWidth, 600); // Maximum width of 600px
      
      if (lines.length > 1 || imageUrl) {
        // Use full width (with max-width) for multiline messages or with images
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
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        ref={measureRef}
        className="absolute invisible whitespace-pre p-4"
        style={{ fontFamily: 'inherit' }}
      />
      
      <div
        ref={contentRef}
        className={`rounded-md p-4 break-words transition-all duration-200 prose prose-sm max-w-none`}
        style={{
          width: 'auto',
          background: message.role === 'user' 
            ? 'linear-gradient(to right, #1B3B4B, #2C5D7C)' 
            : '#E6EEF2',
          color: message.role === 'user' ? '#E6EEF2' : '#0F2634'
        }}
      >
        { 
          isImage ? (
            <div className="mt-3">
              <a href={message.content} target="_blank" rel="noopener noreferrer">
                <div className="relative w-full h-64 rounded-md overflow-hidden">
                  <Image
                    src={message.content}
                    alt="Map result"
                    className="object-contain "
                    width={600}
                    height={600}
                  />
                </div>
              </a>
            </div>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          )
        }
      </div>
    </div>
  );
}