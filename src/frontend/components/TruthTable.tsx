/**
 * Truth Table Renderer Component
 * Renders interactive HTML truth tables with auto-grading capability
 */

import React, { useState, useEffect } from 'react';

interface TruthTableProps {
  content: string;
  lessonId?: string;
  onAnswersChange?: (answers: Record<string, number>) => void;
  showSolution?: boolean;
  className?: string;
}

const TruthTable: React.FC<TruthTableProps> = ({
  content,
  lessonId,
  onAnswersChange,
  showSolution = false,
  className = ''
}) => {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const tableRef = React.useRef<HTMLDivElement>(null);

  // Parse table from HTML content
  const parseTableContent = () => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(content, 'text/html');
    return doc.querySelector('table');
  };

  useEffect(() => {
    if (onAnswersChange) {
      onAnswersChange(answers);
    }
  }, [answers, onAnswersChange]);

  const handleAnswerChange = (rowIndex: number, value: string) => {
    setAnswers(prev => ({
      ...prev,
      [`row_${rowIndex}`]: parseInt(value)
    }));
  };

  const handleSubmit = () => {
    setSubmitted(true);
    // Could send to backend for grading
  };

  const handleReset = () => {
    setAnswers({});
    setSubmitted(false);
  };

  return (
    <div className={`truth-table-container ${className}`}>
      <div className="truth-table-header">
        <h3>Logic Truth Table</h3>
        <p className="truth-table-instruction">
          Fill in the Result column for each row based on the logic operation.
        </p>
      </div>

      <div 
        className="truth-table-wrapper"
        ref={tableRef}
        dangerouslySetInnerHTML={{ __html: content }}
      />

      <div className="truth-table-controls">
        <button 
          onClick={handleSubmit}
          className="truth-table-btn truth-table-btn-submit"
          disabled={submitted}
        >
          {submitted ? '✓ Submitted' : 'Submit Answers'}
        </button>
        
        <button 
          onClick={handleReset}
          className="truth-table-btn truth-table-btn-reset"
        >
          Reset
        </button>

        {submitted && (
          <div className="truth-table-feedback">
            <span className="feedback-icon">ℹ</span>
            Your answers have been recorded for this practice.
          </div>
        )}
      </div>

      <style jsx>{`
        .truth-table-container {
          margin: 20px 0;
          border-radius: 8px;
          overflow: hidden;
          background: #f5f5f5;
          border: 1px solid #e0e0e0;
        }

        .truth-table-header {
          padding: 16px;
          background: #2c3e50;
          color: white;
          border-bottom: 1px solid #34495e;
        }

        .truth-table-header h3 {
          margin: 0 0 8px 0;
          font-size: 16px;
          font-weight: 600;
        }

        .truth-table-instruction {
          margin: 0;
          font-size: 13px;
          color: #ecf0f1;
        }

        .truth-table-wrapper {
          padding: 16px;
          background: white;
          overflow-x: auto;
        }

        :global(.truth-table) {
          width: 100%;
          border-collapse: collapse;
          margin: 0;
        }

        :global(.truth-table th) {
          background-color: #ecf0f1;
          padding: 12px 8px;
          text-align: center;
          font-weight: 600;
          border: 1px solid #bdc3c7;
          font-size: 13px;
        }

        :global(.truth-table td) {
          padding: 10px 8px;
          text-align: center;
          border: 1px solid #ecf0f1;
          font-size: 13px;
        }

        :global(.truth-table tr:nth-child(even)) {
          background-color: #f9f9f9;
        }

        :global(.truth-table input) {
          width: 50px;
          padding: 6px;
          text-align: center;
          border: 1px solid #3498db;
          border-radius: 4px;
          font-size: 13px;
        }

        :global(.truth-table input:focus) {
          outline: none;
          border-color: #2980b9;
          box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }

        .truth-table-controls {
          padding: 16px;
          background: #f5f5f5;
          display: flex;
          gap: 12px;
          align-items: center;
          justify-content: flex-start;
          flex-wrap: wrap;
          border-top: 1px solid #e0e0e0;
        }

        .truth-table-btn {
          padding: 10px 16px;
          border: none;
          border-radius: 4px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .truth-table-btn-submit {
          background: #27ae60;
          color: white;
        }

        .truth-table-btn-submit:hover:not(:disabled) {
          background: #229954;
        }

        .truth-table-btn-submit:disabled {
          background: #95a5a6;
          cursor: not-allowed;
        }

        .truth-table-btn-reset {
          background: #95a5a6;
          color: white;
        }

        .truth-table-btn-reset:hover {
          background: #7f8c8d;
        }

        .truth-table-feedback {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 12px;
          background: #d5f4e6;
          border-left: 4px solid #27ae60;
          border-radius: 4px;
          color: #229954;
          font-size: 13px;
        }

        .feedback-icon {
          font-size: 16px;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .truth-table-header {
            padding: 12px;
          }

          .truth-table-header h3 {
            font-size: 14px;
          }

          .truth-table-wrapper {
            padding: 12px;
          }

          .truth-table-controls {
            padding: 12px;
            gap: 8px;
          }

          .truth-table-btn {
            padding: 8px 12px;
            font-size: 12px;
          }

          :global(.truth-table th),
          :global(.truth-table td) {
            padding: 8px 4px;
            font-size: 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default TruthTable;
