/**
 * Tests for ResultsSummary Component
 * 
 * Tests cover:
 * - Results display
 * - Performance level calculation
 * - Statistics rendering
 * - Question review
 * - Circular progress visualization
 * - Action buttons (restart/exit)
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ResultsSummary from './ResultsSummary';
import type { QuizResults, QuestionDetail, AnswerValidation } from '../hooks/usePhase4Questions';

const mockQuestion: QuestionDetail = {
  id: 1,
  question_text: 'What is 2+2?',
  question_type: 'multiple_choice',
  difficulty: 'easy',
  subject: 'Mathematics',
  topic: 'Addition',
  points: 10,
  estimated_time_seconds: 60,
  question_data: {
    options: ['3', '4', '5', '6'],
    correct_answer: 'B',
    explanation: '2+2 equals 4'
  }
};

describe('ResultsSummary Component', () => {
  const mockOnRestart = jest.fn();
  const mockOnExit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Performance Levels', () => {
    it('should display "Excellent" for 90%+', () => {
      const excellentResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 9,
        totalPoints: 100,
        earnedPoints: 95,
        percentage: 95,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={excellentResults} />);

      expect(screen.getByText('Excellent')).toBeInTheDocument();
      expect(screen.getByText(/Outstanding performance/)).toBeInTheDocument();
    });

    it('should display "Good" for 75-89%', () => {
      const goodResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 8,
        totalPoints: 100,
        earnedPoints: 80,
        percentage: 80,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={goodResults} />);

      expect(screen.getByText('Good')).toBeInTheDocument();
      expect(screen.getByText(/Great job/)).toBeInTheDocument();
    });

    it('should display "Fair" for 60-74%', () => {
      const fairResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 7,
        totalPoints: 100,
        earnedPoints: 70,
        percentage: 70,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={fairResults} />);

      expect(screen.getByText('Fair')).toBeInTheDocument();
      expect(screen.getByText(/Making progress/)).toBeInTheDocument();
    });

    it('should display "Needs Improvement" for 40-59%', () => {
      const needsImprovementResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 5,
        totalPoints: 100,
        earnedPoints: 50,
        percentage: 50,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={needsImprovementResults} />);

      expect(screen.getByText('Needs Improvement')).toBeInTheDocument();
      expect(screen.getByText(/Keep practicing/)).toBeInTheDocument();
    });

    it('should display "Poor" for <40%', () => {
      const poorResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 3,
        totalPoints: 100,
        earnedPoints: 30,
        percentage: 30,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={poorResults} />);

      expect(screen.getByText('Poor')).toBeInTheDocument();
      expect(screen.getByText(/Additional study recommended/)).toBeInTheDocument();
    });
  });

  describe('Score Display', () => {
    const results: QuizResults = {
      totalQuestions: 10,
      answeredQuestions: 9,
      correctAnswers: 7,
      totalPoints: 100,
      earnedPoints: 85,
      percentage: 85,
      timeSpent: 450,
      questionResults: []
    };

    it('should display percentage score', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText('85%')).toBeInTheDocument();
    });

    it('should display points earned', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText(/85 \/ 100/)).toBeInTheDocument();
    });

    it('should display correct answers count', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText(/7 \/ 10/)).toBeInTheDocument();
    });

    it('should display answered count', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText(/9 \/ 10/)).toBeInTheDocument();
    });

    it('should display time spent', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText(/7 min 30 sec/)).toBeInTheDocument();
    });
  });

  describe('Statistics Grid', () => {
    const results: QuizResults = {
      totalQuestions: 10,
      answeredQuestions: 9,
      correctAnswers: 6,
      totalPoints: 100,
      earnedPoints: 75,
      percentage: 75,
      timeSpent: 600,
      questionResults: []
    };

    it('should display correct answers stat', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText('Correct')).toBeInTheDocument();
      expect(screen.getByText('6')).toBeInTheDocument();
    });

    it('should display incorrect answers stat', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText('Incorrect')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument(); // 9 answered - 6 correct
    });

    it('should display unanswered stat', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText('Unanswered')).toBeInTheDocument();
      expect(screen.getByText('1')).toBeInTheDocument(); // 10 total - 9 answered
    });

    it('should display average time per question', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.getByText('Avg Time')).toBeInTheDocument();
      expect(screen.getByText(/1:00/)).toBeInTheDocument(); // 600s / 10 = 60s
    });
  });

  describe('Question Review', () => {
    const mockValidation: AnswerValidation = {
      is_correct: true,
      points_earned: 10,
      points_possible: 10,
      feedback: 'Correct!',
      explanation: '2+2 equals 4'
    };

    const resultsWithQuestions: QuizResults = {
      totalQuestions: 1,
      answeredQuestions: 1,
      correctAnswers: 1,
      totalPoints: 10,
      earnedPoints: 10,
      percentage: 100,
      timeSpent: 60,
      questionResults: [
        {
          question: mockQuestion,
          userAnswer: 'B',
          validation: mockValidation
        }
      ]
    };

    it('should display question review section', () => {
      render(
        <ResultsSummary 
          results={resultsWithQuestions}
          showDetailedReview={true}
        />
      );

      expect(screen.getByText('Question Review')).toBeInTheDocument();
    });

    it('should display each question in review', () => {
      render(
        <ResultsSummary 
          results={resultsWithQuestions}
          showDetailedReview={true}
        />
      );

      expect(screen.getByText(/What is 2\+2\?/)).toBeInTheDocument();
    });

    it('should expand question details on click', () => {
      render(
        <ResultsSummary 
          results={resultsWithQuestions}
          showDetailedReview={true}
        />
      );

      const questionItem = screen.getByText(/What is 2\+2\?/);
      fireEvent.click(questionItem);

      expect(screen.getByText('2+2 equals 4')).toBeInTheDocument();
    });

    it('should display correct indicator for correct answers', () => {
      render(
        <ResultsSummary 
          results={resultsWithQuestions}
          showDetailedReview={true}
        />
      );

      expect(screen.getByText('✓')).toBeInTheDocument();
    });

    it('should display incorrect indicator for wrong answers', () => {
      const incorrectValidation: AnswerValidation = {
        is_correct: false,
        points_earned: 0,
        points_possible: 10,
        feedback: 'Incorrect',
        correct_answer: 'B',
        explanation: 'The correct answer is B'
      };

      const resultsWithIncorrect: QuizResults = {
        ...resultsWithQuestions,
        correctAnswers: 0,
        earnedPoints: 0,
        percentage: 0,
        questionResults: [
          {
            question: mockQuestion,
            userAnswer: 'A',
            validation: incorrectValidation
          }
        ]
      };

      render(
        <ResultsSummary 
          results={resultsWithIncorrect}
          showDetailedReview={true}
        />
      );

      expect(screen.getByText('✗')).toBeInTheDocument();
    });

    it('should display unanswered indicator', () => {
      const resultsWithUnanswered: QuizResults = {
        totalQuestions: 1,
        answeredQuestions: 0,
        correctAnswers: 0,
        totalPoints: 10,
        earnedPoints: 0,
        percentage: 0,
        timeSpent: 60,
        questionResults: [
          {
            question: mockQuestion,
            userAnswer: null,
            validation: {
              is_correct: false,
              points_earned: 0,
              points_possible: 10,
              feedback: 'Not answered',
              explanation: ''
            }
          }
        ]
      };

      render(
        <ResultsSummary 
          results={resultsWithUnanswered}
          showDetailedReview={true}
        />
      );

      expect(screen.getByText('−')).toBeInTheDocument();
    });

    it('should hide review when showDetailedReview is false', () => {
      render(
        <ResultsSummary 
          results={resultsWithQuestions}
          showDetailedReview={false}
        />
      );

      expect(screen.queryByText('Question Review')).not.toBeInTheDocument();
    });
  });

  describe('Circular Progress', () => {
    it('should render SVG circular progress', () => {
      const results: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 8,
        totalPoints: 100,
        earnedPoints: 80,
        percentage: 80,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={results} />);

      const svg = screen.getByRole('img', { hidden: true }); // SVG has implicit role
      expect(svg).toBeInTheDocument();
    });

    it('should display percentage in center of circle', () => {
      const results: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 7,
        totalPoints: 100,
        earnedPoints: 75,
        percentage: 75,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={results} />);

      expect(screen.getByText('75%')).toBeInTheDocument();
    });
  });

  describe('Action Buttons', () => {
    const results: QuizResults = {
      totalQuestions: 10,
      answeredQuestions: 10,
      correctAnswers: 8,
      totalPoints: 100,
      earnedPoints: 80,
      percentage: 80,
      timeSpent: 300,
      questionResults: []
    };

    it('should call onRestart when Restart button is clicked', () => {
      render(
        <ResultsSummary 
          results={results}
          onRestart={mockOnRestart}
        />
      );

      const restartButton = screen.getByText('Restart Quiz');
      fireEvent.click(restartButton);

      expect(mockOnRestart).toHaveBeenCalledTimes(1);
    });

    it('should call onExit when Exit button is clicked', () => {
      render(
        <ResultsSummary 
          results={results}
          onExit={mockOnExit}
        />
      );

      const exitButton = screen.getByText('Exit');
      fireEvent.click(exitButton);

      expect(mockOnExit).toHaveBeenCalledTimes(1);
    });

    it('should not display buttons when callbacks are not provided', () => {
      render(<ResultsSummary results={results} />);

      expect(screen.queryByText('Restart Quiz')).not.toBeInTheDocument();
      expect(screen.queryByText('Exit')).not.toBeInTheDocument();
    });
  });

  describe('Answer Formatting', () => {
    it('should format multiple choice answers', () => {
      const mcValidation: AnswerValidation = {
        is_correct: true,
        points_earned: 10,
        points_possible: 10,
        feedback: 'Correct',
        explanation: 'Explanation'
      };

      const resultsWithMC: QuizResults = {
        totalQuestions: 1,
        answeredQuestions: 1,
        correctAnswers: 1,
        totalPoints: 10,
        earnedPoints: 10,
        percentage: 100,
        timeSpent: 60,
        questionResults: [
          {
            question: mockQuestion,
            userAnswer: 'B',
            validation: mcValidation
          }
        ]
      };

      render(
        <ResultsSummary 
          results={resultsWithMC}
          showDetailedReview={true}
        />
      );

      // Expand question
      fireEvent.click(screen.getByText(/What is 2\+2\?/));

      expect(screen.getByText(/Your Answer: B/)).toBeInTheDocument();
    });

    it('should format true/false answers', () => {
      const tfQuestion: QuestionDetail = {
        ...mockQuestion,
        question_type: 'true_false',
        question_data: {
          correct_answer: true,
          explanation: 'True is correct'
        }
      };

      const resultsWithTF: QuizResults = {
        totalQuestions: 1,
        answeredQuestions: 1,
        correctAnswers: 1,
        totalPoints: 10,
        earnedPoints: 10,
        percentage: 100,
        timeSpent: 60,
        questionResults: [
          {
            question: tfQuestion,
            userAnswer: true,
            validation: {
              is_correct: true,
              points_earned: 10,
              points_possible: 10,
              feedback: 'Correct',
              explanation: 'True is correct'
            }
          }
        ]
      };

      render(
        <ResultsSummary 
          results={resultsWithTF}
          showDetailedReview={true}
        />
      );

      fireEvent.click(screen.getByText(/What is 2\+2\?/));

      expect(screen.getByText(/Your Answer: True/)).toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('should handle zero percentage', () => {
      const zeroResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 0,
        totalPoints: 100,
        earnedPoints: 0,
        percentage: 0,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={zeroResults} />);

      expect(screen.getByText('0%')).toBeInTheDocument();
      expect(screen.getByText('Poor')).toBeInTheDocument();
    });

    it('should handle perfect score', () => {
      const perfectResults: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 10,
        totalPoints: 100,
        earnedPoints: 100,
        percentage: 100,
        timeSpent: 300,
        questionResults: []
      };

      render(<ResultsSummary results={perfectResults} />);

      expect(screen.getByText('100%')).toBeInTheDocument();
      expect(screen.getByText('Excellent')).toBeInTheDocument();
    });

    it('should handle no time spent', () => {
      const results: QuizResults = {
        totalQuestions: 10,
        answeredQuestions: 10,
        correctAnswers: 8,
        totalPoints: 100,
        earnedPoints: 80,
        percentage: 80,
        timeSpent: 0,
        questionResults: []
      };

      render(<ResultsSummary results={results} />);

      expect(screen.getByText(/0 sec/)).toBeInTheDocument();
    });
  });
});
