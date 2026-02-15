/**
 * Flowchart Viewer Component
 * Displays algorithm and process flowcharts with zoom and pan
 */

import React, { useState, useRef, useEffect } from 'react';
import { useDiagramContent } from '../hooks/usePhase3Diagrams';

interface FlowchartViewerProps {
  diagramId?: string;
  svgContent?: string;
  title?: string;
  className?: string;
  showControls?: boolean;
}

export const FlowchartViewer: React.FC<FlowchartViewerProps> = ({
  diagramId,
  svgContent: providedSvg,
  title,
  className = '',
  showControls = true
}) => {
  const { content, loading, error } = useDiagramContent(diagramId);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  const svgContent = providedSvg || content?.svg;
  const displayTitle = title || content?.title || 'Flowchart';

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const dx = e.clientX - dragStart.x;
      const dy = e.clientY - dragStart.y;
      setPan({ x: pan.x + dx, y: pan.y + dy });
      setDragStart({ x: e.clientX, y: e.clientY });
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragStart, pan]);

  if (loading) {
    return <div className={`flowchart-viewer loading ${className}`}>Loading flowchart...</div>;
  }

  if (error) {
    return <div className={`flowchart-viewer error ${className}`}>Error: {error.message}</div>;
  }

  if (!svgContent) {
    return <div className={`flowchart-viewer empty ${className}`}>No flowchart available</div>;
  }

  const handleZoomIn = () => setZoom(prev => Math.min(prev + 0.25, 4));
  const handleZoomOut = () => setZoom(prev => Math.max(prev - 0.25, 0.25));
  const handleReset = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX, y: e.clientY });
  };

  return (
    <div className={`flowchart-viewer ${className}`}>
      <div className="flowchart-header">
        <h3 className="flowchart-title">{displayTitle}</h3>
        {showControls && (
          <div className="flowchart-controls">
            <button onClick={handleZoomOut}>−</button>
            <button onClick={handleReset}>Reset</button>
            <button onClick={handleZoomIn}>+</button>
          </div>
        )}
      </div>
      <div 
        ref={containerRef}
        className="flowchart-container"
        onMouseDown={handleMouseDown}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        <div
          className="flowchart-content"
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
            transformOrigin: 'center'
          }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      </div>
      <style jsx>{`
        .flowchart-viewer {
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 16px;
          background: #fafafa;
          margin: 16px 0;
        }
        .flowchart-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid #ddd;
        }
        .flowchart-title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
          color: #333;
        }
        .flowchart-controls {
          display: flex;
          gap: 8px;
        }
        .flowchart-controls button {
          padding: 6px 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          background: white;
          cursor: pointer;
          transition: all 0.2s;
        }
        .flowchart-controls button:hover {
          background: #e3f2fd;
          border-color: #2196f3;
        }
        .flowchart-container {
          overflow: hidden;
          min-height: 400px;
          background: white;
          border: 1px solid #e0e0e0;
          border-radius: 4px;
          position: relative;
        }
        .flowchart-content {
          display: flex;
          justify-content: center;
          align-items: center;
          width: 100%;
          min-height: 400px;
          transition: transform 0.1s;
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

export default FlowchartViewer;
