import React from 'react';

const LoadingMessage = ({ variant = 'default', lines = 2 }) => {
  const variants = {
    default: 'bg-gray-200',
    dark: 'bg-gray-300',
    primary: 'bg-blue-200',
  };

  const bgColor = variants[variant];

  return (
    <div className="w-full max-w-2xl rounded-lg p-4 bg-white/50 backdrop-blur-sm">
      <div className="flex animate-pulse space-x-4">
        {/* Avatar placeholder with subtle shadow */}
        <div className={`size-10 rounded-full ${bgColor} shadow-sm`}></div>
        
        <div className="flex-1 space-y-4 py-1">
          {/* Header line */}
          <div className={`h-2.5 rounded-full ${bgColor} w-1/4`}></div>
          
          {/* Message body */}
          <div className="space-y-3">
            {Array(lines).fill(0).map((_, i) => (
              <div key={i} className="flex flex-col space-y-2">
                <div className={`h-2 rounded-full ${bgColor} w-${Math.random() > 0.5 ? 'full' : '3/4'}`}></div>
              </div>
            ))}
          </div>
          
          {/* Footer elements */}
          <div className="flex space-x-4 pt-2">
            <div className={`h-2 rounded-full ${bgColor} w-16`}></div>
            <div className={`h-2 rounded-full ${bgColor} w-12`}></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingMessage; 