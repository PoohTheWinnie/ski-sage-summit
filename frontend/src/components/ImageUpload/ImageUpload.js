'use client';
import { useState } from 'react';

export default function ImageUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setUploadStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify({
      name: file.name,
      type: 'ski_map',
      upload_date: new Date().toISOString()
    }));

    try {
      const response = await fetch('/api/upload-map', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setUploadStatus('Upload successful!');
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Upload failed.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-white shadow-sm">
      <h2 className="text-lg font-medium mb-4">Upload Ski Map</h2>
      <div className="space-y-4">
        <input
          type="file"
          accept="image/*"
          onChange={handleUpload}
          disabled={isUploading}
          className="block w-full text-sm text-slate-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-violet-50 file:text-violet-700
            hover:file:bg-violet-100"
        />
        {uploadStatus && (
          <p className={`text-sm ${
            uploadStatus.includes('failed') ? 'text-red-500' : 'text-green-500'
          }`}>
            {uploadStatus}
          </p>
        )}
      </div>
    </div>
  );
} 