/**
 * Chemistry Diagram Viewer Component
 * Displays molecular structures and chemical reactions
 */

import React, { useState } from 'react';
import { useDiagramContent } from '../hooks/usePhase3Diagrams';

interface ChemistryViewerProps {
  diagramId?: string;
  svgContent?: string;
  title?: string;
  chemistryType?: 'molecular' | 'reaction';
  className?: string;
  showControls?: boolean;
}

export const ChemistryViewer: React.FC<ChemistryViewerProps> = ({
  diagramId,
  svgContent: providedSvg,
  title,
  chemistryType = 'reaction',
  className = '',
  showControls = true
}) => {
  const { content, loading, error } = useDiagramContent(diagramId);
  const [zoom, setZoom] = useState(1);
  const [highlightBonds, setHighlightBonds] = useState(false);

  const svgContent = providedSvg || content?.svg;
  const displayTitle = title || content?.title || `${chemistryType === 'molecular' ? 'Molecular Structure' : 'Chemical Reaction'}`;

  if (loading) {
    return <div className={`chemistry-viewer loading ${className}`}>Loading chemistry diagram...</div>;
  }

  if (error) {
    return <div className={`chemistry-viewer error ${className}`}>Error: {error.message}</div>;
  }

  if (!svgContent) {
    return <div className={`chemistry-viewer empty ${className}`}>No chemistry diagram available</div>;
  }

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.2, 0.5));
  const handleReset = () => setZoom(1);

  return (
    <div className={`chemistry-viewer chemistry-${chemistryType} ${className}`}>
      <div className="chemistry-header">
        <div className="header-left">
          <h3 className="chemistry-title">{displayTitle}</h3>
          <span className={`chemistry-badge ${chemistryType}`}>
            {chemistryType === 'molecular' ? '🧬 Molecular' : '⚗️ Reaction'}
          </span>
        </div>
        {showControls && (
          <div className="chemistry-controls">
            {chemistryType === 'molecular' && (
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={highlightBonds}
                  onChange={() => setHighlightBonds(!highlightBonds)}
                />
                Highlight Bonds
              </label>
            )}
            <button onClick={handleZoomOut}>−</button>
            <button onClick={handleReset}>Reset</button>
            <button onClick={handleZoomIn}>+</button>
          </div>
        )}
      </div>
      <div className="chemistry-container">
        <div
          className={`chemistry-content ${highlightBonds ? 'highlight-bonds' : ''}`}
          style={{ transform: `scale(${zoom})` }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      </div>
      <div className="chemistry-info">
        <p className="info-text">
          {chemistryType === 'molecular' 
            ? 'Molecular structure showing atom bonds and spatial arrangement'
            : 'Chemical reaction showing reactants, products, and reaction conditions'}
        </p>
      </div>
      <style jsx>{`
        .chemistry-viewer {
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 16px;
          background: white;
          margin: 16px 0;
        }
        .chemistry-molecular {
          border-color: #4caf50;
        }
        .chemistry-reaction {
          border-color: #f44336;
        }
        .chemistry-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 2px solid #e0e0e0;
        }
        .header-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .chemistry-title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
          color: #333;
        }
        .chemistry-badge {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
          text-transform: uppercase;
        }
        .chemistry-badge.molecular {
          background: #e8f5e9;
          color: #2e7d32;
          border: 1px solid #81c784;
        }
        .chemistry-badge.reaction {
          background: #ffebee;
          color: #c62828;
          border: 1px solid #e57373;
        }
        .chemistry-controls {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .toggle-label {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 14px;
          color: #666;
          margin-right: 8px;
        }
        .chemistry-controls button {
          padding: 6px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          background: white;
          cursor: pointer;
          transition: all 0.2s;
        }
        .chemistry-controls button:hover {
          background: #f5f5f5;
          border-color: #999;
        }
        .chemistry-container {
          overflow: auto;
          min-height: 250px;
          background: #fafafa;
          border: 1px solid #e0e0e0;
          border-radius: 4px;
          padding: 20px;
          margin-bottom: 12px;
        }
        .chemistry-content {
          display: flex;
          justify-content: center;
          align-items: center;
          transition: transform 0.3s ease;
        }
        .chemistry-content.highlight-bonds line,
        .chemistry-content.highlight-bonds path {
          stroke-width: 3;
          stroke: #ff5722;
        }
        .chemistry-info {
          padding: 12px;
          background: #f5f5f5;
          border-radius: 4px;
        }
        .info-text {
          margin: 0;
          font-size: 13px;
          color: #666;
          line-height: 1.5;
        }
        .loading, .error, .empty {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
          color: #666;
        }
      `}</style>
    </div>
  );
};

export default ChemistryViewer;
