/**
 * Phase 3 Diagrams Gallery Component
 * Unified viewer for all Phase 3 specialized diagrams
 */

import React, { useState, useEffect } from 'react';
import { usePhase3Diagrams, DiagramsByType } from '../hooks/usePhase3Diagrams';
import VennDiagramViewer from './VennDiagramViewer';
import FlowchartViewer from './FlowchartViewer';
import CircuitViewer from './CircuitViewer';
import ChemistryViewer from './ChemistryViewer';

interface Phase3DiagramsGalleryProps {
  lessonId: string;
  className?: string;
}

type DiagramCategory = 'all' | 'venn' | 'flowchart' | 'circuit' | 'chemistry';

export const Phase3DiagramsGallery: React.FC<Phase3DiagramsGalleryProps> = ({
  lessonId,
  className = ''
}) => {
  const { diagrams, loading, error, fetchDiagramsForLesson } = usePhase3Diagrams(lessonId);
  const [activeCategory, setActiveCategory] = useState<DiagramCategory>('all');
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    if (diagrams) {
      const count = 
        diagrams.venn_diagrams.length +
        diagrams.flowcharts.length +
        diagrams.timelines.length +
        diagrams.electrical_circuits.length +
        diagrams.logic_circuits.length +
        diagrams.molecular_structures.length +
        diagrams.chemical_reactions.length;
      setTotalCount(count);
    }
  }, [diagrams]);

  if (loading) {
    return (
      <div className={`phase3-gallery loading ${className}`}>
        <div className="spinner">Loading diagrams...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`phase3-gallery error ${className}`}>
        <p>Error loading diagrams: {error.message}</p>
      </div>
    );
  }

  if (!diagrams || totalCount === 0) {
    return (
      <div className={`phase3-gallery empty ${className}`}>
        <p>No Phase 3 diagrams available for this lesson</p>
      </div>
    );
  }

  const shouldShowCategory = (category: DiagramCategory): boolean => {
    if (activeCategory === 'all') return true;
    return activeCategory === category;
  };

  return (
    <div className={`phase3-gallery ${className}`}>
      <div className="gallery-header">
        <h2 className="gallery-title">Specialized Diagrams</h2>
        <div className="category-tabs">
          <button 
            className={activeCategory === 'all' ? 'active' : ''}
            onClick={() => setActiveCategory('all')}
          >
            All ({totalCount})
          </button>
          {diagrams.venn_diagrams.length > 0 && (
            <button 
              className={activeCategory === 'venn' ? 'active' : ''}
              onClick={() => setActiveCategory('venn')}
            >
              Venn ({diagrams.venn_diagrams.length})
            </button>
          )}
          {diagrams.flowcharts.length > 0 && (
            <button 
              className={activeCategory === 'flowchart' ? 'active' : ''}
              onClick={() => setActiveCategory('flowchart')}
            >
              Flowcharts ({diagrams.flowcharts.length})
            </button>
          )}
          {(diagrams.electrical_circuits.length + diagrams.logic_circuits.length) > 0 && (
            <button 
              className={activeCategory === 'circuit' ? 'active' : ''}
              onClick={() => setActiveCategory('circuit')}
            >
              Circuits ({diagrams.electrical_circuits.length + diagrams.logic_circuits.length})
            </button>
          )}
          {(diagrams.molecular_structures.length + diagrams.chemical_reactions.length) > 0 && (
            <button 
              className={activeCategory === 'chemistry' ? 'active' : ''}
              onClick={() => setActiveCategory('chemistry')}
            >
              Chemistry ({diagrams.molecular_structures.length + diagrams.chemical_reactions.length})
            </button>
          )}
        </div>
      </div>

      <div className="gallery-content">
        {/* Venn Diagrams */}
        {shouldShowCategory('venn') && diagrams.venn_diagrams.map(diagram => (
          <VennDiagramViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
          />
        ))}

        {/* Flowcharts */}
        {shouldShowCategory('flowchart') && diagrams.flowcharts.map(diagram => (
          <FlowchartViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
          />
        ))}

        {/* Electrical Circuits */}
        {shouldShowCategory('circuit') && diagrams.electrical_circuits.map(diagram => (
          <CircuitViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
            circuitType="electrical"
          />
        ))}

        {/* Logic Circuits */}
        {shouldShowCategory('circuit') && diagrams.logic_circuits.map(diagram => (
          <CircuitViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
            circuitType="logic"
          />
        ))}

        {/* Molecular Structures */}
        {shouldShowCategory('chemistry') && diagrams.molecular_structures.map(diagram => (
          <ChemistryViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
            chemistryType="molecular"
          />
        ))}

        {/* Chemical Reactions */}
        {shouldShowCategory('chemistry') && diagrams.chemical_reactions.map(diagram => (
          <ChemistryViewer
            key={diagram.id}
            diagramId={diagram.id}
            title={diagram.title}
            chemistryType="reaction"
          />
        ))}
      </div>

      <style jsx>{`
        .phase3-gallery {
          margin: 24px 0;
        }
        .gallery-header {
          margin-bottom: 24px;
        }
        .gallery-title {
          font-size: 24px;
          font-weight: 700;
          color: #333;
          margin: 0 0 16px 0;
        }
        .category-tabs {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
        .category-tabs button {
          padding: 8px 16px;
          border: 2px solid #e0e0e0;
          border-radius: 20px;
          background: white;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
          color: #666;
          transition: all 0.2s;
        }
        .category-tabs button:hover {
          border-color: #2196f3;
          color: #2196f3;
        }
        .category-tabs button.active {
          background: #2196f3;
          border-color: #2196f3;
          color: white;
        }
        .gallery-content {
          display: grid;
          gap: 24px;
        }
        .loading, .error, .empty {
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
          color: #666;
          font-size: 16px;
        }
        .spinner {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Phase3DiagramsGallery;
