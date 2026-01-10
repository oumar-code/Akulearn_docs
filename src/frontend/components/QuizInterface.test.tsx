/**
 * Tests for QuizInterface Component
 * 
 * Tests cover:
 * - Quiz initialization
 * - Question navigation
 * - Answer submission and collection
 * - Timer functionality
 * - Progress tracking
 * - Quiz completion
 * - Results calculation
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import QuizInterface from './QuizInterface';
import type { QuestionDetail, QuizConfig, QuizResults } from '../hooks/usePhase4Questions';

// Mock questions for testing
const mockQuestions: QuestionDetail[] = [
  {
    id: 1,
    question_text: 'What is 2+2?',
    question_type: 'multiple_choice',
    difficulty: 'easy',
    subject: 'Mathematics',
    topic: 'Addition',
    points: 5,
    estimated_time_seconds: 60,
    question_data: {
      options: ['3', '4', '5', '6'],
      correct_answer: 'B',
      explanation: '2+2 equals 4'
    }
  },
  {
    id: 2,
    question_text: 'Is water H2O?',
    question_type: 'true_false',
    difficulty: 'easy',
    subject: 'Chemistry',
    topic: 'Compounds',
    points: 5,
    estimated_time_seconds: 30,
    question_data: {
      correct_answer: true,
      explanation: 'Water is H2O'
    }
  },
  {
    id: 3,
    question_text: 'Explain photosynthesis',
    question_type: 'short_answer',
    difficulty: 'hard',
    subject: 'Biology',
    topic: 'Plants',
    points: 10,
    estimated_time_seconds: 180,
    question_data: {
      expected_keywords: ['light', 'energy'],
      sample_answer: 'Process of converting light...',
      explanation: 'Photosynthesis explanation'
    }
  }
];

describe('QuizInterface Component', () => {
  const mockOnQuizComplete = jest.fn();
  const mockOnQuizExit = jest.fn();

  const defaultConfig: QuizConfig = {
    subject: 'All',
    difficulty: 'medium',
    questionCount: 3,
    timeLimit: 10, // 10 minutes
    showFeedback: true,
    allowReview: true
  };

  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('Initialization', () => {
    it('should render quiz with first question', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      expect(screen.getByText('What is 2+2?')).toBeInTheDocument();
      expect(screen.getByText(/Question 1 of 3/)).toBeInTheDocument();
    });

    it('should display progress bar', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      const progressBar = screen.getByRole('progressbar');
      expect(progressBar).toBeInTheDocument();
    });

    it('should display timer when timeLimit is set', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      expect(screen.getByText(/10:00/)).toBeInTheDocument();
    });

    it('should display question grid', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      expect(screen.getByText('1')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    it('should navigate to next question', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      const nextButton = screen.getByText('Next');
      fireEvent.click(nextButton);

      expect(screen.getByText('Is water H2O?')).toBeInTheDocument();
      expect(screen.getByText(/Question 2 of 3/)).toBeInTheDocument();
    });

    it('should navigate to previous question', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      // Go to second question
      fireEvent.click(screen.getByText('Next'));
      expect(screen.getByText('Is water H2O?')).toBeInTheDocument();

      // Go back to first
      fireEvent.click(screen.getByText('Previous'));
      expect(screen.getByText('What is 2+2?')).toBeInTheDocument();
    });

    it('should disable Previous button on first question', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      const previousButton = screen.getByText('Previous');
      expect(previousButton).toBeDisabled();
    });

    it('should show Finish button on last question', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      // Navigate to last question
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));

      expect(screen.getByText('Finish Quiz')).toBeInTheDocument();
    });

    it('should jump to specific question via grid', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      // Click question 3 in grid
      const questionButtons = screen.getAllByRole('button');
      const question3Button = questionButtons.find(btn => btn.textContent === '3');
      fireEvent.click(question3Button!);

      expect(screen.getByText('Explain photosynthesis')).toBeInTheDocument();
    });
  });

  describe('Answer Collection', () => {
    it('should collect and store answers', async () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizComplete={mockOnQuizComplete}
        />
      );

      // Answer first question
      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);
      
      // Navigate to second question
      fireEvent.click(screen.getByText('Next'));
      
      // Answer second question
      fireEvent.click(screen.getByText('True'));
      
      // Navigate to last question and finish
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Finish Quiz'));

      await waitFor(() => {
        expect(mockOnQuizComplete).toHaveBeenCalled();
      });
    });

    it('should show answered questions in grid', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      // Answer first question
      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);

      // Question 1 button should have answered class
      const questionButtons = screen.getAllByRole('button');
      const question1Button = questionButtons.find(btn => btn.textContent === '1');
      expect(question1Button).toHaveClass('answered');
    });
  });

  describe('Timer', () => {
    it('should countdown timer', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={{ ...defaultConfig, timeLimit: 1 }} // 1 minute
        />
      );

      expect(screen.getByText(/1:00/)).toBeInTheDocument();

      act(() => {
        jest.advanceTimersByTime(30000); // 30 seconds
      });

      expect(screen.getByText(/0:30/)).toBeInTheDocument();
    });

    it('should show warning when time is low', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={{ ...defaultConfig, timeLimit: 1 }}
        />
      );

      act(() => {
        jest.advanceTimersByTime(30000); // 30 seconds remaining
      });

      expect(screen.getByText(/Time is running out!/)).toBeInTheDocument();
    });

    it('should auto-complete quiz when time runs out', async () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={{ ...defaultConfig, timeLimit: 1 }}
          onQuizComplete={mockOnQuizComplete}
        />
      );

      act(() => {
        jest.advanceTimersByTime(60000); // 1 minute
      });

      await waitFor(() => {
        expect(mockOnQuizComplete).toHaveBeenCalled();
      });
    });
  });

  describe('Progress Tracking', () => {
    it('should update progress bar as questions are answered', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      const progressBar = screen.getByRole('progressbar');
      expect(progressBar).toHaveAttribute('aria-valuenow', '0');

      // Answer first question
      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);

      expect(progressBar).toHaveAttribute('aria-valuenow', '33'); // 1/3 = 33%
    });

    it('should display answered count', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      expect(screen.getByText(/0 of 3 answered/)).toBeInTheDocument();

      // Answer first question
      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);

      expect(screen.getByText(/1 of 3 answered/)).toBeInTheDocument();
    });
  });

  describe('Quiz Completion', () => {
    it('should calculate results correctly', async () => {
      const onComplete = jest.fn();
      
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizComplete={onComplete}
        />
      );

      // Answer all questions
      fireEvent.click(screen.getByLabelText(/B\./)); // Correct
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('True')); // Correct
      fireEvent.click(screen.getByText('Next'));
      
      const textarea = screen.getByRole('textbox');
      fireEvent.change(textarea, { target: { value: 'Light energy process' } });
      
      fireEvent.click(screen.getByText('Finish Quiz'));

      await waitFor(() => {
        expect(onComplete).toHaveBeenCalled();
        const results: QuizResults = onComplete.mock.calls[0][0];
        
        expect(results.totalQuestions).toBe(3);
        expect(results.answeredQuestions).toBe(3);
        expect(results.questionResults).toHaveLength(3);
      });
    });

    it('should include unanswered questions in results', async () => {
      const onComplete = jest.fn();
      
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizComplete={onComplete}
        />
      );

      // Answer only first question
      fireEvent.click(screen.getByLabelText(/B\./));
      
      // Jump to last question and finish
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Finish Quiz'));

      await waitFor(() => {
        expect(onComplete).toHaveBeenCalled();
        const results: QuizResults = onComplete.mock.calls[0][0];
        
        expect(results.answeredQuestions).toBe(1);
        expect(results.totalQuestions).toBe(3);
      });
    });

    it('should track time spent', async () => {
      const onComplete = jest.fn();
      
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizComplete={onComplete}
        />
      );

      act(() => {
        jest.advanceTimersByTime(120000); // 2 minutes
      });

      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Finish Quiz'));

      await waitFor(() => {
        expect(onComplete).toHaveBeenCalled();
        const results: QuizResults = onComplete.mock.calls[0][0];
        
        expect(results.timeSpent).toBeGreaterThanOrEqual(120);
      });
    });
  });

  describe('Quiz Exit', () => {
    it('should call onQuizExit when exit button is clicked', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizExit={mockOnQuizExit}
        />
      );

      const exitButton = screen.getByText('Exit Quiz');
      fireEvent.click(exitButton);

      expect(mockOnQuizExit).toHaveBeenCalled();
    });

    it('should show confirmation dialog before exit', () => {
      const confirmSpy = jest.spyOn(window, 'confirm').mockReturnValue(false);
      
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
          onQuizExit={mockOnQuizExit}
        />
      );

      fireEvent.click(screen.getByText('Exit Quiz'));

      expect(confirmSpy).toHaveBeenCalled();
      expect(mockOnQuizExit).not.toHaveBeenCalled();

      confirmSpy.mockRestore();
    });
  });

  describe('Validation Display', () => {
    it('should show instant feedback when enabled', async () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={{ ...defaultConfig, showFeedback: true }}
        />
      );

      // Answer question
      fireEvent.click(screen.getByLabelText(/B\./));
      
      // Submit answer
      fireEvent.click(screen.getByText('Submit Answer'));

      await waitFor(() => {
        expect(screen.getByText(/Correct|Incorrect/)).toBeInTheDocument();
      });
    });

    it('should not show feedback when disabled', () => {
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={{ ...defaultConfig, showFeedback: false }}
        />
      );

      fireEvent.click(screen.getByLabelText(/B\./));
      fireEvent.click(screen.getByText('Submit Answer'));

      expect(screen.queryByText(/Correct|Incorrect/)).not.toBeInTheDocument();
    });
  });

  describe('Empty States', () => {
    it('should handle empty questions array', () => {
      render(
        <QuizInterface
          questions={[]}
          quizConfig={defaultConfig}
        />
      );

      expect(screen.getByText(/No questions available/)).toBeInTheDocument();
    });
  });

  describe('Responsive Behavior', () => {
    it('should render question grid on mobile', () => {
      // Mock mobile viewport
      global.innerWidth = 375;
      
      render(
        <QuizInterface
          questions={mockQuestions}
          quizConfig={defaultConfig}
        />
      );

      const questionGrid = screen.getByRole('navigation');
      expect(questionGrid).toBeInTheDocument();
    });
  });
});
