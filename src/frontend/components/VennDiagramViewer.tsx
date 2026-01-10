/**
 * Venn Diagram Viewer Component
 * Displays 2-set and 3-set Venn diagrams with interactive features
 */

import React, { useState } from 'react';
import { useDiagramContent } from '../hooks/usePhase3Diagrams';

interface VennDiagramViewerProps {
  diagramId?: string;
  svgContent?: string;
  title?: string;
  className?: string;
  showControls?: boolean;
}

export const VennDiagramViewer: React.FC<VennDiagramViewerProps> = ({
  diagramId,
  svgContent: providedSvg,
  title,
  className = '',
  showControls = true
}) => {
  const { content, loading, error } = useDiagramContent(diagramId);
  const [zoom, setZoom] = useState(1);

  // Use provided SVG or fetched content
  const svgContent = providedSvg || content?.svg;
  const displayTitle = title || content?.title || 'Venn Diagram';

  if (loading) {
    return (
      <div className={`venn-diagram-viewer loading ${className}`}>
        <div className="spinner">Loading diagram...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`venn-diagram-viewer error ${className}`}>
        <p className="error-message">Failed to load diagram: {error.message}</p>
      </div>
    );
  }

  if (!svgContent) {
    return (
      <div className={`venn-diagram-viewer empty ${className}`}>
        <p>No Venn diagram available</p>
      </div>
    );
  }

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.2, 0.5));
  const handleReset = () => setZoom(1);

  return (
    <div className={`venn-diagram-viewer ${className}`}>
      <div className="diagram-header">
        <h3 className="diagram-title">{displayTitle}</h3>
        {showControls && (
          <div className="diagram-controls">
            <button onClick={handleZoomOut} aria-label="Zoom out">−</button>
            <button onClick={handleReset} aria-label="Reset zoom">Reset</button>
            <button onClick={handleZoomIn} aria-label="Zoom in">+</button>
          </div>
        )}
      </div>
      <div 
        className="diagram-content"
        style={{ transform: `scale(${zoom})`, transformOrigin: 'center top' }}
        dangerouslySetInnerHTML={{ __html: svgContent }}
      />
      <style jsx>{`
        .venn-diagram-viewer {
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 16px;
          background: white;
          margin: 16px 0;
        }
        .diagram-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid #e0e0e0;
        }
        .diagram-title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
          color: #333;
        }
        .diagram-controls {
          display: flex;
          gap: 8px;
        }
        .diagram-controls button {
          padding: 6px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          background: white;
          cursor: pointer;
          font-size: 14px;
          transition: all 0.2s;
        }
        .diagram-controls button:hover {
          background: #f5f5f5;
          border-color: #999;
        }
        .diagram-content {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 300px;
          overflow: auto;
          transition: transform 0.3s ease;
        }
        .loading, .error, .empty {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
          color: #666;
        }
        .error-message {
          color: #d32f2f;
        }
      `}</style>
    </div>
  );
};

export default VennDiagramViewer;
