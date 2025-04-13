import React from 'react';

export default function UserMessage({ message }) {
  return (
    <div className="flex flex-col justify-end items-end ml-auto max-w-[82%]">
      <div className="px-4 py-3 rounded-lg shadow-lg" style={{ backgroundColor: '#1B3B4B' }}>
        <p className="font-medium whitespace-pre-line" style={{ color: '#E6EEF2' }}>
          {message.content}
        </p>
      </div>
    </div>
  );
}