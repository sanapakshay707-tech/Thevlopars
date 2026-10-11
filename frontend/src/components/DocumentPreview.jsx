import React from 'react';
import { Eye, FileText, CornerDownRight, Sparkles, ExternalLink } from 'lucide-react';

export default function DocumentPreview({ pdfBlobUrl, selectedEvidence, documentName }) {
  if (!pdfBlobUrl) {
    return (
      <div className="card">
        <div className="card-header">
          <h2>
            <Eye size={18} color="#64748b" />
            PDF Evidence Viewer
          </h2>
        </div>
        <div className="card-body">
          <div className="empty-preview">
            <FileText size={48} strokeWidth={1.5} />
            <p style={{ fontWeight: 500 }}>No Document Active</p>
            <span style={{ fontSize: '0.8rem' }}>
              Upload a court judgment or click a QA case to preview side-by-side with AI extractions.
            </span>
          </div>
        </div>
      </div>
    );
  }

  const activePage = selectedEvidence ? selectedEvidence.page : 1;
  const viewerUrl = `${pdfBlobUrl}#page=${activePage}&view=FitH`;

  return (
    <div className="card">
      <div className="card-header">
        <h2>
          <Eye size={18} color="#2563eb" />
          Interactive PDF Evidence Viewer
        </h2>
        <span style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>
          {documentName || 'Document.pdf'}
        </span>
      </div>

      <div className="card-body" style={{ padding: '0.75rem' }}>
        {/* Evidence Highlight Spotlight Bar */}
        {selectedEvidence && (
          <div
            style={{
              background: '#fef08a',
              border: '1px solid #facc15',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
              marginBottom: '0.75rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.35rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: '#854d0e', display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                <Sparkles size={13} /> Evidence Spotlight: {selectedEvidence.field.toUpperCase()} (Page {selectedEvidence.page})
              </span>
              <a
                href={viewerUrl}
                target="_blank"
                rel="noreferrer"
                style={{ fontSize: '0.7rem', color: '#854d0e', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.2rem' }}
              >
                Open in tab <ExternalLink size={10} />
              </a>
            </div>
            <div style={{ fontSize: '0.825rem', color: '#713f12', fontStyle: 'italic', lineHeight: 1.4 }}>
              "{selectedEvidence.text}"
            </div>
          </div>
        )}

        {/* Embedded native PDF iframe */}
        <div className="pdf-viewer-container">
          <div className="pdf-viewer-header">
            <span>Viewing: {documentName}</span>
            <span>Target: Page {activePage}</span>
          </div>
          <iframe
            key={`${pdfBlobUrl}-${activePage}`}
            src={viewerUrl}
            title="Court Judgment PDF Preview"
            className="pdf-iframe"
          />
        </div>
      </div>
    </div>
  );
}
