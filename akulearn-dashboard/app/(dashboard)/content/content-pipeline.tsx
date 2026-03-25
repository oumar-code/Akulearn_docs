"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function ContentPipelinePanel() {
  type ContentItem = { id: string; title: string; status?: string; submitted_by?: string };
  const [items, setItems] = useState<ContentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPipeline = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase
          .from("content_pipeline")
          .select("*")
          .order("created_at", { ascending: false });
        if (error) throw error;
        setItems(data || []);
      } catch {
        setError("Unable to fetch content pipeline.");
      }
      setLoading(false);
    };
    fetchPipeline();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Content Pipeline</h3>
      {loading && <div>Loading pipeline...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {items.map(item => (
            <li key={item.id}><b>{item.title}</b> — {item.status || "pending"} {item.submitted_by ? `by ${item.submitted_by}` : ""}</li>
          ))}
          {items.length === 0 && <li>No pipeline items found.</li>}
        </ul>
      )}
    </div>
  );
}
