import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Eye, FileText, CornerDownRight, Sparkles, ExternalLink } from 'lucide-react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

function findEvidenceRanges(textItems, evidenceText) {
  if (!textItems?.length || !evidenceText) return {};

  const query = evidenceText
    .replace(/^(?:\.\.\.|…)\s*/, '')
    .replace(/\s*(?:\.\.\.|…)+$/, '')
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .trim();
  if (!query) return {};

  let pageText = '';
  const positions = [];
  textItems.forEach((item, itemIndex) => {
    const itemText = item.str || '';
    for (let charIndex = 0; charIndex < itemText.length; charIndex += 1) {
      const char = itemText[charIndex];
      if (/\s/.test(char)) {
        if (pageText && !pageText.endsWith(' ')) {
          pageText += ' ';
          positions.push({ itemIndex, charIndex });
        }
      } else {
        pageText += char.toLowerCase();
        positions.push({ itemIndex, charIndex });
      }
    }
    if (pageText && !pageText.endsWith(' ')) {
      pageText += ' ';
      positions.push({ itemIndex, charIndex: itemText.length });
    }
  });

  const matchStart = pageText.trimEnd().indexOf(query);
  if (matchStart === -1) return {};

  const ranges = {};
  for (const { itemIndex, charIndex } of positions.slice(matchStart, matchStart + query.length)) {
    if (charIndex >= textItems[itemIndex].str.length) continue;
    const range = ranges[itemIndex] || { start: charIndex, end: charIndex + 1 };
    range.start = Math.min(range.start, charIndex);
    range.end = Math.max(range.end, charIndex + 1);
    ranges[itemIndex] = range;
  }
  return ranges;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[char]);
}

function renderTextItem(text, range) {
  if (!range) return escapeHtml(text);
  return `${escapeHtml(text.slice(0, range.start))}<mark class="pdf-evidence-highlight">${escapeHtml(text.slice(range.start, range.end))}</mark>${escapeHtml(text.slice(range.end))}`;
}

export default function DocumentPreview({ pdfBlobUrl, selectedEvidence, documentName }) {
  const pageContainerRef = useRef(null);
  const [pageWidth, setPageWidth] = useState(0);
  const [textItems, setTextItems] = useState(null);

  const activePage = selectedEvidence ? selectedEvidence.page : 1;
  const highlightRanges = useMemo(
    () => findEvidenceRanges(textItems, selectedEvidence?.text),
    [textItems, selectedEvidence?.text],
  );
  const handleTextSuccess = useCallback(({ items }) => setTextItems(items), []);
  const customTextRenderer = useCallback(
    ({ str, itemIndex }) => renderTextItem(str, highlightRanges[itemIndex]),
    [highlightRanges],
  );

  useEffect(() => {
    const container = pageContainerRef.current;
    if (!container) return undefined;

    const observer = new ResizeObserver(([entry]) => {
      setPageWidth(Math.floor(entry.contentRect.width));
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, [pdfBlobUrl]);

  useEffect(() => {
    setTextItems(null);
    if (pageContainerRef.current) pageContainerRef.current.scrollTop = 0;
  }, [pdfBlobUrl, activePage]);

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
          <div className="pdf-page-scroll" ref={pageContainerRef}>
            <Document
              file={pdfBlobUrl}
              loading={<span className="pdf-page-status">Loading PDF…</span>}
              error={<span className="pdf-page-status">Unable to render this PDF.</span>}
            >
              {pageWidth > 0 && (
                <Page
                  key={`${pdfBlobUrl}-${activePage}`}
                  pageNumber={activePage}
                  width={Math.min(pageWidth - 24, 760)}
                  onGetTextSuccess={handleTextSuccess}
                  customTextRenderer={customTextRenderer}
                  renderAnnotationLayer={false}
                />
              )}
            </Document>
          </div>
        </div>
      </div>
    </div>
  );
}
