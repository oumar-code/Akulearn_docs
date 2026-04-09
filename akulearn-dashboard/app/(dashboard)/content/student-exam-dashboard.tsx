"use client";

const EXAM_SUBJECTS: Record<string, string[]> = {
  JAMB: ["Use of English", "Mathematics", "Biology", "Physics", "Chemistry", "Economics", "Government", "Literature"],
  WAEC: ["English Language", "Mathematics", "Biology", "Chemistry", "Physics", "Economics", "Literature", "Government", "Agricultural Science"],
  NECO: ["English Language", "Mathematics", "Biology", "Chemistry", "Physics", "Economics", "Literature", "Government", "Agricultural Science"],
  Secondary: ["English Language", "Mathematics", "Basic Science", "Social Studies", "Civic Education", "Agricultural Science", "Computer Science", "Fine Art"],
};

const EXAM_COLORS: Record<string, string> = {
  JAMB: "#1a237e",
  WAEC: "#1b5e20",
  NECO: "#b71c1c",
  Secondary: "#4a148c",
};

type StudentUser = {
  name: string;
  email: string;
  exam_type: string;
  class_level: string;
  subjects: string[];
};

export default function StudentExamDashboard({ student }: { student: StudentUser }) {
  const examColor = EXAM_COLORS[student.exam_type] || "#333";
  const subjects = student.subjects?.length
    ? student.subjects
    : EXAM_SUBJECTS[student.exam_type] || [];

  return (
    <div style={{ maxWidth: 820, margin: "2rem auto", padding: "1.5rem", fontFamily: "sans-serif" }}>
      {/* Header */}
      <div style={{
        background: examColor,
        color: "#fff",
        borderRadius: 10,
        padding: "1.5rem 2rem",
        marginBottom: "1.5rem",
      }}>
        <h2 style={{ margin: 0 }}>👋 Welcome, {student.name}!</h2>
        <p style={{ margin: "0.5rem 0 0", opacity: 0.9 }}>
          {student.exam_type} Prep Dashboard &nbsp;·&nbsp; {student.class_level}
        </p>
        <p style={{ margin: "0.25rem 0 0", fontSize: "0.85rem", opacity: 0.75 }}>{student.email}</p>
      </div>

      {/* Quick Stats */}
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginBottom: "1.5rem" }}>
        {[
          { label: "Subjects Enrolled", value: subjects.length },
          { label: "Practice Tests Done", value: 0 },
          { label: "Avg. Score", value: "—" },
          { label: "Days to Exam", value: "—" },
        ].map(stat => (
          <div key={stat.label} style={{
            flex: "1 1 140px",
            background: "#f5f5f5",
            borderRadius: 8,
            padding: "1rem",
            textAlign: "center",
          }}>
            <div style={{ fontSize: "1.6rem", fontWeight: 700, color: examColor }}>{stat.value}</div>
            <div style={{ fontSize: "0.8rem", color: "#666", marginTop: 4 }}>{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Subjects */}
      <div style={{ background: "#fff", border: "1px solid #e0e0e0", borderRadius: 8, padding: "1.25rem", marginBottom: "1.5rem" }}>
        <h3 style={{ margin: "0 0 1rem", color: examColor }}>📚 My Subjects</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
          {subjects.map(subject => (
            <div key={subject} style={{
              background: examColor + "15",
              color: examColor,
              border: `1px solid ${examColor}40`,
              borderRadius: 20,
              padding: "0.35rem 0.9rem",
              fontSize: "0.9rem",
              cursor: "pointer",
            }}>
              {subject}
            </div>
          ))}
        </div>
      </div>

      {/* Past Questions */}
      <div style={{ background: "#fff", border: "1px solid #e0e0e0", borderRadius: 8, padding: "1.25rem", marginBottom: "1.5rem" }}>
        <h3 style={{ margin: "0 0 1rem", color: examColor }}>📝 Past Questions</h3>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem" }}>
          {["2023", "2022", "2021", "2020", "2019"].map(year => (
            <button key={year} style={{
              background: "#fff",
              border: `1px solid ${examColor}`,
              color: examColor,
              borderRadius: 6,
              padding: "0.5rem 1.1rem",
              cursor: "pointer",
              fontWeight: 600,
            }}>
              {student.exam_type} {year}
            </button>
          ))}
        </div>
        <p style={{ margin: "0.75rem 0 0", fontSize: "0.85rem", color: "#888" }}>
          Select a year to start a timed past-question session.
        </p>
      </div>

      {/* Practice Quiz */}
      <div style={{ background: "#fff", border: "1px solid #e0e0e0", borderRadius: 8, padding: "1.25rem", marginBottom: "1.5rem" }}>
        <h3 style={{ margin: "0 0 0.75rem", color: examColor }}>🎯 Practice Quiz</h3>
        <p style={{ margin: "0 0 1rem", color: "#555", fontSize: "0.9rem" }}>
          Start a topic-based quiz in any of your subjects to test your understanding.
        </p>
        <button style={{
          background: examColor,
          color: "#fff",
          border: "none",
          borderRadius: 6,
          padding: "0.6rem 1.5rem",
          cursor: "pointer",
          fontWeight: 600,
          fontSize: "0.95rem",
        }}>
          Start Practice Quiz
        </button>
      </div>

      {/* Study Schedule */}
      <div style={{ background: "#fff", border: "1px solid #e0e0e0", borderRadius: 8, padding: "1.25rem" }}>
        <h3 style={{ margin: "0 0 0.75rem", color: examColor }}>🗓 Study Schedule</h3>
        <p style={{ margin: 0, color: "#888", fontSize: "0.9rem" }}>
          Your personalised study schedule will appear here once set up by your coordinator.
        </p>
      </div>
    </div>
  );
}
