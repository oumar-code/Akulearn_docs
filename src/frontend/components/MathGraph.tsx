/**
 * MathGraph Component
 * Renders interactive SVG mathematical graphs with zoom, pan, and export features
 */

import React, { useState, useRef, useEffect } from 'react';

interface MathGraphProps {
  svgContent: string;
  title?: string;
  description?: string;
  graphType?: string;
  className?: string;
  showControls?: boolean;
}

interface ViewState {
  scale: number;
  offsetX: number;
  offsetY: number;
}

const MathGraph: React.FC<MathGraphProps> = ({
  svgContent,
  title,
  description,
  graphType = "mathematical",
  className = '',
  showControls = true
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [view, setView] = useState<ViewState>({ scale: 1, offsetX: 0, offsetY: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const handleZoomIn = () => {
    setView(prev => ({ ...prev, scale: Math.min(prev.scale + 0.2, 3) }));
  };

  const handleZoomOut = () => {
    setView(prev => ({ ...prev, scale: Math.max(prev.scale - 0.2, 0.5) }));
  };

  const handleReset = () => {
    setView({ scale: 1, offsetX: 0, offsetY: 0 });
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    if (!showControls) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - view.offsetX, y: e.clientY - view.offsetY });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging || !showControls) return;
    setView(prev => ({
      ...prev,
      offsetX: e.clientX - dragStart.x,
      offsetY: e.clientY - dragStart.y
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (e: React.WheelEvent) => {
    if (!showControls) return;
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    setView(prev => ({
      ...prev,
      scale: Math.max(0.5, Math.min(3, prev.scale + delta))
    }));
  };

  const handleExport = () => {
    if (!svgRef.current) return;

    // Create canvas from SVG
    const svgData = new XMLSerializer().serializeToString(svgRef.current);
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');

    if (!ctx) return;

    const img = new Image();
    img.onload = () => {
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);

      // Download
      const link = document.createElement('a');
      link.href = canvas.toDataURL('image/png');
      link.download = `${title || 'graph'}.png`;
      link.click();
    };

    img.src = `data:image/svg+xml;base64,${btoa(svgData)}`;
  };

  return (
    <div className={`math-graph-container ${className}`}>
      {(title || description) && (
        <div className="math-graph-header">
          {title && <h3 className="math-graph-title">{title}</h3>}
          {description && <p className="math-graph-description">{description}</p>}
        </div>
      )}

      <div
        className="math-graph-wrapper"
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
        style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
      >
        <div
          className="math-graph-content"
          style={{
            transform: `translate(${view.offsetX}px, ${view.offsetY}px) scale(${view.scale})`,
            transformOrigin: 'top left',
            transition: isDragging ? 'none' : 'transform 0.3s ease'
          }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      </div>

      {showControls && (
        <div className="math-graph-controls">
          <button
            onClick={handleZoomOut}
            className="math-graph-btn math-graph-btn-zoom-out"
            title="Zoom out"
            disabled={view.scale <= 0.5}
          >
            🔍−
          </button>

          <button
            onClick={handleReset}
            className="math-graph-btn math-graph-btn-reset"
            title="Reset view"
          >
            ⟲ Reset
          </button>

          <button
            onClick={handleZoomIn}
            className="math-graph-btn math-graph-btn-zoom-in"
            title="Zoom in"
            disabled={view.scale >= 3}
          >
            🔍+
          </button>

          <div className="math-graph-zoom-level">
            {Math.round(view.scale * 100)}%
          </div>

          <button
            onClick={handleExport}
            className="math-graph-btn math-graph-btn-export"
            title="Export as PNG"
          >
            ⬇ Export
          </button>

          <span className="math-graph-hint">Drag to pan, scroll to zoom</span>
        </div>
      )}

      <style jsx>{`
        .math-graph-container {
          margin: 20px 0;
          border-radius: 8px;
          overflow: hidden;
          background: #fff;
          border: 1px solid #e0e0e0;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .math-graph-header {
          padding: 16px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom: 1px solid #e0e0e0;
        }

        .math-graph-title {
          margin: 0 0 4px 0;
          font-size: 16px;
          font-weight: 600;
        }

        .math-graph-description {
          margin: 0;
          font-size: 12px;
          opacity: 0.9;
        }

        .math-graph-wrapper {
          position: relative;
          width: 100%;
          height: 400px;
          overflow: hidden;
          background: #f9f9f9;
          border-bottom: 1px solid #e0e0e0;
        }

        .math-graph-content {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        :global(.math-graph-content svg) {
          max-width: 100%;
          max-height: 100%;
          user-select: none;
        }

        .math-graph-controls {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 16px;
          background: #f5f5f5;
          border-top: 1px solid #e0e0e0;
          flex-wrap: wrap;
        }

        .math-graph-btn {
          padding: 8px 12px;
          background: white;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.3s ease;
          font-weight: 500;
        }

        .math-graph-btn:hover:not(:disabled) {
          background: #e8f4f8;
          border-color: #3498db;
          color: #2980b9;
        }

        .math-graph-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .math-graph-btn-zoom-out,
        .math-graph-btn-zoom-in {
          min-width: 36px;
        }

        .math-graph-btn-reset {
          background: #f0f0f0;
        }

        .math-graph-btn-export {
          background: #27ae60;
          color: white;
          border-color: #229954;
        }

        .math-graph-btn-export:hover {
          background: #229954;
          border-color: #1e8449;
          color: white;
        }

        .math-graph-zoom-level {
          padding: 8px 12px;
          background: white;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 600;
          color: #2980b9;
          min-width: 50px;
          text-align: center;
        }

        .math-graph-hint {
          font-size: 11px;
          color: #999;
          margin-left: auto;
          padding: 0 8px;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .math-graph-wrapper {
            height: 300px;
          }

          .math-graph-controls {
            padding: 10px 12px;
            gap: 6px;
          }

          .math-graph-btn {
            padding: 6px 10px;
            font-size: 11px;
          }

          .math-graph-hint {
            display: none;
          }
        }
      `}</style>
    </div>
  );
};

export default MathGraph;
