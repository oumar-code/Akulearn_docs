"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

export default function StudentTeacherDashboard() {
  type Profile = { id: string; name?: string; role?: string; email?: string };
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfiles = async () => {
      setLoading(true);
      setError("");
      try {
        const { data, error } = await supabase.from("profiles").select("*");
        if (error) throw error;
        setProfiles(data || []);
      } catch {
        setError("Unable to fetch student/teacher profiles.");
      }
      setLoading(false);
    };
    fetchProfiles();
  }, []);

  return (
    <div style={{ padding: "1rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3>Student &amp; Teacher Dashboard</h3>
      {loading && <div>Loading profiles...</div>}
      {error && <div style={{ color: "#d32f2f" }}>{error}</div>}
      {!loading && !error && (
        <ul>
          {profiles.map(p => (
            <li key={p.id}>{p.name || p.email} — {p.role || "N/A"}</li>
          ))}
          {profiles.length === 0 && <li>No profiles found.</li>}
        </ul>
      )}
    </div>
  );
}
