/**
 * ASCII Diagram Renderer Component
 * Renders ASCII art diagrams with syntax highlighting and styling
 */

import React, { useState, useEffect } from 'react';

interface ASCIIDiagramProps {
  content: string;
  title?: string;
  className?: string;
}

const ASCIIDiagram: React.FC<ASCIIDiagramProps> = ({ content, title, className = '' }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`ascii-diagram-container ${className}`}>
      {title && <h3 className="ascii-diagram-title">{title}</h3>}
      
      <div className="ascii-diagram-wrapper">
        <pre className="ascii-diagram-content">
          <code>{content}</code>
        </pre>
        
        <button 
          onClick={handleCopy}
          className="ascii-diagram-copy-btn"
          title="Copy diagram"
        >
          {copied ? '✓ Copied' : '📋 Copy'}
        </button>
      </div>

      <style jsx>{`
        .ascii-diagram-container {
          margin: 20px 0;
          border-radius: 8px;
          overflow: hidden;
          background: #f5f5f5;
          border: 1px solid #e0e0e0;
        }

        .ascii-diagram-title {
          margin: 0;
          padding: 12px 16px;
          background: #2c3e50;
          color: white;
          font-size: 14px;
          font-weight: 600;
          border-bottom: 1px solid #34495e;
        }

        .ascii-diagram-wrapper {
          position: relative;
          padding: 16px;
          background: #ffffff;
          overflow-x: auto;
        }

        .ascii-diagram-content {
          margin: 0;
          padding: 12px;
          background: #f8f8f8;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-family: 'Courier New', monospace;
          font-size: 13px;
          line-height: 1.5;
          color: #333;
          overflow-x: auto;
          max-height: 400px;
          overflow-y: auto;
        }

        .ascii-diagram-content code {
          font-family: inherit;
          color: inherit;
        }

        .ascii-diagram-copy-btn {
          position: absolute;
          top: 8px;
          right: 8px;
          padding: 6px 12px;
          background: #3498db;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 12px;
          cursor: pointer;
          transition: background 0.3s ease;
          z-index: 10;
        }

        .ascii-diagram-copy-btn:hover {
          background: #2980b9;
        }

        .ascii-diagram-copy-btn:active {
          transform: scale(0.98);
        }

        /* Responsive */
        @media (max-width: 768px) {
          .ascii-diagram-wrapper {
            padding: 12px;
          }

          .ascii-diagram-content {
            font-size: 12px;
          }

          .ascii-diagram-copy-btn {
            padding: 4px 8px;
            font-size: 11px;
          }
        }
      `}</style>
    </div>
  );
};

export default ASCIIDiagram;
