import React from "react";

const TEAM = [
  {
    name: "Umar Abubakar",
    role: "System Designer, Project Manager & Technical Lead",
  },
  {
    name: "Munira Abubakar",
    role: "Head of Product & External Engagement",
  },
  {
    name: "Zakwan Lawali",
    role: "Head of Skill Acquisition & Vocational Training",
  },
  {
    name: "Balkisu Sani Kaura",
    role: "Head of Finance & Content Management",
  },
  {
    name: "Hauwau Abubakar",
    role: "Exam Prep & Access Coordinator",
  },
];

export default function AboutUsTeam() {
  return (
    <section className="section">
      <div className="container">
        <h2>Meet the Akudemy Team</h2>
        <div className="grid marginTop2rem">
          {TEAM.map((member) => (
            <div className="card" key={member.name}>
              <strong>{member.name}</strong>
              <br />
              <span>{member.role}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
