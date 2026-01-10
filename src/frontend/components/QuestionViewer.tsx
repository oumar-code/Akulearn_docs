/**
 * Question Viewer Component
 * Displays individual practice questions with type-specific rendering
 * Supports: Multiple Choice, True/False, Fill-in-Blank, Matching, Short Answer
 */

import React, { useState, useEffect } from 'react';
import { QuestionDetail, AnswerValidation } from '../hooks/usePhase4Questions';

interface QuestionViewerProps {
  question: QuestionDetail;
  onAnswerSubmit?: (answer: any) => void;
  onValidationResult?: (result: AnswerValidation) => void;
  showFeedback?: boolean;
  validation?: AnswerValidation | null;
  disabled?: boolean;
  className?: string;
}

export const QuestionViewer: React.FC<QuestionViewerProps> = ({
  question,
  onAnswerSubmit,
  onValidationResult,
  showFeedback = true,
  validation,
  disabled = false,
  className = ''
}) => {
  const [userAnswer, setUserAnswer] = useState<any>(null);
  const [submitted, setSubmitted] = useState<boolean>(false);

  // Reset state when question changes
  useEffect(() => {
    setUserAnswer(null);
    setSubmitted(false);
  }, [question.id]);

  // Update when validation prop changes
  useEffect(() => {
    if (validation && onValidationResult) {
      onValidationResult(validation);
      setSubmitted(true);
    }
  }, [validation, onValidationResult]);

  const handleSubmit = () => {
    if (userAnswer !== null && !disabled) {
      setSubmitted(true);
      if (onAnswerSubmit) {
        onAnswerSubmit(userAnswer);
      }
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return '#4caf50';
      case 'medium': return '#ff9800';
      case 'hard': return '#f44336';
      default: return '#757575';
    }
  };

  // Render Multiple Choice Question
  const renderMultipleChoice = () => {
    const { question_text, options = [] } = question.question_data;
    
    return (
      <div className="question-content multiple-choice">
        <p className="question-text">{question_text}</p>
        <div className="options">
          {options.map((option, index) => {
            const isSelected = userAnswer === index;
            const isCorrect = validation?.correct_answer === index;
            const showResult = submitted && showFeedback && validation;
            
            return (
              <label
                key={index}
                className={`option ${isSelected ? 'selected' : ''} ${
                  showResult ? (isCorrect ? 'correct' : isSelected ? 'incorrect' : '') : ''
                }`}
              >
                <input
                  type="radio"
                  name="answer"
                  value={index}
                  checked={isSelected}
                  onChange={() => setUserAnswer(index)}
                  disabled={disabled || submitted}
                />
                <span className="option-label">{String.fromCharCode(65 + index)}.</span>
                <span className="option-text">{option}</span>
                {showResult && isCorrect && <span className="check-mark">✓</span>}
                {showResult && isSelected && !isCorrect && <span className="cross-mark">✗</span>}
              </label>
            );
          })}
        </div>
      </div>
    );
  };

  // Render True/False Question
  const renderTrueFalse = () => {
    const { statement } = question.question_data;
    
    return (
      <div className="question-content true-false">
        <p className="question-text">{statement}</p>
        <div className="options">
          {[true, false].map((value) => {
            const isSelected = userAnswer === value;
            const isCorrect = validation?.correct_answer === value;
            const showResult = submitted && showFeedback && validation;
            
            return (
              <label
                key={value.toString()}
                className={`option ${isSelected ? 'selected' : ''} ${
                  showResult ? (isCorrect ? 'correct' : isSelected ? 'incorrect' : '') : ''
                }`}
              >
                <input
                  type="radio"
                  name="answer"
                  value={value.toString()}
                  checked={isSelected}
                  onChange={() => setUserAnswer(value)}
                  disabled={disabled || submitted}
                />
                <span className="option-text">{value ? 'True' : 'False'}</span>
                {showResult && isCorrect && <span className="check-mark">✓</span>}
                {showResult && isSelected && !isCorrect && <span className="cross-mark">✗</span>}
              </label>
            );
          })}
        </div>
      </div>
    );
  };

  // Render Fill-in-Blank Question
  const renderFillBlank = () => {
    const { sentence } = question.question_data;
    const parts = sentence?.split('______') || [''];
    
    return (
      <div className="question-content fill-blank">
        <div className="sentence">
          {parts.map((part, index) => (
            <React.Fragment key={index}>
              <span>{part}</span>
              {index < parts.length - 1 && (
                <input
                  type="text"
                  className={`blank-input ${
                    submitted && showFeedback && validation
                      ? validation.correct ? 'correct' : 'incorrect'
                      : ''
                  }`}
                  value={userAnswer || ''}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  disabled={disabled || submitted}
                  placeholder="Your answer"
                />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>
    );
  };

  // Render Matching Question
  const renderMatching = () => {
    const { instruction, column_a = [], column_b = [] } = question.question_data;
    const [matches, setMatches] = useState<Record<number, number>>({});
    
    useEffect(() => {
      if (userAnswer) setMatches(userAnswer);
    }, [userAnswer]);
    
    const handleMatch = (indexA: number, indexB: number) => {
      const newMatches = { ...matches, [indexA]: indexB };
      setMatches(newMatches);
      setUserAnswer(newMatches);
    };
    
    const showResult = submitted && showFeedback && validation;
    
    return (
      <div className="question-content matching">
        <p className="instruction">{instruction}</p>
        <div className="matching-columns">
          <div className="column column-a">
            <h4>Column A</h4>
            {column_a.map((item, index) => (
              <div key={index} className="match-item">
                <span className="item-number">{index + 1}.</span>
                <span className="item-text">{item}</span>
              </div>
            ))}
          </div>
          <div className="column column-b">
            <h4>Column B</h4>
            {column_a.map((_, indexA) => (
              <div key={indexA} className="match-select">
                <select
                  value={matches[indexA] ?? ''}
                  onChange={(e) => handleMatch(indexA, parseInt(e.target.value))}
                  disabled={disabled || submitted}
                  className={
                    showResult && validation?.correct_answer
                      ? matches[indexA] === (validation.correct_answer as any)[indexA]
                        ? 'correct'
                        : 'incorrect'
                      : ''
                  }
                >
                  <option value="">Select...</option>
                  {column_b.map((item, indexB) => (
                    <option key={indexB} value={indexB}>
                      {String.fromCharCode(65 + indexB)}. {item}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  // Render Short Answer Question
  const renderShortAnswer = () => {
    const { question_text } = question.question_data;
    
    return (
      <div className="question-content short-answer">
        <p className="question-text">{question_text}</p>
        <textarea
          className="answer-textarea"
          value={userAnswer || ''}
          onChange={(e) => setUserAnswer(e.target.value)}
          disabled={disabled || submitted}
          placeholder="Write your answer here..."
          rows={6}
        />
      </div>
    );
  };

  // Render question based on type
  const renderQuestion = () => {
    switch (question.question_type) {
      case 'multiple_choice':
        return renderMultipleChoice();
      case 'true_false':
        return renderTrueFalse();
      case 'fill_blank':
        return renderFillBlank();
      case 'matching':
        return renderMatching();
      case 'short_answer':
        return renderShortAnswer();
      default:
        return <p>Unsupported question type</p>;
    }
  };

  return (
    <div className={`question-viewer ${className}`}>
      {/* Question Header */}
      <div className="question-header">
        <div className="question-meta">
          <span className="subject-badge">{question.subject}</span>
          <span className="topic-badge">{question.topic}</span>
          <span 
            className="difficulty-badge"
            style={{ backgroundColor: getDifficultyColor(question.difficulty) }}
          >
            {question.difficulty}
          </span>
          <span className="type-badge">{question.question_type.replace('_', ' ')}</span>
        </div>
        <div className="question-stats">
          <span className="points">{question.points} pts</span>
          <span className="time">{question.estimated_time}s</span>
        </div>
      </div>

      {/* Question Content */}
      {renderQuestion()}

      {/* Submit Button */}
      {!submitted && (
        <div className="question-actions">
          <button
            className="submit-button"
            onClick={handleSubmit}
            disabled={disabled || userAnswer === null}
          >
            Submit Answer
          </button>
        </div>
      )}

      {/* Feedback */}
      {submitted && showFeedback && validation && (
        <div className={`feedback ${validation.correct ? 'correct' : 'incorrect'}`}>
          <div className="feedback-header">
            {validation.correct ? (
              <>
                <span className="icon">✓</span>
                <span className="text">Correct!</span>
              </>
            ) : (
              <>
                <span className="icon">✗</span>
                <span className="text">Incorrect</span>
              </>
            )}
            <span className="score">
              {validation.points_earned}/{validation.points_possible} points
            </span>
          </div>
          {validation.explanation && (
            <div className="feedback-explanation">
              <strong>Explanation:</strong> {validation.explanation}
            </div>
          )}
          {validation.requires_manual_grading && (
            <div className="feedback-note">
              <strong>Note:</strong> {validation.note}
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .question-viewer {
          border: 1px solid #e0e0e0;
          border-radius: 12px;
          padding: 24px;
          background: white;
          margin: 16px 0;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .question-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 16px;
          border-bottom: 2px solid #f0f0f0;
          flex-wrap: wrap;
          gap: 12px;
        }

        .question-meta {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .subject-badge, .topic-badge, .difficulty-badge, .type-badge {
          padding: 4px 12px;
          border-radius: 12px;
          font-size: 12px;
          font-weight: 600;
          text-transform: capitalize;
        }

        .subject-badge {
          background: #e3f2fd;
          color: #1976d2;
        }

        .topic-badge {
          background: #f3e5f5;
          color: #7b1fa2;
        }

        .difficulty-badge {
          color: white;
        }

        .type-badge {
          background: #fff3e0;
          color: #e65100;
        }

        .question-stats {
          display: flex;
          gap: 16px;
          font-size: 14px;
          font-weight: 600;
          color: #666;
        }

        .question-content {
          margin: 20px 0;
        }

        .question-text, .instruction, .sentence {
          font-size: 16px;
          line-height: 1.6;
          color: #333;
          margin-bottom: 20px;
        }

        .options {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .option {
          display: flex;
          align-items: center;
          padding: 16px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
          gap: 12px;
        }

        .option:hover:not(.selected):not([disabled]) {
          border-color: #2196f3;
          background: #f5f5f5;
        }

        .option.selected {
          border-color: #2196f3;
          background: #e3f2fd;
        }

        .option.correct {
          border-color: #4caf50;
          background: #e8f5e9;
        }

        .option.incorrect {
          border-color: #f44336;
          background: #ffebee;
        }

        .option input[type="radio"] {
          margin: 0;
        }

        .option-label {
          font-weight: 600;
          color: #666;
        }

        .option-text {
          flex: 1;
        }

        .check-mark {
          color: #4caf50;
          font-size: 20px;
          font-weight: bold;
        }

        .cross-mark {
          color: #f44336;
          font-size: 20px;
          font-weight: bold;
        }

        .blank-input {
          padding: 8px 12px;
          border: 2px solid #e0e0e0;
          border-radius: 4px;
          font-size: 16px;
          min-width: 200px;
          margin: 0 8px;
        }

        .blank-input.correct {
          border-color: #4caf50;
          background: #e8f5e9;
        }

        .blank-input.incorrect {
          border-color: #f44336;
          background: #ffebee;
        }

        .matching-columns {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 24px;
          margin-top: 20px;
        }

        .column h4 {
          margin: 0 0 16px 0;
          font-size: 14px;
          font-weight: 600;
          color: #666;
          text-transform: uppercase;
        }

        .match-item {
          padding: 12px;
          margin-bottom: 12px;
          background: #f5f5f5;
          border-radius: 6px;
          display: flex;
          gap: 8px;
        }

        .item-number {
          font-weight: 600;
          color: #666;
        }

        .match-select {
          margin-bottom: 12px;
        }

        .match-select select {
          width: 100%;
          padding: 12px;
          border: 2px solid #e0e0e0;
          border-radius: 6px;
          font-size: 14px;
        }

        .match-select select.correct {
          border-color: #4caf50;
          background: #e8f5e9;
        }

        .match-select select.incorrect {
          border-color: #f44336;
          background: #ffebee;
        }

        .answer-textarea {
          width: 100%;
          padding: 12px;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 14px;
          font-family: inherit;
          resize: vertical;
        }

        .question-actions {
          margin-top: 24px;
          display: flex;
          justify-content: flex-end;
        }

        .submit-button {
          padding: 12px 32px;
          background: #2196f3;
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: background 0.2s;
        }

        .submit-button:hover:not(:disabled) {
          background: #1976d2;
        }

        .submit-button:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .feedback {
          margin-top: 24px;
          padding: 20px;
          border-radius: 8px;
          border-left: 4px solid;
        }

        .feedback.correct {
          background: #e8f5e9;
          border-left-color: #4caf50;
        }

        .feedback.incorrect {
          background: #ffebee;
          border-left-color: #f44336;
        }

        .feedback-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          font-size: 18px;
          font-weight: 600;
        }

        .feedback-header .icon {
          font-size: 24px;
        }

        .feedback.correct .icon {
          color: #4caf50;
        }

        .feedback.incorrect .icon {
          color: #f44336;
        }

        .feedback-header .score {
          margin-left: auto;
          font-size: 16px;
          color: #666;
        }

        .feedback-explanation, .feedback-note {
          margin-top: 12px;
          line-height: 1.6;
          color: #666;
        }

        @media (max-width: 768px) {
          .matching-columns {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default QuestionViewer;
