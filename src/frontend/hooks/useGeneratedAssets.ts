/**
 * Hook: useGeneratedAssets
 * 
 * Loads generated Phase 1 assets (ASCII diagrams, truth tables) for lessons
 * 
 * Usage:
 * const { assets, loading, error, reload } = useGeneratedAssets(lessonId);
 */

import { useState, useEffect, useCallback } from 'react';

export interface GeneratedAsset {
  type: string;
  content: string;
  format: string;
}

export interface GeneratedAssets {
  lesson_id: string;
  ascii_diagram?: GeneratedAsset;
  truth_table?: GeneratedAsset;
}

interface UseGeneratedAssetsOptions {
  autoLoad?: boolean;
  onError?: (error: string) => void;
  apiBaseUrl?: string;
}

const useGeneratedAssets = (
  lessonId: string | undefined,
  options: UseGeneratedAssetsOptions = {}
) => {
  const {
    autoLoad = true,
    onError,
    apiBaseUrl = '/api/assets'
  } = options;

  const [assets, setAssets] = useState<GeneratedAssets | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadAssets = useCallback(async () => {
    if (!lessonId) {
      setAssets(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBaseUrl}/lesson/${lessonId}`);

      if (response.status === 404) {
        // No assets found, but not an error
        setAssets(null);
        return;
      }

      if (!response.ok) {
        throw new Error(`Failed to load assets: ${response.statusText}`);
      }

      const data = await response.json();
      setAssets(data);
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
      loadAssets();
    }
  }, [loadAssets, autoLoad]);

  return {
    assets,
    loading,
    error,
    reload: loadAssets,
    hasAssets: !!assets && (!!assets.ascii_diagram || !!assets.truth_table),
    hasASCII: !!assets?.ascii_diagram,
    hasTruthTable: !!assets?.truth_table
  };
};

export default useGeneratedAssets;
