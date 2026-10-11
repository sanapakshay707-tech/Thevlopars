import React from 'react';
import { Search, Quote, ExternalLink, Bookmark } from 'lucide-react';

export default function EvidenceViewer({ evidence = [], selectedEvidence, onSelectEvidence }) {
  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <Bookmark size={18} color="#2563eb" />
          Clickable Evidence References ({evidence.length})
        </h2>
        <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
          Exact Source Citations
        </span>
      </div>

      <div className="card-body">
        {evidence.length === 0 ? (
          <div style={{ color: '#94a3b8', fontStyle: 'italic', fontSize: '0.85rem' }}>
            No evidence citations loaded yet.
          </div>
        ) : (
          <div className="evidence-list">
            {evidence.map((item, idx) => {
              const isSelected = selectedEvidence === item;
              return (
                <div
                  key={idx}
                  className={`evidence-card ${isSelected ? 'selected' : ''}`}
                  onClick={() => onSelectEvidence(item)}
                >
                  <div className="evidence-header">
                    <span className="evidence-page-pill">Page {item.page}</span>
                    <span className="evidence-field-tag">
                      {item.field.toUpperCase()}
                    </span>
                  </div>
                  <div className="evidence-quote">
                    "{item.text}"
                  </div>
                  <div style={{ marginTop: '0.4rem', fontSize: '0.7rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                    <ExternalLink size={11} /> Click to highlight in PDF viewer
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
