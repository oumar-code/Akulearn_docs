/**
 * Circuit Diagram Viewer Component
 * Displays electrical and logic circuit diagrams
 */

import React, { useState } from 'react';
import { useDiagramContent } from '../hooks/usePhase3Diagrams';

interface CircuitViewerProps {
  diagramId?: string;
  svgContent?: string;
  title?: string;
  circuitType?: 'electrical' | 'logic';
  className?: string;
  showControls?: boolean;
}

export const CircuitViewer: React.FC<CircuitViewerProps> = ({
  diagramId,
  svgContent: providedSvg,
  title,
  circuitType = 'electrical',
  className = '',
  showControls = true
}) => {
  const { content, loading, error } = useDiagramContent(diagramId);
  const [zoom, setZoom] = useState(1);
  const [showLabels, setShowLabels] = useState(true);

  const svgContent = providedSvg || content?.svg;
  const displayTitle = title || content?.title || `${circuitType === 'electrical' ? 'Electrical' : 'Logic'} Circuit`;

  if (loading) {
    return <div className={`circuit-viewer loading ${className}`}>Loading circuit...</div>;
  }

  if (error) {
    return <div className={`circuit-viewer error ${className}`}>Error: {error.message}</div>;
  }

  if (!svgContent) {
    return <div className={`circuit-viewer empty ${className}`}>No circuit diagram available</div>;
  }

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.2, 3));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.2, 0.5));
  const handleReset = () => setZoom(1);

  return (
    <div className={`circuit-viewer circuit-${circuitType} ${className}`}>
      <div className="circuit-header">
        <div className="header-left">
          <h3 className="circuit-title">{displayTitle}</h3>
          <span className={`circuit-badge ${circuitType}`}>
            {circuitType === 'electrical' ? '⚡ Electrical' : '🔌 Logic'}
          </span>
        </div>
        {showControls && (
          <div className="circuit-controls">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={showLabels}
                onChange={() => setShowLabels(!showLabels)}
              />
              Labels
            </label>
            <button onClick={handleZoomOut}>−</button>
            <button onClick={handleReset}>Reset</button>
            <button onClick={handleZoomIn}>+</button>
          </div>
        )}
      </div>
      <div className="circuit-container">
        <div
          className={`circuit-content ${!showLabels ? 'hide-labels' : ''}`}
          style={{ transform: `scale(${zoom})` }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      </div>
      <style jsx>{`
        .circuit-viewer {
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 16px;
          background: white;
          margin: 16px 0;
        }
        .circuit-electrical {
          border-color: #ff9800;
        }
        .circuit-logic {
          border-color: #2196f3;
        }
        .circuit-header {
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
        .circuit-title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
          color: #333;
        }
        .circuit-badge {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 500;
          text-transform: uppercase;
        }
        .circuit-badge.electrical {
          background: #fff3e0;
          color: #f57c00;
          border: 1px solid #ffb74d;
        }
        .circuit-badge.logic {
          background: #e3f2fd;
          color: #1976d2;
          border: 1px solid #64b5f6;
        }
        .circuit-controls {
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
        .circuit-controls button {
          padding: 6px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          background: white;
          cursor: pointer;
          transition: all 0.2s;
        }
        .circuit-controls button:hover {
          background: #f5f5f5;
          border-color: #999;
        }
        .circuit-container {
          overflow: auto;
          min-height: 300px;
          background: #fafafa;
          border: 1px solid #e0e0e0;
          border-radius: 4px;
          padding: 20px;
        }
        .circuit-content {
          display: flex;
          justify-content: center;
          align-items: center;
          transition: transform 0.3s ease;
        }
        .circuit-content.hide-labels text {
          display: none;
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

export default CircuitViewer;
