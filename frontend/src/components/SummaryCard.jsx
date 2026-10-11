import React, { useState } from 'react';
import { FileSpreadsheet, Copy, Check, Sparkles } from 'lucide-react';

export default function SummaryCard({ summary, advocateSummary }) {
  const [copied, setCopied] = useState(false);
  const [audience, setAudience] = useState('general');
  const activeSummary = audience === 'general' ? summary : advocateSummary;

  const handleCopy = () => {
    if (!activeSummary) return;
    navigator.clipboard.writeText(activeSummary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <Sparkles size={18} color="#b45309" />
          Case Summary
        </h2>
        {activeSummary && (
          <button
            onClick={handleCopy}
            className="sample-btn"
            title="Copy selected summary"
          >
            {copied ? <Check size={13} color="#059669" /> : <Copy size={13} />}
            {copied ? 'Copied!' : 'Copy Summary'}
          </button>
        )}
      </div>
      <div className="card-body">
        <div className="summary-audience-switch" role="tablist" aria-label="Summary audience">
          <button
            id="summary-tab-general"
            className={`summary-audience-tab ${audience === 'general' ? 'active' : ''}`}
            type="button"
            role="tab"
            aria-selected={audience === 'general'}
            aria-controls="summary-panel"
            onClick={() => setAudience('general')}
          >
            General reader
          </button>
          <button
            id="summary-tab-advocate"
            className={`summary-audience-tab ${audience === 'advocate' ? 'active' : ''}`}
            type="button"
            role="tab"
            aria-selected={audience === 'advocate'}
            aria-controls="summary-panel"
            onClick={() => setAudience('advocate')}
          >
            Junior advocate
          </button>
        </div>
        {activeSummary ? (
          <div
            id="summary-panel"
            className="summary-text"
            role="tabpanel"
            aria-labelledby={audience === 'general' ? 'summary-tab-general' : 'summary-tab-advocate'}
          >
            {activeSummary}
          </div>
        ) : (
          <div style={{ color: '#94a3b8', fontStyle: 'italic', fontSize: '0.875rem' }}>
            No {audience === 'general' ? 'general-reader' : 'junior-advocate'} summary is available.
          </div>
        )}
      </div>
    </div>
  );
}
