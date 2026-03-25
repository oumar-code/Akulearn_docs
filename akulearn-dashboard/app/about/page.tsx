import React from "react";
import styles from "./about.module.css";

export default function AboutPage() {
  return (
    <main>
      {/* Converted from about.html */}
      <nav>
        <div className="container">
          <a href="/">Akudemy</a>
          <a href="/blog">Blog</a>
          <a href="/pricing">Pricing</a>
        </div>
      </nav>
      <header>
        <div className="container">
          <span className="tag">Our Mission</span>
          <h1>Education that works without the internet.</h1>
          <p>
            Akudemy exists to give every Nigerian student access to quality, curriculum-aligned learning—
            no matter where they live or how reliable their connectivity is.
          </p>
        </div>
      </header>
      <section className="section">
        <div className="container grid">
          <div className="card">
            <h3>Why We Built Akudemy</h3>
            <p>Only 1 in 4 students has reliable internet. Most learning tools assume connectivity. We build for the other 3.</p>
          </div>
          <div className="card">
            <h3>What Makes Us Different</h3>
            <p>Offline-first, 3D learning models, AI-powered diagnostics, and curriculum alignment for WAEC/JAMB/NECO.</p>
          </div>
          <div className="card">
            <h3>Our Impact Goal</h3>
            <p>Help 10 million students across Africa access quality learning by 2030.</p>
          </div>
        </div>
      </section>
      <section className="section alt">
        <div className="container">
          <h2>Values We Live By</h2>
          <div className={"grid " + styles.marginTop2rem}>
            <div className="card"><strong>Accessibility</strong><br />Learning should work anywhere.</div>
            <div className="card"><strong>Quality</strong><br />Curriculum-aligned, exam-focused content.</div>
            <div className="card"><strong>Innovation</strong><br />3D models, AI, offline-first by design.</div>
            <div className="card"><strong>Impact</strong><br />Measurable student improvement.</div>
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Milestones</h2>
          <div className={"grid " + styles.marginTop2rem}>
            <div className="card"><strong>2025</strong><br />Platform prototype and initial content pipeline.</div>
            <div className="card"><strong>2026</strong><br />Launch with 1,350+ questions and 3D models.</div>
            <div className="card"><strong>2027</strong><br />Scale to 100,000+ students across Nigeria.</div>
          </div>
        </div>
      </section>
      <section className="cta">
        <div className="container">
          <h2>Join the Akudemy mission</h2>
          <p>Help us bring quality learning to every student.</p>
          <a href="/">Start Learning</a>
        </div>
      </section>
      <footer>
        <div className="container">© 2026 Akudemy • Part of the Aku ecosystem</div>
      </footer>
    </main>
  );
}
