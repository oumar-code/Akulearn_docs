"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function QuizTopicManagement() {
  type Topic = { id: string; name: string; subject?: string };
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTopics = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("quiz_topics").select("*");
        if (error) throw error;
        setTopics(data || []);
      } catch {
        setError("Unable to fetch quiz topics.");
      }
      setLoading(false);
    };
    fetchTopics();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Quiz &amp; Topic Management</h3>
      {loading && <div>Loading topics...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {topics.map(t => (
            <li key={t.id}>{t.name} {t.subject ? `(${t.subject})` : ""}</li>
          ))}
          {topics.length === 0 && <li>No topics found.</li>}
        </ul>
      )}
    </div>
  );
}
