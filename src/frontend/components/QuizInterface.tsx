/**
 * Quiz Interface Component
 * Manages multi-question quiz flow with navigation, timer, and progress tracking
 */

import React, { useState, useEffect, useCallback } from 'react';
import { QuestionDetail, AnswerValidation, usePhase4Questions } from '../hooks/usePhase4Questions';
import QuestionViewer from './QuestionViewer';

interface QuizInterfaceProps {
  questions?: QuestionDetail[];
  quizConfig?: QuizConfig;
  onQuizComplete?: (results: QuizResults) => void;
  onQuizExit?: () => void;
  className?: string;
}

export interface QuizConfig {
  subject?: string;
  difficulty?: string;
  questionCount?: number;
  timeLimit?: number; // in minutes
  showFeedback?: boolean;
  allowReview?: boolean;
}

export interface QuizResults {
  totalQuestions: number;
  answeredQuestions: number;
  correctAnswers: number;
  totalPoints: number;
  earnedPoints: number;
  percentage: number;
  timeSpent: number;
  questionResults: Array<{
    question: QuestionDetail;
    userAnswer: any;
    validation: AnswerValidation;
  }>;
}

export const QuizInterface: React.FC<QuizInterfaceProps> = ({
  questions: providedQuestions,
  quizConfig,
  onQuizComplete,
  onQuizExit,
  className = ''
}) => {
  const { 
    questions: fetchedQuestions, 
    loading, 
    error, 
    generateQuiz,
    validateAnswer 
  } = usePhase4Questions();

  const questions = providedQuestions || fetchedQuestions || [];
  
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number>(0);
  const [userAnswers, setUserAnswers] = useState<Record<number, any>>({});
  const [validations, setValidations] = useState<Record<number, AnswerValidation>>({});
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [quizCompleted, setQuizCompleted] = useState<boolean>(false);
  const [startTime] = useState<number>(Date.now());
  const [timeRemaining, setTimeRemaining] = useState<number | null>(
    quizConfig?.timeLimit ? quizConfig.timeLimit * 60 : null
  );

  // Generate quiz on mount if no questions provided
  useEffect(() => {
    if (!providedQuestions && quizConfig) {
      generateQuiz({
        subject: quizConfig.subject,
        difficulty: quizConfig.difficulty,
        question_count: quizConfig.questionCount || 10
      });
    }
  }, [providedQuestions, quizConfig, generateQuiz]);

  // Timer effect
  useEffect(() => {
    if (timeRemaining === null || quizCompleted) return;

    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev === null || prev <= 0) {
          handleQuizComplete();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeRemaining, quizCompleted]);

  const currentQuestion = questions[currentQuestionIndex];

  const handleAnswerSubmit = useCallback(async (answer: any) => {
    if (!currentQuestion) return;

    setIsSubmitting(true);
    
    // Store user answer
    setUserAnswers(prev => ({
      ...prev,
      [currentQuestionIndex]: answer
    }));

    // Validate answer
    const validation = await validateAnswer(currentQuestion.id, answer);
    
    if (validation) {
      setValidations(prev => ({
        ...prev,
        [currentQuestionIndex]: validation
      }));
    }

    setIsSubmitting(false);
  }, [currentQuestion, currentQuestionIndex, validateAnswer]);

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleJumpToQuestion = (index: number) => {
    setCurrentQuestionIndex(index);
  };

  const handleQuizComplete = useCallback(() => {
    setQuizCompleted(true);

    // Calculate results
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    const answeredCount = Object.keys(userAnswers).length;
    const correctCount = Object.values(validations).filter(v => v.correct).length;
    const totalPoints = questions.reduce((sum, q) => sum + q.points, 0);
    const earnedPoints = Object.values(validations).reduce((sum, v) => sum + (v.points_earned || 0), 0);
    const percentage = totalPoints > 0 ? (earnedPoints / totalPoints) * 100 : 0;

    const questionResults = questions.map((question, index) => ({
      question,
      userAnswer: userAnswers[index],
      validation: validations[index] || {
        valid: false,
        error: 'Not answered'
      }
    }));

    const results: QuizResults = {
      totalQuestions: questions.length,
      answeredQuestions: answeredCount,
      correctAnswers: correctCount,
      totalPoints,
      earnedPoints,
      percentage,
      timeSpent,
      questionResults
    };

    if (onQuizComplete) {
      onQuizComplete(results);
    }
  }, [questions, userAnswers, validations, startTime, onQuizComplete]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getProgressPercentage = (): number => {
    return (Object.keys(userAnswers).length / questions.length) * 100;
  };

  if (loading) {
    return (
      <div className={`quiz-interface loading ${className}`}>
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading quiz...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`quiz-interface error ${className}`}>
        <div className="error-message">
          <p>Failed to load quiz: {error.message}</p>
          <button onClick={onQuizExit}>Exit</button>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className={`quiz-interface empty ${className}`}>
        <p>No questions available</p>
        <button onClick={onQuizExit}>Exit</button>
      </div>
    );
  }

  if (quizCompleted) {
    return null; // Results will be shown by parent via onQuizComplete
  }

  return (
    <div className={`quiz-interface ${className}`}>
      {/* Quiz Header */}
      <div className="quiz-header">
        <div className="quiz-title">
          <h2>Practice Quiz</h2>
          {quizConfig?.subject && <span className="subject">{quizConfig.subject}</span>}
        </div>
        <div className="quiz-stats">
          <div className="stat">
            <span className="label">Question</span>
            <span className="value">{currentQuestionIndex + 1} / {questions.length}</span>
          </div>
          <div className="stat">
            <span className="label">Progress</span>
            <span className="value">{Object.keys(userAnswers).length} answered</span>
          </div>
          {timeRemaining !== null && (
            <div className={`stat timer ${timeRemaining < 60 ? 'warning' : ''}`}>
              <span className="label">Time</span>
              <span className="value">{formatTime(timeRemaining)}</span>
            </div>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ width: `${getProgressPercentage()}%` }}
        />
      </div>

      {/* Question Navigation */}
      <div className="question-navigation">
        {questions.map((_, index) => (
          <button
            key={index}
            className={`nav-button ${index === currentQuestionIndex ? 'active' : ''} ${
              userAnswers[index] !== undefined ? 'answered' : ''
            }`}
            onClick={() => handleJumpToQuestion(index)}
          >
            {index + 1}
          </button>
        ))}
      </div>

      {/* Current Question */}
      {currentQuestion && (
        <QuestionViewer
          question={currentQuestion}
          onAnswerSubmit={handleAnswerSubmit}
          validation={validations[currentQuestionIndex]}
          showFeedback={quizConfig?.showFeedback !== false}
          disabled={isSubmitting}
        />
      )}

      {/* Quiz Controls */}
      <div className="quiz-controls">
        <div className="navigation-buttons">
          <button
            className="nav-btn secondary"
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            ← Previous
          </button>
          <button
            className="nav-btn secondary"
            onClick={onQuizExit}
          >
            Exit Quiz
          </button>
          {currentQuestionIndex < questions.length - 1 ? (
            <button
              className="nav-btn primary"
              onClick={handleNext}
            >
              Next →
            </button>
          ) : (
            <button
              className="nav-btn primary complete"
              onClick={handleQuizComplete}
              disabled={Object.keys(userAnswers).length < questions.length}
            >
              Complete Quiz
            </button>
          )}
        </div>
      </div>

      <style jsx>{`
        .quiz-interface {
          max-width: 900px;
          margin: 0 auto;
          padding: 24px;
        }

        .loading-spinner {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 400px;
          gap: 16px;
        }

        .spinner {
          width: 48px;
          height: 48px;
          border: 4px solid #f3f3f3;
          border-top: 4px solid #2196f3;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .quiz-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
          padding: 20px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          flex-wrap: wrap;
          gap: 16px;
        }

        .quiz-title h2 {
          margin: 0 0 4px 0;
          font-size: 24px;
          color: #333;
        }

        .quiz-title .subject {
          font-size: 14px;
          color: #666;
          font-weight: 500;
        }

        .quiz-stats {
          display: flex;
          gap: 24px;
        }

        .stat {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 4px;
        }

        .stat .label {
          font-size: 12px;
          color: #999;
          text-transform: uppercase;
          font-weight: 600;
        }

        .stat .value {
          font-size: 18px;
          font-weight: 700;
          color: #333;
        }

        .stat.timer.warning .value {
          color: #f44336;
          animation: pulse 1s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }

        .progress-bar {
          height: 8px;
          background: #e0e0e0;
          border-radius: 4px;
          overflow: hidden;
          margin-bottom: 24px;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #2196f3 0%, #21cbf3 100%);
          transition: width 0.3s ease;
        }

        .question-navigation {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-bottom: 24px;
          padding: 16px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .nav-button {
          width: 40px;
          height: 40px;
          border: 2px solid #e0e0e0;
          background: white;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 600;
          color: #666;
          cursor: pointer;
          transition: all 0.2s;
        }

        .nav-button:hover {
          border-color: #2196f3;
          background: #f5f5f5;
        }

        .nav-button.active {
          border-color: #2196f3;
          background: #2196f3;
          color: white;
        }

        .nav-button.answered {
          border-color: #4caf50;
          background: #e8f5e9;
          color: #4caf50;
        }

        .nav-button.answered.active {
          background: #4caf50;
          color: white;
        }

        .quiz-controls {
          margin-top: 24px;
          padding: 20px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        .navigation-buttons {
          display: flex;
          justify-content: space-between;
          gap: 12px;
        }

        .nav-btn {
          padding: 12px 24px;
          border: none;
          border-radius: 8px;
          font-size: 16px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }

        .nav-btn.primary {
          background: #2196f3;
          color: white;
        }

        .nav-btn.primary:hover:not(:disabled) {
          background: #1976d2;
        }

        .nav-btn.primary.complete {
          background: #4caf50;
        }

        .nav-btn.primary.complete:hover:not(:disabled) {
          background: #388e3c;
        }

        .nav-btn.secondary {
          background: #f5f5f5;
          color: #333;
          border: 1px solid #e0e0e0;
        }

        .nav-btn.secondary:hover:not(:disabled) {
          background: #e0e0e0;
        }

        .nav-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .error-message, .empty {
          text-align: center;
          padding: 40px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        @media (max-width: 768px) {
          .quiz-interface {
            padding: 16px;
          }

          .quiz-header {
            flex-direction: column;
            align-items: flex-start;
          }

          .quiz-stats {
            width: 100%;
            justify-content: space-between;
          }

          .navigation-buttons {
            flex-direction: column;
          }

          .nav-button {
            width: 36px;
            height: 36px;
            font-size: 12px;
          }
        }
      `}</style>
    </div>
  );
};

export default QuizInterface;
