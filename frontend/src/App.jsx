import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import FileUpload from './components/FileUpload';
import AnalysisViewer from './components/AnalysisViewer';
import SummaryCard from './components/SummaryCard';
import EvidenceViewer from './components/EvidenceViewer';
import DocumentPreview from './components/DocumentPreview';
import { AlertTriangle, ShieldCheck, Loader2 } from 'lucide-react';

export default function App() {
  const [healthData, setHealthData] = useState(null);
  const [isCheckingHealth, setIsCheckingHealth] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [pdfBlobUrl, setPdfBlobUrl] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [selectedEvidence, setSelectedEvidence] = useState(null);

  // Health check polling
  useEffect(() => {
    const fetchHealth = async () => {
      setIsCheckingHealth(true);
      try {
        const res = await fetch('/api/health');
        const data = await res.json();
        setHealthData(data);
      } catch (err) {
        console.warn('Backend health check error:', err);
        setHealthData(null);
      } finally {
        setIsCheckingHealth(false);
      }
    };

    fetchHealth();
    const interval = setInterval(fetchHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  // Analyze file
  const analyzeFile = async (file) => {
    setSelectedFile(file);
    setErrorMessage(null);
    setAnalysis(null);
    setSelectedEvidence(null);

    // Create preview blob URL
    const blobUrl = URL.createObjectURL(file);
    setPdfBlobUrl(blobUrl);

    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || data.error || `HTTP ${response.status} error`);
      }

      setAnalysis(data);
      if (data.evidence && data.evidence.length > 0) {
        setSelectedEvidence(data.evidence[0]);
      }
    } catch (err) {
      console.error('Analysis failed:', err);
      setErrorMessage(err.message || 'An error occurred while analyzing the document.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  // 1-Click QA Sample Selector
  const handleSampleSelect = async (sampleName) => {
    setErrorMessage(null);
    setIsAnalyzing(true);
    try {
      const res = await fetch(`/api/sample/${sampleName}`);
      if (!res.ok) {
        throw new Error(`Failed to load sample ${sampleName}`);
      }
      const blob = await res.blob();
      const file = new File([blob], sampleName, { type: 'application/pdf' });
      await analyzeFile(file);
    } catch (err) {
      console.error('Error loading sample:', err);
      setErrorMessage(`Failed to load sample ${sampleName}: ${err.message}`);
      setIsAnalyzing(false);
    }
  };

  const handleSelectEvidenceByField = (field) => {
    if (!analysis || !analysis.evidence) return;
    const match = analysis.evidence.find(
      (e) => (e.field || '').toLowerCase() === field.toLowerCase()
    );
    if (match) {
      setSelectedEvidence(match);
    }
  };

  return (
    <div className="app-container">
      <Navbar healthData={healthData} isCheckingHealth={isCheckingHealth} />

      <main className="main-content">
        {/* Offline Privacy Guarantee Banner */}
        <div className="privacy-banner">
          <div className="info">
            <ShieldCheck size={20} color="#60a5fa" />
            <div>
              <strong>100% Offline Legal Privacy Guaranteed:</strong> All PDF parsing and AI inference occurs strictly on this local machine via Ollama (<code>qwen2.5:1.5b</code>). Zero data leaves your computer.
            </div>
          </div>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
            FastAPI + PyMuPDF + Ollama
          </span>
        </div>

        {/* Error Banner */}
        {errorMessage && (
          <div className="error-banner">
            <AlertTriangle size={20} style={{ flexShrink: 0 }} />
            <div>
              <strong>Document Analysis Error:</strong> {errorMessage}
            </div>
          </div>
        )}

        {/* Main Dashboard Layout */}
        <div className="dashboard-grid">
          {/* Left Column: Input and Intelligence Extraction */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <FileUpload
              onFileSelect={analyzeFile}
              onSampleSelect={handleSampleSelect}
              isAnalyzing={isAnalyzing}
              selectedFileName={selectedFile ? selectedFile.name : null}
            />

            {isAnalyzing && (
              <div className="card" style={{ padding: '2.5rem', textAlign: 'center' }}>
                <div className="spinner"></div>
                <h3 style={{ marginTop: '1rem', fontSize: '1rem', fontWeight: 600, color: '#1e293b' }}>
                  Analyzing Judgment with Ollama (qwen2.5:1.5b)...
                </h3>
                <p style={{ fontSize: '0.825rem', color: '#64748b', marginTop: '0.35rem' }}>
                  Extracting parties, cross-referencing statutory provisions, and validating textual evidence.
                </p>
              </div>
            )}

            {analysis && (
              <>
                <AnalysisViewer
                  analysis={analysis}
                  onSelectEvidenceByField={handleSelectEvidenceByField}
                />

                <SummaryCard
                  summary={analysis.summary}
                  advocateSummary={analysis.advocateSummary}
                />

                <EvidenceViewer
                  evidence={analysis.evidence}
                  selectedEvidence={selectedEvidence}
                  onSelectEvidence={setSelectedEvidence}
                />
              </>
            )}
          </div>

          {/* Right Column: PDF Document Evidence Viewer */}
          <div style={{ position: 'sticky', top: '5.5rem' }}>
            <DocumentPreview
              pdfBlobUrl={pdfBlobUrl}
              selectedEvidence={selectedEvidence}
              documentName={selectedFile ? selectedFile.name : ''}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
