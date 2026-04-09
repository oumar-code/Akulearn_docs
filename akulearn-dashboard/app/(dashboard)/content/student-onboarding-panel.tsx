"use client";
import { useState } from "react";
import { supabase } from "../../../lib/supabaseClient";

const EXAM_TYPES = ["JAMB", "WAEC", "NECO", "Secondary"] as const;
const CLASS_LEVELS = ["JSS1", "JSS2", "JSS3", "SS1", "SS2", "SS3"] as const;

const SUBJECTS_BY_EXAM: Record<string, string[]> = {
  JAMB: ["Use of English", "Mathematics", "Biology", "Physics", "Chemistry", "Economics", "Government", "Literature", "Geography", "Agricultural Science"],
  WAEC: ["English Language", "Mathematics", "Biology", "Chemistry", "Physics", "Economics", "Literature in English", "Government", "Agricultural Science", "Geography", "Accounting", "Commerce"],
  NECO: ["English Language", "Mathematics", "Biology", "Chemistry", "Physics", "Economics", "Literature in English", "Government", "Agricultural Science", "Geography", "Accounting", "Commerce"],
  Secondary: ["English Language", "Mathematics", "Basic Science", "Social Studies", "Civic Education", "Agricultural Science", "Computer Science", "Fine Art", "Business Studies", "French"],
};

type OnboardedStudent = {
  name: string;
  email: string;
  exam_type: string;
  class_level: string;
  subjects: string[];
  status: string;
};

export default function StudentOnboardingPanel() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [examType, setExamType] = useState<typeof EXAM_TYPES[number]>("JAMB");
  const [classLevel, setClassLevel] = useState<typeof CLASS_LEVELS[number]>("SS2");
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>([]);
  const [students, setStudents] = useState<OnboardedStudent[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const availableSubjects = SUBJECTS_BY_EXAM[examType] || [];

  const toggleSubject = (subject: string) => {
    setSelectedSubjects(prev =>
      prev.includes(subject) ? prev.filter(s => s !== subject) : [...prev, subject]
    );
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || selectedSubjects.length === 0) {
      setMessage("Please fill in all fields and select at least one subject.");
      return;
    }
    setLoading(true);
    setMessage("");

    // Use Supabase magic link to invite the student
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        data: {
          name,
          exam_type: examType,
          class_level: classLevel,
          subjects: selectedSubjects,
          role: `student_${examType.toLowerCase()}`,
          dashboard: "student",
        },
      },
    });

    if (error) {
      setMessage(`Error: ${error.message}`);
    } else {
      const newStudent: OnboardedStudent = {
        name,
        email,
        exam_type: examType,
        class_level: classLevel,
        subjects: selectedSubjects,
        status: "Invitation sent ✓",
      };
      setStudents(prev => [newStudent, ...prev]);
      setMessage(`✅ Invitation sent to ${name} (${email}) — they will receive a login link.`);
      setName("");
      setEmail("");
      setSelectedSubjects([]);
    }
    setLoading(false);
  };

  const examColors: Record<string, string> = {
    JAMB: "#1a237e",
    WAEC: "#1b5e20",
    NECO: "#b71c1c",
    Secondary: "#4a148c",
  };
  const color = examColors[examType] || "#333";

  return (
    <div style={{ padding: "1.25rem", border: "1px solid #e0e0e0", borderRadius: 8, margin: "1rem 0" }}>
      <h3 style={{ color: "#333", marginTop: 0 }}>🎓 Student Onboarding</h3>
      <p style={{ color: "#666", fontSize: "0.9rem", marginTop: 0 }}>
        Register students for JAMB, WAEC, NECO, or Secondary school dashboards. They will receive a magic-link login invitation.
      </p>

      <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", gap: "0.75rem", maxWidth: 480 }}>
        <div>
          <label style={{ display: "block", marginBottom: 4, fontWeight: 600, fontSize: "0.9rem" }}>Full Name</label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="Student full name"
            required
            style={{ width: "100%", padding: "0.5rem 0.75rem", borderRadius: 4, border: "1px solid #ccc", fontSize: "0.9rem", boxSizing: "border-box" }}
          />
        </div>

        <div>
          <label style={{ display: "block", marginBottom: 4, fontWeight: 600, fontSize: "0.9rem" }}>Email Address</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="student@email.com"
            required
            style={{ width: "100%", padding: "0.5rem 0.75rem", borderRadius: 4, border: "1px solid #ccc", fontSize: "0.9rem", boxSizing: "border-box" }}
          />
        </div>

        <div style={{ display: "flex", gap: "0.75rem" }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: "block", marginBottom: 4, fontWeight: 600, fontSize: "0.9rem" }}>Exam Type</label>
            <select
              value={examType}
              onChange={e => {
                setExamType(e.target.value as typeof EXAM_TYPES[number]);
                setSelectedSubjects([]);
              }}
              style={{ width: "100%", padding: "0.5rem 0.75rem", borderRadius: 4, border: "1px solid #ccc", fontSize: "0.9rem" }}
            >
              {EXAM_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          <div style={{ flex: 1 }}>
            <label style={{ display: "block", marginBottom: 4, fontWeight: 600, fontSize: "0.9rem" }}>Class Level</label>
            <select
              value={classLevel}
              onChange={e => setClassLevel(e.target.value as typeof CLASS_LEVELS[number])}
              style={{ width: "100%", padding: "0.5rem 0.75rem", borderRadius: 4, border: "1px solid #ccc", fontSize: "0.9rem" }}
            >
              {CLASS_LEVELS.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
          </div>
        </div>

        <div>
          <label style={{ display: "block", marginBottom: 6, fontWeight: 600, fontSize: "0.9rem" }}>
            Subjects <span style={{ color: "#888", fontWeight: 400 }}>({selectedSubjects.length} selected)</span>
          </label>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem" }}>
            {availableSubjects.map(subject => (
              <button
                key={subject}
                type="button"
                onClick={() => toggleSubject(subject)}
                style={{
                  padding: "0.3rem 0.75rem",
                  borderRadius: 16,
                  border: `1px solid ${selectedSubjects.includes(subject) ? color : "#ccc"}`,
                  background: selectedSubjects.includes(subject) ? color : "#fff",
                  color: selectedSubjects.includes(subject) ? "#fff" : "#444",
                  cursor: "pointer",
                  fontSize: "0.82rem",
                  fontWeight: selectedSubjects.includes(subject) ? 600 : 400,
                }}
              >
                {subject}
              </button>
            ))}
          </div>
        </div>

        {message && (
          <div style={{ color: message.startsWith("✅") ? "#2e7d32" : "#c62828", fontSize: "0.9rem", padding: "0.5rem 0.75rem", background: message.startsWith("✅") ? "#e8f5e9" : "#ffebee", borderRadius: 4 }}>
            {message}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{ padding: "0.6rem 1.5rem", background: color, color: "#fff", border: "none", borderRadius: 4, cursor: "pointer", fontWeight: 600, fontSize: "0.95rem", alignSelf: "flex-start" }}
        >
          {loading ? "Sending…" : "Register Student & Send Invite"}
        </button>
      </form>

      {/* Onboarded students list */}
      {students.length > 0 && (
        <div style={{ marginTop: "1.5rem" }}>
          <h4 style={{ margin: "0 0 0.75rem" }}>Recently Onboarded</h4>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.85rem" }}>
            <thead>
              <tr style={{ background: "#f5f5f5" }}>
                {["Name", "Email", "Exam", "Class", "Subjects", "Status"].map(h => (
                  <th key={h} style={{ padding: "0.5rem 0.75rem", textAlign: "left", border: "1px solid #e0e0e0" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {students.map((s, i) => (
                <tr key={i}>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0" }}>{s.name}</td>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0" }}>{s.email}</td>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0" }}>{s.exam_type}</td>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0" }}>{s.class_level}</td>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0" }}>{s.subjects.join(", ")}</td>
                  <td style={{ padding: "0.5rem 0.75rem", border: "1px solid #e0e0e0", color: "#2e7d32" }}>{s.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
