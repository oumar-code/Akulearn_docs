/**
 * Custom hook for fetching and managing Phase 3 specialized diagrams
 * Supports Venn diagrams, flowcharts, timelines, circuits, and chemistry
 */

import { useState, useEffect, useCallback } from 'react';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

export interface DiagramInfo {
  id: string;
  title: string;
  type: string;
  path: string;
  subject: string;
}

export interface DiagramsByType {
  venn_diagrams: DiagramInfo[];
  flowcharts: DiagramInfo[];
  timelines: DiagramInfo[];
  electrical_circuits: DiagramInfo[];
  logic_circuits: DiagramInfo[];
  molecular_structures: DiagramInfo[];
  chemical_reactions: DiagramInfo[];
}

export interface DiagramContent {
  id: string;
  title: string;
  type: string;
  svg: string;
}

export interface Phase3Stats {
  total_diagrams: number;
  venn_diagrams: number;
  flowcharts: number;
  timelines: number;
  electrical_circuits: number;
  logic_circuits: number;
  molecular_structures: number;
  chemical_reactions: number;
  generated_at?: string;
}

interface UsePhase3DiagramsOptions {
  apiBaseUrl?: string;
  autoFetch?: boolean;
  onError?: (error: Error) => void;
}

interface UsePhase3DiagramsReturn {
  diagrams: DiagramsByType | null;
  stats: Phase3Stats | null;
  loading: boolean;
  error: Error | null;
  fetchDiagramsForLesson: (lessonId: string) => Promise<void>;
  fetchDiagramContent: (diagramId: string) => Promise<DiagramContent | null>;
  fetchStats: () => Promise<void>;
  fetchDiagramsByType: (type: string, lessonId?: string) => Promise<DiagramInfo[]>;
}

// ============================================================================
// HOOK IMPLEMENTATION
// ============================================================================

export const usePhase3Diagrams = (
  lessonId?: string,
  options: UsePhase3DiagramsOptions = {}
): UsePhase3DiagramsReturn => {
  const {
    apiBaseUrl = '/api/assets/phase3',
    autoFetch = true,
    onError
  } = options;

  const [diagrams, setDiagrams] = useState<DiagramsByType | null>(null);
  const [stats, setStats] = useState<Phase3Stats | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  // Fetch diagrams for a specific lesson
  const fetchDiagramsForLesson = useCallback(async (targetLessonId: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBaseUrl}/lesson/${targetLessonId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          // No diagrams found - not an error, just empty
          setDiagrams({
            venn_diagrams: [],
            flowcharts: [],
            timelines: [],
            electrical_circuits: [],
            logic_circuits: [],
            molecular_structures: [],
            chemical_reactions: []
          });
          return;
        }
        throw new Error(`Failed to fetch diagrams: ${response.statusText}`);
      }

      const data: DiagramsByType = await response.json();
      setDiagrams(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      if (onError) onError(error);
    } finally {
      setLoading(false);
    }
  }, [apiBaseUrl, onError]);

  // Fetch SVG content for a specific diagram
  const fetchDiagramContent = useCallback(async (diagramId: string): Promise<DiagramContent | null> => {
    try {
      const response = await fetch(`${apiBaseUrl}/diagram/${diagramId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch diagram content: ${response.statusText}`);
      }

      const data: DiagramContent = await response.json();
      return data;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      if (onError) onError(error);
      return null;
    }
  }, [apiBaseUrl, onError]);

  // Fetch Phase 3 statistics
  const fetchStats = useCallback(async () => {
    try {
      const response = await fetch(`${apiBaseUrl}/summary`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch stats: ${response.statusText}`);
      }

      const data: Phase3Stats = await response.json();
      setStats(data);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      if (onError) onError(error);
    }
  }, [apiBaseUrl, onError]);

  // Fetch diagrams by type
  const fetchDiagramsByType = useCallback(async (
    type: string,
    targetLessonId?: string
  ): Promise<DiagramInfo[]> => {
    try {
      const url = targetLessonId 
        ? `${apiBaseUrl}/type/${type}?lesson_id=${targetLessonId}`
        : `${apiBaseUrl}/type/${type}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        if (response.status === 404) return [];
        throw new Error(`Failed to fetch diagrams by type: ${response.statusText}`);
      }

      const data = await response.json();
      return data.diagrams || [];
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      if (onError) onError(error);
      return [];
    }
  }, [apiBaseUrl, onError]);

  // Auto-fetch on mount if lessonId provided
  useEffect(() => {
    if (autoFetch && lessonId) {
      fetchDiagramsForLesson(lessonId);
    }
  }, [lessonId, autoFetch, fetchDiagramsForLesson]);

  return {
    diagrams,
    stats,
    loading,
    error,
    fetchDiagramsForLesson,
    fetchDiagramContent,
    fetchStats,
    fetchDiagramsByType
  };
};

// ============================================================================
// UTILITY HOOKS
// ============================================================================

/**
 * Hook for fetching a single diagram's content
 */
export const useDiagramContent = (diagramId?: string) => {
  const [content, setContent] = useState<DiagramContent | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!diagramId) return;

    const fetchContent = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`/api/assets/phase3/diagram/${diagramId}`);
        if (!response.ok) throw new Error('Failed to fetch diagram');
        const data = await response.json();
        setContent(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, [diagramId]);

  return { content, loading, error };
};

/**
 * Hook for Phase 3 statistics only
 */
export const usePhase3Stats = () => {
  const [stats, setStats] = useState<Phase3Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/assets/phase3/summary');
        if (!response.ok) throw new Error('Failed to fetch stats');
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return { stats, loading, error };
};
