import React from "react";

export default function BlogPage() {
  return (
    <main>
      {/* Converted from blog.html */}
      <nav>
        <div className="container">
          <a href="/">Akudemy</a>
          <a href="/about">About</a>
          <a href="/pricing">Pricing</a>
        </div>
      </nav>
      <header>
        <div className="container">
          <h1>Akudemy Blog</h1>
          <p>Study tips, exam strategies, and the science of learning.</p>
        </div>
      </header>
      <section className="posts">
        <div className="container">
          <div className="post-grid">
            <article className="post">
              <span className="tag">Exam Prep</span>
              <h3>How to Prepare for WAEC in 30 Days</h3>
              <p>Practical strategies to focus on high-impact topics and improve scores fast.</p>
            </article>
            <article className="post">
              <span className="tag">Science</span>
              <h3>Why 3D Models Help You Remember Chemistry</h3>
              <p>Visual learning boosts retention. Here’s how 3D makes abstract ideas concrete.</p>
            </article>
            <article className="post">
              <span className="tag">Study Hacks</span>
              <h3>7 Proven Study Techniques for JAMB Success</h3>
              <p>From spaced repetition to practice tests—these techniques work.</p>
            </article>
            <article className="post">
              <span className="tag">Offline Learning</span>
              <h3>Learning Without Internet: How Akudemy Works</h3>
              <p>Offline-first architecture explained in simple terms for students and parents.</p>
            </article>
            <article className="post">
              <span className="tag">Education</span>
              <h3>NECO Prep: The Topics Students Miss Most</h3>
              <p>We analyzed common weak areas and how to improve them quickly.</p>
            </article>
            <article className="post">
              <span className="tag">Product</span>
              <h3>Inside Akudemy: Building for Nigeria First</h3>
              <p>Why we chose offline-first and how we built the platform.</p>
            </article>
          </div>
        </div>
      </section>
      <section className="cta">
        <div className="container">
          <h2>Want more study tips?</h2>
          <p>Follow Akudemy and get weekly learning content.</p>
          <a href="/">Start Learning</a>
        </div>
      </section>
      <footer>
        <div className="container">© 2026 Akudemy • Learn Anywhere. Achieve Everywhere.</div>
      </footer>
    </main>
  );
}
