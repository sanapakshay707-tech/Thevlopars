import React, { useState, useEffect } from 'react';
import { Scale, Cpu, ShieldCheck, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function Navbar({ healthData, isCheckingHealth }) {
  const isReady = healthData && healthData.ready;
  const modelName = healthData?.model || 'qwen2.5:1.5b';

  return (
    <header className="navbar">
      <div className="navbar-brand">
        <div className="brand-icon">
          <Scale size={24} />
        </div>
        <div className="brand-text">
          <h1>CourtLens</h1>
          <span>AI-Powered Legal Document Analyzer</span>
        </div>
      </div>

      <div className="nav-actions">
        <div className="privacy-tag" title="Local-only execution ensures full attorney-client confidentiality">
          <ShieldCheck size={14} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} />
          Local AI Inference (Offline)
        </div>

        <div className={`health-badge ${isReady ? 'ready' : healthData ? 'degraded' : 'offline'}`}>
          <span className="pulse-dot"></span>
          <Cpu size={14} />
          <span>
            {isReady
              ? `Model: ${modelName} (Ready)`
              : healthData
              ? `Model Degraded: ${modelName}`
              : 'Connecting to Ollama...'}
          </span>
        </div>
      </div>
    </header>
  );
}
