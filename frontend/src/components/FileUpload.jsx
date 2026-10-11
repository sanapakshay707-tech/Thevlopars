import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, Sparkles, FileWarning } from 'lucide-react';

export default function FileUpload({ onFileSelect, onSampleSelect, isAnalyzing, selectedFileName }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      onFileSelect(file);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <UploadCloud size={18} color="#2563eb" />
          Ingest Court Judgment
        </h2>
        {selectedFileName && (
          <span style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 500 }}>
            Active: <strong>{selectedFileName}</strong>
          </span>
        )}
      </div>

      <div className="card-body">
        <div
          className={`dropzone ${isDragging ? 'active' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !isAnalyzing && fileInputRef.current.click()}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".pdf,application/pdf"
            style={{ display: 'none' }}
            disabled={isAnalyzing}
          />
          <div className="dropzone-icon">
            <FileText size={28} />
          </div>
          <div className="dropzone-title">
            {isAnalyzing
              ? 'Analyzing Legal Document...'
              : 'Drop Judgment PDF Here or Click to Browse'}
          </div>
          <div className="dropzone-sub">
            Supports digital & scanned court judgments (Civil, Criminal, Supreme Court, High Court)
          </div>
        </div>

        {/* 1-Click Sample QA Judgments */}
        <div className="sample-bar">
          <span className="sample-bar-label">
            <Sparkles size={12} style={{ display: 'inline', marginRight: '3px' }} />
            Demo / QA Cases:
          </span>

          <button
            type="button"
            className="sample-btn"
            disabled={isAnalyzing}
            onClick={() => onSampleSelect('civil_judgment.pdf')}
          >
            Civil Judgment
          </button>

          <button
            type="button"
            className="sample-btn"
            disabled={isAnalyzing}
            onClick={() => onSampleSelect('criminal_judgment.pdf')}
          >
            Criminal Judgment
          </button>

          <button
            type="button"
            className="sample-btn"
            disabled={isAnalyzing}
            onClick={() => onSampleSelect('interim_order.pdf')}
          >
            Interim Order (No Final Outcome)
          </button>

          <button
            type="button"
            className="sample-btn"
            style={{ borderColor: '#fca5a5', color: '#991b1b', background: '#fef2f2' }}
            disabled={isAnalyzing}
            onClick={() => onSampleSelect('corrupted_document.pdf')}
          >
            <FileWarning size={12} />
            Corrupted PDF Test
          </button>
        </div>
      </div>
    </div>
  );
}
