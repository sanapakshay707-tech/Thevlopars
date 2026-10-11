import React, { useState } from 'react';
import { FileSpreadsheet, Copy, Check, Sparkles } from 'lucide-react';

export default function SummaryCard({ summary }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!summary) return;
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <Sparkles size={18} color="#b45309" />
          Executive Summary & Reasoning
        </h2>
        {summary && (
          <button
            onClick={handleCopy}
            className="sample-btn"
            title="Copy summary to clipboard"
          >
            {copied ? <Check size={13} color="#059669" /> : <Copy size={13} />}
            {copied ? 'Copied!' : 'Copy Summary'}
          </button>
        )}
      </div>
      <div className="card-body">
        {summary ? (
          <div className="summary-text">
            {summary}
          </div>
        ) : (
          <div style={{ color: '#94a3b8', fontStyle: 'italic', fontSize: '0.875rem' }}>
            No summary generated yet. Upload a document to analyze.
          </div>
        )}
      </div>
    </div>
  );
}
