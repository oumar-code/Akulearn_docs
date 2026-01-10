/**
 * Custom hook for fetching and managing Phase 4 practice questions
 * Supports question retrieval, answer validation, and quiz generation
 */

import { useState, useEffect, useCallback } from 'react';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface QuestionInfo {
  id: string;
  subject: string;
  topic: string;
  grade: string;
  question_type: 'multiple_choice' | 'true_false' | 'fill_blank' | 'matching' | 'short_answer';
  difficulty: 'easy' | 'medium' | 'hard';
  points: number;
  estimated_time: number;
  tags: string[];
}

export interface QuestionDetail extends QuestionInfo {
  question_data: {
    // Multiple Choice
    question_text?: string;
    options?: string[];
    correct_answer?: number | boolean | string | Record<string, number>;
    
    // True/False
    statement?: string;
    
    // Fill-in-Blank
    sentence?: string;
    alternative_answers?: string[];
    
    // Matching
    instruction?: string;
    column_a?: string[];
    column_b?: string[];
    correct_pairs?: Record<number, number>;
    
    // Short Answer
    sample_answer?: string;
    marking_criteria?: string[];
    
    // Common
    explanation: string;
  };
}

export interface AnswerValidation {
  valid: boolean;
  correct?: boolean;
  user_answer?: any;
  correct_answer?: any;
  explanation?: string;
  points_earned?: number;
  points_possible?: number;
  error?: string;
  requires_manual_grading?: boolean;
  sample_answer?: string;
  marking_criteria?: string[];
  correct_count?: number;
  total_pairs?: number;
  note?: string;
}

export interface Phase4Stats {
  total_questions: number;
  question_types: number;
  subjects: number;
  total_points: number;
  total_time_minutes: number;
  type_breakdown: Record<string, number>;
  difficulty_breakdown: Record<string, number>;
  subject_breakdown: Record<string, number>;
  generated_at?: string;
}

export interface SubjectStats {
  subject: string;
  total_questions: number;
  total_points?: number;
  total_time_minutes?: number;
  type_breakdown?: Record<string, number>;
  difficulty_breakdown?: Record<string, number>;
  error?: string;
}

interface UsePhase4QuestionsOptions {
  apiBaseUrl?: string;
  autoFetch?: boolean;
  onError?: (error: Error) => void;
}

interface UsePhase4QuestionsReturn {
  questions: QuestionDetail[] | null;
  currentQuestion: QuestionDetail | null;
  stats: Phase4Stats | null;
  loading: boolean;
  error: Error | null;
  
  // Fetching methods
  fetchQuestionById: (questionId: string) => Promise<QuestionDetail | null>;
  fetchQuestionsForLesson: (lessonId: string, limit?: number) => Promise<void>;
  fetchQuestionsBySubject: (subject: string, limit?: number) => Promise<void>;
  fetchQuestionsByType: (questionType: string, limit?: number) => Promise<void>;
  fetchQuestionsByDifficulty: (difficulty: string, limit?: number) => Promise<void>;
  fetchRandomQuestions: (count: number, subject?: string, difficulty?: string) => Promise<void>;
  fetchStats: () => Promise<void>;
  fetchSubjectStats: (subject: string) => Promise<SubjectStats | null>;
  
  // Quiz generation
  generateQuiz: (options: QuizGenerationOptions) => Promise<void>;
  
  // Answer validation
  validateAnswer: (questionId: string, userAnswer: any) => Promise<AnswerValidation | null>;
  validateAnswersBatch: (submissions: Array<{question_id: string, user_answer: any}>) => Promise<AnswerValidation[]>;
}

export interface QuizGenerationOptions {
  subject?: string;
  difficulty?: string;
  question_count?: number;
  include_types?: string[];
}

// ============================================================================
// HOOK IMPLEMENTATION
// ============================================================================

export const usePhase4Questions = (
  options: UsePhase4QuestionsOptions = {}
): UsePhase4QuestionsReturn => {
  const {
    apiBaseUrl = '/api/assets/phase4',
    autoFetch = false,
    onError
  } = options;

  const [questions, setQuestions] = useState<QuestionDetail[] | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<QuestionDetail | null>(null);
  const [stats, setStats] = useState<Phase4Stats | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  // Helper to handle fetch errors
  const handleError = useCallback((err: Error) => {
    setError(err);
    if (onError) {
      onError(err);
    }
  }, [onError]);

  // Fetch question by ID
  const fetchQuestionById = useCallback(async (questionId: string): Promise<QuestionDetail | null> => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${apiBaseUrl}/question/${questionId}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch question: ${response.statusText}`);
      }
      
      const data: QuestionDetail = await response.json();
      setCurrentQuestion(data);
      return data;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
      return null;
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch questions for lesson
  const fetchQuestionsForLesson = useCallback(async (lessonId: string, limit?: number) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/questions/lesson/${lessonId}`, window.location.origin);
      if (limit) url.searchParams.append('limit', limit.toString());
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch questions: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch questions by subject
  const fetchQuestionsBySubject = useCallback(async (subject: string, limit?: number) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/questions/subject/${subject}`, window.location.origin);
      if (limit) url.searchParams.append('limit', limit.toString());
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch questions: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch questions by type
  const fetchQuestionsByType = useCallback(async (questionType: string, limit: number = 10) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/questions/type/${questionType}`, window.location.origin);
      url.searchParams.append('limit', limit.toString());
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch questions: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch questions by difficulty
  const fetchQuestionsByDifficulty = useCallback(async (difficulty: string, limit?: number) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/questions/difficulty/${difficulty}`, window.location.origin);
      if (limit) url.searchParams.append('limit', limit.toString());
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch questions: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch random questions
  const fetchRandomQuestions = useCallback(async (
    count: number,
    subject?: string,
    difficulty?: string
  ) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/questions/random`, window.location.origin);
      url.searchParams.append('count', count.toString());
      if (subject) url.searchParams.append('subject', subject);
      if (difficulty) url.searchParams.append('difficulty', difficulty);
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to fetch questions: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch statistics
  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`${apiBaseUrl}/summary`);
      if (!response.ok) {
        throw new Error(`Failed to fetch stats: ${response.statusText}`);
      }
      
      const data: Phase4Stats = await response.json();
      setStats(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Fetch subject statistics
  const fetchSubjectStats = useCallback(async (subject: string): Promise<SubjectStats | null> => {
    try {
      const response = await fetch(`${apiBaseUrl}/stats/subject/${subject}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch subject stats: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
      return null;
    }
  }, [apiBaseUrl, handleError]);

  // Generate quiz
  const generateQuiz = useCallback(async (options: QuizGenerationOptions) => {
    try {
      setLoading(true);
      setError(null);
      
      const url = new URL(`${apiBaseUrl}/quiz/generate`, window.location.origin);
      if (options.subject) url.searchParams.append('subject', options.subject);
      if (options.difficulty) url.searchParams.append('difficulty', options.difficulty);
      if (options.question_count) url.searchParams.append('question_count', options.question_count.toString());
      if (options.include_types) url.searchParams.append('include_types', options.include_types.join(','));
      
      const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`Failed to generate quiz: ${response.statusText}`);
      }
      
      const data: QuestionDetail[] = await response.json();
      setQuestions(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, handleError]);

  // Validate answer
  const validateAnswer = useCallback(async (
    questionId: string,
    userAnswer: any
  ): Promise<AnswerValidation | null> => {
    try {
      const response = await fetch(`${apiBaseUrl}/validate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question_id: questionId,
          user_answer: userAnswer
        })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to validate answer: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
      return null;
    }
  }, [apiBaseUrl, handleError]);

  // Validate answers batch
  const validateAnswersBatch = useCallback(async (
    submissions: Array<{question_id: string, user_answer: any}>
  ): Promise<AnswerValidation[]> => {
    try {
      const response = await fetch(`${apiBaseUrl}/validate/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submissions)
      });
      
      if (!response.ok) {
        throw new Error(`Failed to validate answers: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      handleError(error);
      return [];
    }
  }, [apiBaseUrl, handleError]);

  // Auto-fetch stats if enabled
  useEffect(() => {
    if (autoFetch) {
      fetchStats();
    }
  }, [autoFetch, fetchStats]);

  return {
    questions,
    currentQuestion,
    stats,
    loading,
    error,
    fetchQuestionById,
    fetchQuestionsForLesson,
    fetchQuestionsBySubject,
    fetchQuestionsByType,
    fetchQuestionsByDifficulty,
    fetchRandomQuestions,
    fetchStats,
    fetchSubjectStats,
    generateQuiz,
    validateAnswer,
    validateAnswersBatch
  };
};

export default usePhase4Questions;
