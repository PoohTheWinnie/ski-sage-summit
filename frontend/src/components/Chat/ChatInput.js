import { useRef } from 'react';
import ModelToggle from './ModelToggle';
import { MountainSnow } from 'lucide-react';

export default function ChatInput({ 
  input, 
  setInput, 
  handleSubmit, 
  isLoading,
  selectedModel,
  setSelectedModel
}) {
  const textareaRef = useRef(null);

  const handleChange = (e) => {
    setInput(e.target.value);
    // Adjust height
    e.target.style.height = 'auto';
    e.target.style.height = `${e.target.scrollHeight}px`;
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full">
      <div className="relative flex flex-col rounded-2xl border border-gray-200 bg-white shadow-sm">
        {/* Textarea */}
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="How can I help you today?"
          className="w-full mx-2 my-3 resize-none bg-transparent text-gray-700 outline-none"
          style={{
            minHeight: '72px' // 3 lines at roughly 24px per line
          }}
        />

        {/* Controls Row */}
        <div className="flex items-center justify-between px-4 py-2">
          <ModelToggle 
            selectedModel={selectedModel}
            setSelectedModel={setSelectedModel}
          />
          <button className="p-1 hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-center" onClick={handleSubmit}>
            <MountainSnow />
          </button>
        </div>
      </div>
    </div>
  );
} 