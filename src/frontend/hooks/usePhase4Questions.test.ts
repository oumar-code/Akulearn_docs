/**
 * Tests for usePhase4Questions Hook
 * 
 * Tests cover:
 * - Hook initialization
 * - API calls for question retrieval
 * - Answer validation
 * - Statistics fetching
 * - Error handling
 * - State management
 */

import { renderHook, act, waitFor } from '@testing-library/react';
import { usePhase4Questions } from './usePhase4Questions';

// Mock fetch globally
global.fetch = jest.fn();

describe('usePhase4Questions Hook', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    (global.fetch as jest.Mock).mockClear();
  });

  describe('Initialization', () => {
    it('should initialize with default state', () => {
      const { result } = renderHook(() => usePhase4Questions());

      expect(result.current.questions).toEqual([]);
      expect(result.current.currentQuestion).toBeNull();
      expect(result.current.stats).toBeNull();
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
    });

    it('should expose all API methods', () => {
      const { result } = renderHook(() => usePhase4Questions());

      expect(typeof result.current.fetchQuestionById).toBe('function');
      expect(typeof result.current.fetchQuestionsForLesson).toBe('function');
      expect(typeof result.current.fetchQuestionsBySubject).toBe('function');
      expect(typeof result.current.fetchQuestionsByType).toBe('function');
      expect(typeof result.current.fetchQuestionsByDifficulty).toBe('function');
      expect(typeof result.current.fetchRandomQuestions).toBe('function');
      expect(typeof result.current.fetchStats).toBe('function');
      expect(typeof result.current.fetchSubjectStats).toBe('function');
      expect(typeof result.current.generateQuiz).toBe('function');
      expect(typeof result.current.validateAnswer).toBe('function');
      expect(typeof result.current.validateAnswersBatch).toBe('function');
    });
  });

  describe('fetchQuestionById', () => {
    it('should fetch question by ID successfully', async () => {
      const mockQuestion = {
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

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockQuestion
      });

      const { result } = renderHook(() => usePhase4Questions());

      let question;
      await act(async () => {
        question = await result.current.fetchQuestionById(1);
      });

      expect(question).toEqual(mockQuestion);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v4/questions/1')
      );
    });

    it('should handle fetch errors', async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const { result } = renderHook(() => usePhase4Questions());

      await act(async () => {
        await expect(result.current.fetchQuestionById(1)).rejects.toThrow('Network error');
      });

      expect(result.current.error).toBe('Network error');
    });
  });

  describe('fetchRandomQuestions', () => {
    it('should fetch random questions with filters', async () => {
      const mockQuestions = [
        {
          id: 1,
          question_text: 'Question 1',
          question_type: 'multiple_choice',
          difficulty: 'medium',
          subject: 'Physics'
        },
        {
          id: 2,
          question_text: 'Question 2',
          question_type: 'true_false',
          difficulty: 'medium',
          subject: 'Physics'
        }
      ];

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockQuestions
      });

      const { result } = renderHook(() => usePhase4Questions());

      let questions;
      await act(async () => {
        questions = await result.current.fetchRandomQuestions(2, 'Physics', 'medium');
      });

      expect(questions).toEqual(mockQuestions);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/v4/questions/random?count=2&subject=Physics&difficulty=medium')
      );
    });
  });

  describe('validateAnswer', () => {
    it('should validate correct answer successfully', async () => {
      const mockValidation = {
        is_correct: true,
        points_earned: 10,
        points_possible: 10,
        feedback: 'Correct!',
        explanation: 'Well done'
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockValidation
      });

      const { result } = renderHook(() => usePhase4Questions());

      let validation;
      await act(async () => {
        validation = await result.current.validateAnswer(1, 'A');
      });

      expect(validation).toEqual(mockValidation);
      expect(validation.is_correct).toBe(true);
      expect(validation.points_earned).toBe(10);
    });

    it('should validate incorrect answer', async () => {
      const mockValidation = {
        is_correct: false,
        points_earned: 0,
        points_possible: 10,
        feedback: 'Incorrect',
        correct_answer: 'B',
        explanation: 'The correct answer is B'
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockValidation
      });

      const { result } = renderHook(() => usePhase4Questions());

      let validation;
      await act(async () => {
        validation = await result.current.validateAnswer(1, 'A');
      });

      expect(validation).toEqual(mockValidation);
      expect(validation.is_correct).toBe(false);
      expect(validation.points_earned).toBe(0);
    });
  });

  describe('validateAnswersBatch', () => {
    it('should validate multiple answers at once', async () => {
      const mockValidations = [
        { is_correct: true, points_earned: 10, points_possible: 10 },
        { is_correct: false, points_earned: 0, points_possible: 5 }
      ];

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockValidations
      });

      const { result } = renderHook(() => usePhase4Questions());

      const submissions = [
        { questionId: 1, userAnswer: 'A' },
        { questionId: 2, userAnswer: 'false' }
      ];

      let validations;
      await act(async () => {
        validations = await result.current.validateAnswersBatch(submissions);
      });

      expect(validations).toEqual(mockValidations);
      expect(validations.length).toBe(2);
    });
  });

  describe('fetchStats', () => {
    it('should fetch overall statistics', async () => {
      const mockStats = {
        total_questions: 150,
        questions_by_type: {
          multiple_choice: 60,
          true_false: 30,
          fill_blank: 25,
          matching: 20,
          short_answer: 15
        },
        questions_by_difficulty: {
          easy: 62,
          medium: 62,
          hard: 26
        },
        total_points: 1250,
        avg_points_per_question: 8.3
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockStats
      });

      const { result } = renderHook(() => usePhase4Questions());

      let stats;
      await act(async () => {
        stats = await result.current.fetchStats();
      });

      expect(stats).toEqual(mockStats);
      expect(stats.total_questions).toBe(150);
    });
  });

  describe('generateQuiz', () => {
    it('should generate quiz with custom options', async () => {
      const mockQuiz = {
        id: 'quiz-123',
        questions: [
          { id: 1, question_text: 'Q1' },
          { id: 2, question_text: 'Q2' }
        ],
        total_points: 20,
        estimated_time_seconds: 240
      };

      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockQuiz
      });

      const { result } = renderHook(() => usePhase4Questions());

      const options = {
        count: 2,
        subject: 'Mathematics',
        difficulty: 'medium'
      };

      let quiz;
      await act(async () => {
        quiz = await result.current.generateQuiz(options);
      });

      expect(quiz).toEqual(mockQuiz);
      expect(quiz.questions.length).toBe(2);
    });
  });

  describe('Error Handling', () => {
    it('should handle network errors gracefully', async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      const { result } = renderHook(() => usePhase4Questions());

      await act(async () => {
        await expect(result.current.fetchStats()).rejects.toThrow('Network error');
      });

      expect(result.current.error).toBe('Network error');
    });

    it('should handle HTTP errors', async () => {
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Not found' })
      });

      const { result } = renderHook(() => usePhase4Questions());

      await act(async () => {
        await expect(result.current.fetchQuestionById(999)).rejects.toThrow();
      });
    });
  });

  describe('State Management', () => {
    it('should update loading state during fetch', async () => {
      (global.fetch as jest.Mock).mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ id: 1 })
        }), 100))
      );

      const { result } = renderHook(() => usePhase4Questions());

      act(() => {
        result.current.fetchQuestionById(1);
      });

      // Loading should be true during fetch
      await waitFor(() => {
        expect(result.current.loading).toBe(true);
      });
    });

    it('should clear error on successful fetch', async () => {
      const { result } = renderHook(() => usePhase4Questions());

      // First call fails
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Error'));
      await act(async () => {
        await expect(result.current.fetchStats()).rejects.toThrow();
      });
      expect(result.current.error).toBe('Error');

      // Second call succeeds
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ total_questions: 150 })
      });
      await act(async () => {
        await result.current.fetchStats();
      });
      expect(result.current.error).toBeNull();
    });
  });
});
