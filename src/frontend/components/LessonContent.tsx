/**
 * Lesson Content with Generated Assets
 * Integrates ASCII diagrams and truth tables into lesson display
 */

import React, { useState, useEffect } from 'react';
import ASCIIDiagram from './ASCIIDiagram';
import TruthTable from './TruthTable';

interface GeneratedAssets {
  ascii_diagram?: {
    type: string;
    content: string;
    format: string;
  };
  truth_table?: {
    type: string;
    content: string;
    format: string;
  };
}

interface LessonWithAssets {
  id: string;
  title: string;
  subject: string;
  content: string;
  generated_assets?: GeneratedAssets;
}

interface LessonContentProps {
  lesson: LessonWithAssets;
  className?: string;
  showAssets?: boolean;
}

const LessonContent: React.FC<LessonContentProps> = ({
  lesson,
  className = '',
  showAssets = true
}) => {
  const [assetData, setAssetData] = useState<GeneratedAssets | null>(null);
  const [loadingAssets, setLoadingAssets] = useState(false);
  const [assetError, setAssetError] = useState<string | null>(null);

  // Load assets if not already provided
  useEffect(() => {
    if (lesson.generated_assets) {
      setAssetData(lesson.generated_assets);
      return;
    }

    if (showAssets && lesson.id) {
      loadAssets(lesson.id);
    }
  }, [lesson.id, lesson.generated_assets, showAssets]);

  const loadAssets = async (lessonId: string) => {
    setLoadingAssets(true);
    setAssetError(null);

    try {
      const response = await fetch(`/api/assets/lesson/${lessonId}`);
      if (response.ok) {
        const data = await response.json();
        setAssetData(data);
      } else if (response.status !== 404) {
        setAssetError('Failed to load generated assets');
      }
    } catch (error) {
      console.error('Error loading assets:', error);
      setAssetError('Error loading generated assets');
    } finally {
      setLoadingAssets(false);
    }
  };

  const hasAssets = assetData && 
    (assetData.ascii_diagram || assetData.truth_table);

  return (
    <article className={`lesson-content ${className}`}>
      {/* Lesson Header */}
      <header className="lesson-header">
        <div className="lesson-header-meta">
          <span className="lesson-subject">{lesson.subject}</span>
          <h1 className="lesson-title">{lesson.title}</h1>
        </div>
      </header>

      {/* Main Content */}
      <section className="lesson-body">
        <div className="lesson-text">
          {lesson.content}
        </div>
      </section>

      {/* Generated Assets Section */}
      {showAssets && (
        <aside className="lesson-assets">
          {loadingAssets && (
            <div className="assets-loading">
              <span className="loading-spinner">⌛</span>
              Loading visual aids...
            </div>
          )}

          {assetError && (
            <div className="assets-error">
              <span className="error-icon">⚠</span>
              {assetError}
            </div>
          )}

          {hasAssets && !loadingAssets && (
            <div className="assets-container">
              <h2 className="assets-title">Visual Learning Aids</h2>

              {assetData.ascii_diagram && (
                <div className="asset-item">
                  <ASCIIDiagram
                    content={assetData.ascii_diagram.content}
                    title="Process Diagram"
                  />
                </div>
              )}

              {assetData.truth_table && (
                <div className="asset-item">
                  <TruthTable
                    content={assetData.truth_table.content}
                    lessonId={lesson.id}
                  />
                </div>
              )}
            </div>
          )}

          {!hasAssets && !loadingAssets && !assetError && showAssets && (
            <div className="assets-unavailable">
              <span className="info-icon">ℹ</span>
              No visual aids generated for this lesson yet.
            </div>
          )}
        </aside>
      )}

      <style jsx>{`
        .lesson-content {
          max-width: 900px;
          margin: 0 auto;
          background: white;
          border-radius: 8px;
          overflow: hidden;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .lesson-header {
          padding: 24px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .lesson-header-meta {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .lesson-subject {
          font-size: 13px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
          opacity: 0.9;
        }

        .lesson-title {
          margin: 0;
          font-size: 28px;
          font-weight: 700;
          line-height: 1.3;
        }

        .lesson-body {
          padding: 24px;
          background: white;
          border-bottom: 1px solid #ecf0f1;
        }

        .lesson-text {
          font-size: 15px;
          line-height: 1.8;
          color: #2c3e50;
          white-space: pre-wrap;
          word-wrap: break-word;
        }

        .lesson-assets {
          padding: 24px;
          background: #f8f9fa;
        }

        .assets-title {
          margin: 0 0 20px 0;
          font-size: 18px;
          font-weight: 600;
          color: #2c3e50;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .assets-title::before {
          content: '✨';
          font-size: 20px;
        }

        .assets-container {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .asset-item {
          animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .assets-loading,
        .assets-error,
        .assets-unavailable {
          padding: 16px;
          border-radius: 6px;
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 14px;
        }

        .assets-loading {
          background: #d4edff;
          color: #0066cc;
          border-left: 4px solid #0066cc;
        }

        .assets-error {
          background: #ffebee;
          color: #c62828;
          border-left: 4px solid #c62828;
        }

        .assets-unavailable {
          background: #f5f5f5;
          color: #666;
          border-left: 4px solid #999;
        }

        .loading-spinner,
        .error-icon,
        .info-icon {
          font-size: 18px;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .lesson-content {
            border-radius: 0;
          }

          .lesson-header {
            padding: 16px;
          }

          .lesson-title {
            font-size: 20px;
          }

          .lesson-body {
            padding: 16px;
          }

          .lesson-assets {
            padding: 16px;
          }

          .assets-title {
            font-size: 16px;
          }

          .lesson-text {
            font-size: 14px;
          }
        }
      `}</style>
    </article>
  );
};

export default LessonContent;
