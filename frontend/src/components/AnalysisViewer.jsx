import React from 'react';
import { Briefcase, Users, BookOpen, HelpCircle, CheckCircle, Clock, FileCheck } from 'lucide-react';

export default function AnalysisViewer({ analysis, onSelectEvidenceByField }) {
  if (!analysis) return null;

  const {
    caseType,
    parties,
    legalProvisions = [],
    issues = [],
    outcome,
    pageCount,
    processingTimeMs,
  } = analysis;

  const getBadgeClass = (type) => {
    const t = (type || '').toLowerCase();
    if (t.includes('civil')) return 'badge-civil';
    if (t.includes('crim')) return 'badge-criminal';
    if (t.includes('const')) return 'badge-constitutional';
    return 'badge-default';
  };

  const isInterim =
    (outcome || '').toLowerCase().includes('interim') ||
    (outcome || '').toLowerCase().includes('n/a') ||
    (outcome || '').toLowerCase().includes('no final') ||
    (outcome || '').toLowerCase().includes('stay');

  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <Briefcase size={18} color="#1e3a8a" />
          Structured Case Intelligence
        </h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {pageCount > 0 && (
            <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
              <FileCheck size={13} style={{ display: 'inline', verticalAlign: '-1px' }} /> {pageCount} pages
            </span>
          )}
          {processingTimeMs > 0 && (
            <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
              <Clock size={13} style={{ display: 'inline', verticalAlign: '-1px' }} /> {(processingTimeMs / 1000).toFixed(1)}s
            </span>
          )}
        </div>
      </div>

      <div className="card-body">
        {/* Case Type */}
        <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase' }}>
            Case Classification:
          </span>
          <span className={`case-badge ${getBadgeClass(caseType)}`}>
            {caseType || 'Unclassified'}
          </span>
        </div>

        {/* Litigant Parties */}
        <div>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <Users size={14} /> Litigant Parties:
          </span>
          <div
            className="parties-box"
            onClick={() => onSelectEvidenceByField('parties')}
            title="Click to view parties citation evidence"
            style={{ cursor: 'pointer' }}
          >
            <div className="party-item">
              <span className="party-role">Petitioner / Appellant</span>
              <span className="party-name">{parties?.petitioner || 'N/A'}</span>
            </div>
            <div className="vs-badge">VS</div>
            <div className="party-item" style={{ textAlign: 'right' }}>
              <span className="party-role">Respondent / Defendant</span>
              <span className="party-name">{parties?.respondent || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Legal Provisions */}
        <div style={{ marginTop: '1.25rem' }}>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            <BookOpen size={14} /> Cited Legal Provisions & Statutes:
          </span>
          <div className="provisions-container">
            {legalProvisions.length > 0 ? (
              legalProvisions.map((prov, idx) => (
                <span
                  key={idx}
                  className="provision-chip"
                  onClick={() => onSelectEvidenceByField('provisions')}
                  title="Click to locate provision in PDF evidence"
                >
                  {prov}
                </span>
              ))
            ) : (
              <span style={{ fontSize: '0.85rem', color: '#94a3b8', fontStyle: 'italic' }}>
                No explicit statute sections extracted.
              </span>
            )}
          </div>
        </div>

        {/* Legal Issues */}
        {issues.length > 0 && (
          <div style={{ marginTop: '1.25rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
              <HelpCircle size={14} /> Key Legal Issues Framed:
            </span>
            <ul style={{ marginTop: '0.5rem', paddingLeft: '1.25rem', fontSize: '0.875rem', color: '#334155' }}>
              {issues.map((issue, idx) => (
                <li key={idx} style={{ marginBottom: '0.35rem' }}>
                  {issue}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Case Outcome */}
        <div
          className={`outcome-box ${isInterim ? 'interim' : ''}`}
          onClick={() => onSelectEvidenceByField('outcome')}
          title="Click to view outcome citation evidence"
          style={{ cursor: 'pointer' }}
        >
          <div className="outcome-title">
            <CheckCircle size={14} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} />
            {isInterim ? 'Interim Order / Status (No Final Outcome)' : 'Final Outcome & Judgment Ruling'}
          </div>
          <div className="outcome-text">
            {outcome || 'No outcome recorded.'}
          </div>
        </div>
      </div>
    </div>
  );
}
