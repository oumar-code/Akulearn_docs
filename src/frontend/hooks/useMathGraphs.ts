/**
 * Hook: useMathGraphs
 * 
 * Loads generated Phase 2 mathematical graphs for lessons
 * 
 * Usage:
 * const { graphs, loading, error } = useMathGraphs(lessonId);
 */

import { useState, useEffect, useCallback } from 'react';

export interface MathGraphAsset {
  lesson_id: string;
  title: string;
  subject: string;
  type?: string;
  path: string;
  content?: string;
}

export interface MathGraphsData {
  function_graphs: MathGraphAsset[];
  bar_charts: MathGraphAsset[];
  pie_charts: MathGraphAsset[];
  line_charts: MathGraphAsset[];
  [key: string]: MathGraphAsset[];
}

interface UseMathGraphsOptions {
  autoLoad?: boolean;
  onError?: (error: string) => void;
  apiBaseUrl?: string;
}

const useMathGraphs = (
  lessonId: string | undefined,
  options: UseMathGraphsOptions = {}
) => {
  const {
    autoLoad = true,
    onError,
    apiBaseUrl = '/api/assets'
  } = options;

  const [graphs, setGraphs] = useState<MathGraphsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadGraphs = useCallback(async () => {
    if (!lessonId) {
      setGraphs(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Try to get Phase 2 graphs
      const response = await fetch(`${apiBaseUrl}/graphs/lesson/${lessonId}`);

      if (response.status === 404) {
        // No graphs found, but not an error
        setGraphs(null);
        return;
      }

      if (!response.ok) {
        throw new Error(`Failed to load graphs: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Load SVG content for each graph
      const enrichedGraphs: MathGraphsData = {
        function_graphs: [],
        bar_charts: [],
        pie_charts: [],
        line_charts: []
      };

      for (const graphType in data) {
        if (Array.isArray(data[graphType])) {
          enrichedGraphs[graphType] = await Promise.all(
            data[graphType].map(async (graph: MathGraphAsset) => {
              try {
                const svgResponse = await fetch(graph.path);
                const svgContent = await svgResponse.text();
                return { ...graph, content: svgContent };
              } catch {
                return graph;
              }
            })
          );
        }
      }

      setGraphs(enrichedGraphs);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMsg);
      if (onError) {
        onError(errorMsg);
      }
    } finally {
      setLoading(false);
    }
  }, [lessonId, apiBaseUrl, onError]);

  useEffect(() => {
    if (autoLoad) {
      loadGraphs();
    }
  }, [loadGraphs, autoLoad]);

  const hasGraphs = graphs && (
    (graphs.function_graphs?.length ?? 0) > 0 ||
    (graphs.bar_charts?.length ?? 0) > 0 ||
    (graphs.pie_charts?.length ?? 0) > 0 ||
    (graphs.line_charts?.length ?? 0) > 0
  );

  const getAllGraphs = (): MathGraphAsset[] => {
    if (!graphs) return [];
    return [
      ...(graphs.function_graphs || []),
      ...(graphs.bar_charts || []),
      ...(graphs.pie_charts || []),
      ...(graphs.line_charts || [])
    ];
  };

  return {
    graphs,
    loading,
    error,
    reload: loadGraphs,
    hasGraphs,
    getAllGraphs,
    graphCount: getAllGraphs().length
  };
};

export default useMathGraphs;
