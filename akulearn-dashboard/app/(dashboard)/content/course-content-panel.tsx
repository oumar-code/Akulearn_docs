"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function CourseContentPanel() {
  type Content = { id: string; title: string; type?: string; course_id?: string };
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchContent = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("course_content").select("*");
        if (error) throw error;
        setContent(data || []);
      } catch {
        setError("Unable to fetch course content.");
      }
      setLoading(false);
    };
    fetchContent();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Course Content Panel</h3>
      {loading && <div>Loading content...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {content.map(c => (
            <li key={c.id}>{c.title} {c.type ? `[${c.type}]` : ""}</li>
          ))}
          {content.length === 0 && <li>No content found.</li>}
        </ul>
      )}
    </div>
  );
}
