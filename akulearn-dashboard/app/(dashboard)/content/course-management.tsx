"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function CourseManagementPanel() {
  type Course = { id: string; title: string; description?: string; status?: string };
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCourses = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("courses").select("*");
        if (error) throw error;
        setCourses(data || []);
      } catch {
        setError("Unable to fetch courses.");
      }
      setLoading(false);
    };
    fetchCourses();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Course Management</h3>
      {loading && <div>Loading courses...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {courses.map(c => (
            <li key={c.id}><b>{c.title}</b> — {c.status || "draft"}</li>
          ))}
          {courses.length === 0 && <li>No courses found.</li>}
        </ul>
      )}
    </div>
  );
}
