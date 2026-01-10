/**
 * Tests for QuestionViewer Component
 * 
 * Tests cover:
 * - Rendering different question types
 * - User interaction (answer selection)
 * - Answer submission
 * - Validation feedback display
 * - Visual states (correct/incorrect)
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import QuestionViewer from './QuestionViewer';
import type { QuestionDetail, AnswerValidation } from '../hooks/usePhase4Questions';

describe('QuestionViewer Component', () => {
  const mockOnAnswerSubmit = jest.fn();
  const mockOnValidationResult = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Multiple Choice Questions', () => {
    const multipleChoiceQuestion: QuestionDetail = {
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
    };

    it('should render multiple choice question with options', () => {
      render(<QuestionViewer question={multipleChoiceQuestion} />);

      expect(screen.getByText('What is 2+2?')).toBeInTheDocument();
      expect(screen.getByText(/A\./)).toBeInTheDocument();
      expect(screen.getByText(/B\./)).toBeInTheDocument();
      expect(screen.getByText(/C\./)).toBeInTheDocument();
      expect(screen.getByText(/D\./)).toBeInTheDocument();
    });

    it('should allow selecting an option', () => {
      render(<QuestionViewer question={multipleChoiceQuestion} />);

      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);

      expect(optionB).toBeChecked();
    });

    it('should call onAnswerSubmit when answer is submitted', () => {
      render(
        <QuestionViewer 
          question={multipleChoiceQuestion}
          onAnswerSubmit={mockOnAnswerSubmit}
        />
      );

      // Select option B
      const optionB = screen.getByLabelText(/B\./);
      fireEvent.click(optionB);

      // Submit answer
      const submitButton = screen.getByText('Submit Answer');
      fireEvent.click(submitButton);

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith('B');
    });

    it('should display validation feedback for correct answer', () => {
      const correctValidation: AnswerValidation = {
        is_correct: true,
        points_earned: 5,
        points_possible: 5,
        feedback: 'Correct!',
        explanation: '2+2 equals 4'
      };

      const { rerender } = render(
        <QuestionViewer question={multipleChoiceQuestion} />
      );

      rerender(
        <QuestionViewer 
          question={multipleChoiceQuestion}
          validation={correctValidation}
          showFeedback={true}
        />
      );

      expect(screen.getByText('Correct!')).toBeInTheDocument();
      expect(screen.getByText(/5 \/ 5 points/)).toBeInTheDocument();
    });

    it('should display validation feedback for incorrect answer', () => {
      const incorrectValidation: AnswerValidation = {
        is_correct: false,
        points_earned: 0,
        points_possible: 5,
        feedback: 'Incorrect',
        correct_answer: 'B',
        explanation: '2+2 equals 4'
      };

      render(
        <QuestionViewer 
          question={multipleChoiceQuestion}
          validation={incorrectValidation}
          showFeedback={true}
        />
      );

      expect(screen.getByText('Incorrect')).toBeInTheDocument();
      expect(screen.getByText(/0 \/ 5 points/)).toBeInTheDocument();
    });
  });

  describe('True/False Questions', () => {
    const trueFalseQuestion: QuestionDetail = {
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
        explanation: 'Water is indeed H2O'
      }
    };

    it('should render true/false question with options', () => {
      render(<QuestionViewer question={trueFalseQuestion} />);

      expect(screen.getByText('Is water H2O?')).toBeInTheDocument();
      expect(screen.getByText('True')).toBeInTheDocument();
      expect(screen.getByText('False')).toBeInTheDocument();
    });

    it('should allow selecting true or false', () => {
      render(<QuestionViewer question={trueFalseQuestion} />);

      const trueButton = screen.getByText('True');
      fireEvent.click(trueButton);

      // Check if the button has the selected class or style
      expect(trueButton.closest('button')).toHaveClass('selected');
    });

    it('should submit boolean answer', () => {
      render(
        <QuestionViewer 
          question={trueFalseQuestion}
          onAnswerSubmit={mockOnAnswerSubmit}
        />
      );

      fireEvent.click(screen.getByText('True'));
      fireEvent.click(screen.getByText('Submit Answer'));

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith(true);
    });
  });

  describe('Fill-in-Blank Questions', () => {
    const fillBlankQuestion: QuestionDetail = {
      id: 3,
      question_text: 'Fill in the blanks',
      question_type: 'fill_blank',
      difficulty: 'medium',
      subject: 'English',
      topic: 'Grammar',
      points: 10,
      estimated_time_seconds: 120,
      question_data: {
        text_with_blanks: 'The capital of Nigeria is ___.',
        blanks: ['Abuja'],
        explanation: 'Abuja is the capital'
      }
    };

    it('should render fill-in-blank question with input', () => {
      render(<QuestionViewer question={fillBlankQuestion} />);

      expect(screen.getByText(/The capital of Nigeria is/)).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/blank/i)).toBeInTheDocument();
    });

    it('should allow typing in blank', () => {
      render(<QuestionViewer question={fillBlankQuestion} />);

      const input = screen.getByPlaceholderText(/blank/i);
      fireEvent.change(input, { target: { value: 'Abuja' } });

      expect(input).toHaveValue('Abuja');
    });

    it('should submit array of answers', () => {
      render(
        <QuestionViewer 
          question={fillBlankQuestion}
          onAnswerSubmit={mockOnAnswerSubmit}
        />
      );

      const input = screen.getByPlaceholderText(/blank/i);
      fireEvent.change(input, { target: { value: 'Abuja' } });
      fireEvent.click(screen.getByText('Submit Answer'));

      expect(mockOnAnswerSubmit).toHaveBeenCalledWith(['Abuja']);
    });
  });

  describe('Matching Questions', () => {
    const matchingQuestion: QuestionDetail = {
      id: 4,
      question_text: 'Match elements with symbols',
      question_type: 'matching',
      difficulty: 'medium',
      subject: 'Chemistry',
      topic: 'Elements',
      points: 15,
      estimated_time_seconds: 180,
      question_data: {
        column_a: ['Hydrogen', 'Oxygen', 'Carbon'],
        column_b: ['C', 'O', 'H'],
        correct_pairs: { 'Hydrogen': 'H', 'Oxygen': 'O', 'Carbon': 'C' },
        explanation: 'Standard chemical symbols'
      }
    };

    it('should render matching question with dropdowns', () => {
      render(<QuestionViewer question={matchingQuestion} />);

      expect(screen.getByText('Match elements with symbols')).toBeInTheDocument();
      expect(screen.getByText('Hydrogen')).toBeInTheDocument();
      expect(screen.getByText('Oxygen')).toBeInTheDocument();
      expect(screen.getByText('Carbon')).toBeInTheDocument();
    });

    it('should allow selecting matches', () => {
      render(<QuestionViewer question={matchingQuestion} />);

      const selects = screen.getAllByRole('combobox');
      expect(selects).toHaveLength(3);

      fireEvent.change(selects[0], { target: { value: 'H' } });
      expect(selects[0]).toHaveValue('H');
    });
  });

  describe('Short Answer Questions', () => {
    const shortAnswerQuestion: QuestionDetail = {
      id: 5,
      question_text: 'Explain photosynthesis',
      question_type: 'short_answer',
      difficulty: 'hard',
      subject: 'Biology',
      topic: 'Plant Biology',
      points: 20,
      estimated_time_seconds: 300,
      question_data: {
        expected_keywords: ['light', 'chlorophyll', 'glucose'],
        sample_answer: 'Photosynthesis is the process...',
        explanation: 'Key concepts include light energy conversion'
      }
    };

    it('should render short answer question with textarea', () => {
      render(<QuestionViewer question={shortAnswerQuestion} />);

      expect(screen.getByText('Explain photosynthesis')).toBeInTheDocument();
      expect(screen.getByRole('textbox')).toBeInTheDocument();
    });

    it('should allow typing long answer', () => {
      render(<QuestionViewer question={shortAnswerQuestion} />);

      const textarea = screen.getByRole('textbox');
      const answer = 'Photosynthesis uses light energy...';
      fireEvent.change(textarea, { target: { value: answer } });

      expect(textarea).toHaveValue(answer);
    });
  });

  describe('Difficulty Badges', () => {
    it('should display easy difficulty badge', () => {
      const easyQuestion: QuestionDetail = {
        id: 1,
        question_text: 'Easy question',
        question_type: 'multiple_choice',
        difficulty: 'easy',
        subject: 'Math',
        topic: 'Basic',
        points: 5,
        estimated_time_seconds: 60,
        question_data: { options: [], correct_answer: 'A', explanation: '' }
      };

      render(<QuestionViewer question={easyQuestion} />);
      expect(screen.getByText('Easy')).toBeInTheDocument();
    });

    it('should display medium difficulty badge', () => {
      const mediumQuestion: QuestionDetail = {
        id: 1,
        question_text: 'Medium question',
        question_type: 'multiple_choice',
        difficulty: 'medium',
        subject: 'Math',
        topic: 'Intermediate',
        points: 10,
        estimated_time_seconds: 120,
        question_data: { options: [], correct_answer: 'A', explanation: '' }
      };

      render(<QuestionViewer question={mediumQuestion} />);
      expect(screen.getByText('Medium')).toBeInTheDocument();
    });

    it('should display hard difficulty badge', () => {
      const hardQuestion: QuestionDetail = {
        id: 1,
        question_text: 'Hard question',
        question_type: 'multiple_choice',
        difficulty: 'hard',
        subject: 'Math',
        topic: 'Advanced',
        points: 20,
        estimated_time_seconds: 300,
        question_data: { options: [], correct_answer: 'A', explanation: '' }
      };

      render(<QuestionViewer question={hardQuestion} />);
      expect(screen.getByText('Hard')).toBeInTheDocument();
    });
  });

  describe('Disabled State', () => {
    const question: QuestionDetail = {
      id: 1,
      question_text: 'Test question',
      question_type: 'multiple_choice',
      difficulty: 'easy',
      subject: 'Math',
      topic: 'Test',
      points: 5,
      estimated_time_seconds: 60,
      question_data: {
        options: ['A', 'B', 'C', 'D'],
        correct_answer: 'A',
        explanation: 'Test'
      }
    };

    it('should disable inputs when disabled prop is true', () => {
      render(<QuestionViewer question={question} disabled={true} />);

      const submitButton = screen.getByText('Submit Answer');
      expect(submitButton).toBeDisabled();
    });
  });

  describe('Metadata Display', () => {
    const question: QuestionDetail = {
      id: 1,
      question_text: 'Test question',
      question_type: 'multiple_choice',
      difficulty: 'medium',
      subject: 'Mathematics',
      topic: 'Algebra',
      points: 10,
      estimated_time_seconds: 120,
      question_data: {
        options: ['A', 'B'],
        correct_answer: 'A',
        explanation: 'Test'
      }
    };

    it('should display subject and topic', () => {
      render(<QuestionViewer question={question} />);

      expect(screen.getByText('Mathematics')).toBeInTheDocument();
      expect(screen.getByText('Algebra')).toBeInTheDocument();
    });

    it('should display points', () => {
      render(<QuestionViewer question={question} />);

      expect(screen.getByText(/10 points/)).toBeInTheDocument();
    });

    it('should display estimated time', () => {
      render(<QuestionViewer question={question} />);

      expect(screen.getByText(/2 min/)).toBeInTheDocument();
    });
  });
});
