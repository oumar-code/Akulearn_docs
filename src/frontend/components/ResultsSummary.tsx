/**
 * Results Summary Component
 * Displays quiz results with score breakdown, question review, and performance analytics
 */

import React, { useState } from 'react';
import { QuizResults } from './QuizInterface';

interface ResultsSummaryProps {
  results: QuizResults;
  onRestart?: () => void;
  onExit?: () => void;
  showDetailedReview?: boolean;
  className?: string;
}

export const ResultsSummary: React.FC<ResultsSummaryProps> = ({
  results,
  onRestart,
  onExit,
  showDetailedReview = true,
  className = ''
}) => {
  const [expandedQuestion, setExpandedQuestion] = useState<number | null>(null);

  const getPerformanceLevel = (percentage: number): {
    level: string;
    color: string;
    message: string;
  } => {
    if (percentage >= 90) {
      return {
        level: 'Excellent',
        color: '#4caf50',
        message: 'Outstanding performance! You have mastered this material.'
      };
    } else if (percentage >= 75) {
      return {
        level: 'Good',
        color: '#8bc34a',
        message: 'Great job! You have a solid understanding of the content.'
      };
    } else if (percentage >= 60) {
      return {
        level: 'Fair',
        color: '#ff9800',
        message: 'You\'re making progress. Review the topics you missed.'
      };
    } else if (percentage >= 40) {
      return {
        level: 'Needs Improvement',
        color: '#ff5722',
        message: 'Keep practicing. Focus on the areas where you struggled.'
      };
    } else {
      return {
        level: 'Poor',
        color: '#f44336',
        message: 'Additional study is recommended. Review the material carefully.'
      };
    }
  };

  const performance = getPerformanceLevel(results.percentage);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    if (mins === 0) {
      return `${secs}s`;
    }
    return `${mins}m ${secs}s`;
  };

  const toggleQuestionExpand = (index: number) => {
    setExpandedQuestion(expandedQuestion === index ? null : index);
  };

  const getQuestionTypeLabel = (type: string): string => {
    const labels: Record<string, string> = {
      multiple_choice: 'Multiple Choice',
      true_false: 'True/False',
      fill_blank: 'Fill in the Blank',
      matching: 'Matching',
      short_answer: 'Short Answer'
    };
    return labels[type] || type;
  };

  return (
    <div className={`results-summary ${className}`}>
      {/* Score Card */}
      <div className="score-card" style={{ borderLeftColor: performance.color }}>
        <div className="score-header">
          <h2>Quiz Complete!</h2>
          <div 
            className="performance-badge"
            style={{ backgroundColor: performance.color }}
          >
            {performance.level}
          </div>
        </div>
        
        <div className="score-main">
          <div className="score-circle">
            <svg viewBox="0 0 200 200" className="circle-svg">
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="#e0e0e0"
                strokeWidth="12"
              />
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke={performance.color}
                strokeWidth="12"
                strokeDasharray={`${2 * Math.PI * 90}`}
                strokeDashoffset={`${2 * Math.PI * 90 * (1 - results.percentage / 100)}`}
                transform="rotate(-90 100 100)"
                strokeLinecap="round"
              />
            </svg>
            <div className="score-text">
              <span className="percentage">{Math.round(results.percentage)}%</span>
              <span className="label">Score</span>
            </div>
          </div>
          
          <div className="score-details">
            <div className="detail-item">
              <span className="label">Points Earned</span>
              <span className="value">{results.earnedPoints} / {results.totalPoints}</span>
            </div>
            <div className="detail-item">
              <span className="label">Correct Answers</span>
              <span className="value">{results.correctAnswers} / {results.totalQuestions}</span>
            </div>
            <div className="detail-item">
              <span className="label">Questions Answered</span>
              <span className="value">{results.answeredQuestions} / {results.totalQuestions}</span>
            </div>
            <div className="detail-item">
              <span className="label">Time Spent</span>
              <span className="value">{formatTime(results.timeSpent)}</span>
            </div>
          </div>
        </div>

        <p className="performance-message">{performance.message}</p>
      </div>

      {/* Statistics */}
      <div className="statistics-grid">
        <div className="stat-box">
          <div className="stat-icon">✓</div>
          <div className="stat-value" style={{ color: '#4caf50' }}>
            {results.correctAnswers}
          </div>
          <div className="stat-label">Correct</div>
        </div>
        <div className="stat-box">
          <div className="stat-icon">✗</div>
          <div className="stat-value" style={{ color: '#f44336' }}>
            {results.answeredQuestions - results.correctAnswers}
          </div>
          <div className="stat-label">Incorrect</div>
        </div>
        <div className="stat-box">
          <div className="stat-icon">−</div>
          <div className="stat-value" style={{ color: '#ff9800' }}>
            {results.totalQuestions - results.answeredQuestions}
          </div>
          <div className="stat-label">Unanswered</div>
        </div>
        <div className="stat-box">
          <div className="stat-icon">⏱</div>
          <div className="stat-value" style={{ color: '#2196f3' }}>
            {Math.round(results.timeSpent / results.answeredQuestions || 0)}s
          </div>
          <div className="stat-label">Avg Time</div>
        </div>
      </div>

      {/* Question Review */}
      {showDetailedReview && (
        <div className="question-review">
          <h3>Question Review</h3>
          <div className="review-list">
            {results.questionResults.map((result, index) => {
              const isExpanded = expandedQuestion === index;
              const isCorrect = result.validation?.correct;
              const isAnswered = result.userAnswer !== undefined;

              return (
                <div
                  key={index}
                  className={`review-item ${isExpanded ? 'expanded' : ''} ${
                    !isAnswered ? 'unanswered' : isCorrect ? 'correct' : 'incorrect'
                  }`}
                >
                  <div 
                    className="review-header"
                    onClick={() => toggleQuestionExpand(index)}
                  >
                    <div className="question-number">
                      <span>Q{index + 1}</span>
                      {isCorrect && <span className="icon">✓</span>}
                      {!isCorrect && isAnswered && <span className="icon">✗</span>}
                      {!isAnswered && <span className="icon">−</span>}
                    </div>
                    <div className="question-info">
                      <span className="topic">{result.question.topic}</span>
                      <span className="type">{getQuestionTypeLabel(result.question.question_type)}</span>
                    </div>
                    <div className="question-score">
                      {isAnswered ? (
                        <span>{result.validation?.points_earned || 0} / {result.question.points} pts</span>
                      ) : (
                        <span className="not-answered">Not answered</span>
                      )}
                    </div>
                    <button className="expand-btn">
                      {isExpanded ? '▼' : '▶'}
                    </button>
                  </div>

                  {isExpanded && (
                    <div className="review-content">
                      <div className="question-text">
                        {result.question.question_data.question_text ||
                         result.question.question_data.statement ||
                         result.question.question_data.sentence ||
                         'Question content'}
                      </div>
                      
                      {result.userAnswer !== undefined && (
                        <div className="answer-section">
                          <div className="your-answer">
                            <strong>Your Answer:</strong>
                            <span>{formatAnswer(result.userAnswer, result.question)}</span>
                          </div>
                          {!isCorrect && result.validation?.correct_answer !== undefined && (
                            <div className="correct-answer">
                              <strong>Correct Answer:</strong>
                              <span>{formatAnswer(result.validation.correct_answer, result.question)}</span>
                            </div>
                          )}
                        </div>
                      )}

                      {result.validation?.explanation && (
                        <div className="explanation">
                          <strong>Explanation:</strong>
                          <p>{result.validation.explanation}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="results-actions">
        {onRestart && (
          <button className="action-btn primary" onClick={onRestart}>
            Take Another Quiz
          </button>
        )}
        {onExit && (
          <button className="action-btn secondary" onClick={onExit}>
            Exit
          </button>
        )}
      </div>

      <style jsx>{`
        .results-summary {
          max-width: 900px;
          margin: 0 auto;
          padding: 24px;
        }

        .score-card {
          background: white;
          border-radius: 16px;
          padding: 32px;
          margin-bottom: 24px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          border-left: 6px solid;
        }

        .score-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 32px;
        }

        .score-header h2 {
          margin: 0;
          font-size: 28px;
          color: #333;
        }

        .performance-badge {
          padding: 8px 20px;
          border-radius: 20px;
          color: white;
          font-weight: 600;
          font-size: 14px;
        }

        .score-main {
          display: grid;
          grid-template-columns: 240px 1fr;
          gap: 40px;
          margin-bottom: 24px;
        }

        .score-circle {
          position: relative;
          width: 200px;
          height: 200px;
        }

        .circle-svg {
          width: 100%;
          height: 100%;
        }

        .score-text {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          text-align: center;
        }

        .percentage {
          display: block;
          font-size: 48px;
          font-weight: 700;
          color: #333;
          line-height: 1;
          margin-bottom: 8px;
        }

        .score-text .label {
          font-size: 14px;
          color: #999;
          text-transform: uppercase;
          font-weight: 600;
        }

        .score-details {
          display: flex;
          flex-direction: column;
          justify-content: center;
          gap: 20px;
        }

        .detail-item {
          display: flex;
          justify-content: space-between;
          padding: 12px 0;
          border-bottom: 1px solid #f0f0f0;
        }

        .detail-item .label {
          color: #666;
          font-size: 14px;
        }

        .detail-item .value {
          font-weight: 700;
          font-size: 16px;
          color: #333;
        }

        .performance-message {
          text-align: center;
          font-size: 16px;
          color: #666;
          line-height: 1.6;
          margin: 0;
        }

        .statistics-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          margin-bottom: 24px;
        }

        .stat-box {
          background: white;
          border-radius: 12px;
          padding: 24px;
          text-align: center;
          box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .stat-icon {
          font-size: 32px;
          margin-bottom: 12px;
        }

        .stat-value {
          font-size: 32px;
          font-weight: 700;
          margin-bottom: 8px;
        }

        .stat-label {
          font-size: 12px;
          color: #999;
          text-transform: uppercase;
          font-weight: 600;
        }

        .question-review {
          background: white;
          border-radius: 12px;
          padding: 24px;
          margin-bottom: 24px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .question-review h3 {
          margin: 0 0 20px 0;
          font-size: 20px;
          color: #333;
        }

        .review-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .review-item {
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          overflow: hidden;
          transition: all 0.2s;
        }

        .review-item.correct {
          border-color: #4caf50;
        }

        .review-item.incorrect {
          border-color: #f44336;
        }

        .review-item.unanswered {
          border-color: #ff9800;
        }

        .review-header {
          display: flex;
          align-items: center;
          padding: 16px;
          cursor: pointer;
          background: white;
          transition: background 0.2s;
          gap: 16px;
        }

        .review-header:hover {
          background: #f9f9f9;
        }

        .question-number {
          display: flex;
          align-items: center;
          gap: 8px;
          min-width: 60px;
          font-weight: 600;
          font-size: 16px;
        }

        .review-item.correct .question-number {
          color: #4caf50;
        }

        .review-item.incorrect .question-number {
          color: #f44336;
        }

        .review-item.unanswered .question-number {
          color: #ff9800;
        }

        .question-number .icon {
          font-size: 20px;
        }

        .question-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .topic {
          font-size: 14px;
          font-weight: 600;
          color: #333;
        }

        .type {
          font-size: 12px;
          color: #999;
        }

        .question-score {
          font-weight: 600;
          color: #666;
        }

        .not-answered {
          color: #ff9800;
        }

        .expand-btn {
          background: none;
          border: none;
          font-size: 16px;
          color: #666;
          cursor: pointer;
          padding: 4px;
        }

        .review-content {
          padding: 20px;
          background: #f9f9f9;
          border-top: 1px solid #e0e0e0;
        }

        .question-text {
          font-size: 15px;
          line-height: 1.6;
          color: #333;
          margin-bottom: 16px;
          padding: 16px;
          background: white;
          border-radius: 8px;
        }

        .answer-section {
          margin-bottom: 16px;
        }

        .your-answer, .correct-answer {
          padding: 12px;
          margin-bottom: 8px;
          border-radius: 6px;
        }

        .your-answer {
          background: #fff3cd;
          border-left: 4px solid #ff9800;
        }

        .correct-answer {
          background: #d4edda;
          border-left: 4px solid #4caf50;
        }

        .your-answer strong, .correct-answer strong {
          display: block;
          margin-bottom: 4px;
          font-size: 12px;
          text-transform: uppercase;
        }

        .explanation {
          padding: 16px;
          background: white;
          border-radius: 8px;
          border-left: 4px solid #2196f3;
        }

        .explanation strong {
          display: block;
          margin-bottom: 8px;
          color: #2196f3;
          font-size: 14px;
        }

        .explanation p {
          margin: 0;
          line-height: 1.6;
          color: #666;
        }

        .results-actions {
          display: flex;
          justify-content: center;
          gap: 16px;
        }

        .action-btn {
          padding: 14px 32px;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .action-btn.primary {
          background: #2196f3;
          color: white;
        }

        .action-btn.primary:hover {
          background: #1976d2;
        }

        .action-btn.secondary {
          background: #f5f5f5;
          color: #333;
          border: 1px solid #e0e0e0;
        }

        .action-btn.secondary:hover {
          background: #e0e0e0;
        }

        @media (max-width: 768px) {
          .score-main {
            grid-template-columns: 1fr;
            justify-items: center;
            gap: 24px;
          }

          .statistics-grid {
            grid-template-columns: repeat(2, 1fr);
          }

          .review-header {
            flex-wrap: wrap;
          }

          .question-info {
            flex-basis: 100%;
            order: 3;
          }
        }
      `}</style>
    </div>
  );
};

// Helper function to format answers for display
function formatAnswer(answer: any, question: any): string {
  if (answer === null || answer === undefined) {
    return 'No answer';
  }

  const type = question.question_type;

  switch (type) {
    case 'multiple_choice':
      if (typeof answer === 'number' && question.question_data.options) {
        return `${String.fromCharCode(65 + answer)}. ${question.question_data.options[answer]}`;
      }
      return String(answer);

    case 'true_false':
      return answer ? 'True' : 'False';

    case 'fill_blank':
      return String(answer);

    case 'matching':
      if (typeof answer === 'object') {
        return Object.entries(answer)
          .map(([k, v]) => `${parseInt(k) + 1} → ${String.fromCharCode(65 + (v as number))}`)
          .join(', ');
      }
      return String(answer);

    case 'short_answer':
      return String(answer).substring(0, 100) + (String(answer).length > 100 ? '...' : '');

    default:
      return String(answer);
  }
}

export default ResultsSummary;
