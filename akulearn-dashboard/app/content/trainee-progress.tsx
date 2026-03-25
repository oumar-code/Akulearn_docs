"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";

export default function TraineeProgressTracker() {
  type Progress = { id: string; trainee_name?: string; course?: string; completion?: number };
  const [progress, setProgress] = useState<Progress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProgress = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("trainee_progress").select("*");
        if (error) throw error;
        setProgress(data || []);
      } catch {
        setError("Unable to fetch trainee progress.");
      }
      setLoading(false);
    };
    fetchProgress();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Trainee Progress Tracker</h3>
      {loading && <div>Loading progress...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {progress.map(p => (
            <li key={p.id}>{p.trainee_name} — {p.course}: {p.completion ?? 0}%</li>
          ))}
          {progress.length === 0 && <li>No progress data found.</li>}
        </ul>
      )}
    </div>
  );
}
