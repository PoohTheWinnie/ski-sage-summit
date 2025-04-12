import { useRef, useEffect } from 'react';
import ModelToggle from './ModelToggle';

export default function ChatInput({ 
  input, 
  setInput, 
  handleSubmit, 
  isLoading,
  selectedModel,
  setSelectedModel 
}) {
  const textareaRef = useRef(null);

  // Function to adjust textarea height
  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      // Reset height to auto to get the correct scrollHeight
      textarea.style.height = 'auto';
      // Set new height based on scrollHeight
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }
  };

  // Adjust height on input change
  useEffect(() => {
    adjustHeight();
  }, [input]);

  // Handle input change
  const handleChange = (e) => {
    setInput(e.target.value);
  };

  // Handle keyboard shortcuts
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const getPlaceholder = () => {
    return selectedModel === 'encyclopedia' 
      ? "Ask about ski techniques, equipment, or general knowledge..."
      : "Ask questions about ski maps and trails...";
  };

  return (
    <div className="w-full">
      <ModelToggle 
        selectedModel={selectedModel} 
        setSelectedModel={setSelectedModel}
      />
      <form onSubmit={handleSubmit} className="flex gap-2 w-full">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={getPlaceholder()}
          rows={1}
          className="flex-1 p-2.5 text-sm border border-[#e2e8f0] rounded-md focus:outline-none focus:ring-1 focus:ring-[#3182ce] focus:border-transparent bg-[#f8fafc] placeholder-[#94a3b8] resize-none overflow-y-auto min-h-[40px] max-h-[200px]"
          style={{
            lineHeight: '1.5',
          }}
        />
        <button
          type="submit"
          disabled={isLoading}
          className="bg-gradient-to-r from-[#2c5282] to-[#4299e1] text-white px-4 self-end h-[40px] rounded-md hover:opacity-90 disabled:opacity-50 transition-all text-sm flex items-center"
        >
          Send
        </button>
      </form>
    </div>
  );
} 