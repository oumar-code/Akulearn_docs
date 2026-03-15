"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import styles from "./jamb.module.css";

function useCountdown(targetDate: Date) {
  const calc = () => {
    const diff = targetDate.getTime() - Date.now();
    if (diff <= 0) return { days: 0, hours: 0, minutes: 0, seconds: 0 };
    return {
      days: Math.floor(diff / 86400000),
      hours: Math.floor((diff % 86400000) / 3600000),
      minutes: Math.floor((diff % 3600000) / 60000),
      seconds: Math.floor((diff % 60000) / 1000),
    };
  };
  const [time, setTime] = useState(calc);
  useEffect(() => {
    const id = setInterval(() => setTime(calc()), 1000);
    return () => clearInterval(id);
  });
  return time;
}

const EXAM_DATE = new Date("May 15, 2026 10:00:00");

const features = [
  { icon: "📚", title: "500+ JAMB Questions", desc: "Practice with real JAMB-style questions across all 4 subjects. Master time management and exam patterns." },
  { icon: "🧬", title: "3D Science Models", desc: "Visualize Biology, Chemistry, and Physics concepts. Complex topics become crystal clear." },
  { icon: "📱", title: "Offline Learning", desc: "No internet needed. Download and study anywhere—in your room, the bus, or during data blackouts." },
  { icon: "📊", title: "Progress Tracking", desc: "See exactly where you're struggling. Know your weak topics before exam day." },
  { icon: "🎯", title: "Timed Practice Tests", desc: "Practice under real exam conditions. 3 hours, 180 questions. Get feedback instantly." },
  { icon: "🌍", title: "Multi-Language Support", desc: "Learn in English, Hausa, Yoruba, or Igbo. Education in the language that works for you." },
];

const faqs = [
  { q: "Is it really free?", a: "Yes, completely free for JAMB 2026 candidates. We're in beta and want your feedback to improve before national rollout. No credit card, no hidden fees." },
  { q: "How long is the free access?", a: "Until the JAMB exam. You get continuous access during your preparation period, plus feedback integration." },
  { q: "What if I don't have good internet?", a: "Perfect! Download everything once and study offline. No data needed. Works even in areas with no connectivity." },
  { q: "Can I use it on my phone?", a: "Yes. Works on Android and iPhone. The app and web version sync so you can switch between devices." },
  { q: "Will my data be shared?", a: "Never. Your progress and performance data is private. We only use it to improve your learning experience and product feedback." },
  { q: "What happens after free access ends?", a: "Optional upgrade to Student Premium (₦1,500/month) for continued access. But no pressure—your exam prep is our first goal." },
  { q: "How do I get started?", a: "Fill the form above. We'll send you the download link and onboarding video within 24 hours. Start studying immediately." },
];

export default function JambPage() {
  const { days, hours, minutes, seconds } = useCountdown(EXAM_DATE);
  const [form, setForm] = useState({ name: "", email: "", phone: "", state: "", examMonth: "" });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 4000);
    setForm({ name: "", email: "", phone: "", state: "", examMonth: "" });
  };

  return (
    <div className={styles.page}>
      {/* NAV */}
      <nav className={styles.nav}>
        <div className={styles.container}>
          <Link href="/">← Back to Akudemy</Link>
        </div>
      </nav>

      {/* HERO */}
      <section className={styles.hero}>
        <div className={styles.container}>
          <div className={styles.heroContent}>
            <div>
              <div className={styles.urgencyBanner}>⏰ LIMITED TIME OFFER</div>
              <h1>Free JAMB Prep for 2026 Candidates</h1>
              <p>You&apos;re registered for JAMB. Now prepare seriously. Get free access to 500+ JAMB questions, 3D science models, and offline learning—no payment needed.</p>
              <div className={styles.heroActions}>
                <a href="#signup" className={`${styles.btn} ${styles.btnPrimary}`}>Get Free Access Now</a>
                <a href="#how" className={`${styles.btn} ${styles.btnWhite}`}>See How It Works</a>
              </div>
              <div className={styles.heroStats}>
                <div className={styles.stat}><div className={styles.statNumber}>500+</div><div className={styles.statLabel}>JAMB Questions</div></div>
                <div className={styles.stat}><div className={styles.statNumber}>3D</div><div className={styles.statLabel}>Science Models</div></div>
                <div className={styles.stat}><div className={styles.statNumber}>100%</div><div className={styles.statLabel}>Free</div></div>
              </div>
            </div>
            <div className={styles.countdown}>
              <p>Time to prepare:</p>
              <div className={styles.countdownTimer}>
                {[{ val: days, label: "Days" }, { val: hours, label: "Hours" }, { val: minutes, label: "Minutes" }, { val: seconds, label: "Seconds" }].map(({ val, label }) => (
                  <div key={label} className={styles.timerBox}>
                    <div className={styles.timerNumber}>{val}</div>
                    <div className={styles.timerLabel}>{label}</div>
                  </div>
                ))}
              </div>
              <p style={{ marginTop: "1.5rem", fontSize: "0.85rem" }}>Until the 2026 JAMB exam</p>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className={styles.features}>
        <div className={styles.container}>
          <h2>What&apos;s Included in Free JAMB Prep</h2>
          <div className={styles.grid}>
            {features.map((f) => (
              <div key={f.title} className={styles.card}>
                <div className={styles.cardIcon}>{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SUBJECTS */}
      <section className={styles.jambContent}>
        <div className={styles.container}>
          <div className={styles.jambHeader}>
            <h2>All 4 JAMB Subjects Covered</h2>
            <p>Complete preparation across English Language, Mathematics, and your choice of 2 subjects.</p>
          </div>
          <div className={styles.subjects}>
            {["📖 English Language","🔢 Mathematics","🧪 Chemistry","🧬 Biology","⚡ Physics","🌍 Geography","📚 Literature","🏛️ History"].map(s => (
              <div key={s} className={styles.subjectBadge}>{s}</div>
            ))}
          </div>
        </div>
      </section>

      {/* WHY FREE */}
      <section className={styles.whyFree}>
        <div className={styles.container}>
          <h2>Why We&apos;re Offering Free Access</h2>
          <p>You&apos;ve taken the first step by registering for JAMB. We want to support you all the way to exam success. We&apos;re offering free premium access during this preparation period so we can gather your feedback and improve before the national rollout. Your success is our success.</p>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className={styles.testimonials}>
        <div className={styles.container}>
          <h2>What JAMB Candidates Are Saying</h2>
          <div className={styles.testiGrid}>
            {[
              { text: "I can study offline! No more worrying about data. The 3D models made Chemistry finally click for me.", author: "— Tunde, SS3, Lagos" },
              { text: "The practice tests are exactly like real JAMB. I've done 5 so far and improved from 185 to 240.", author: "— Chioma, JAMB Candidate, Enugu" },
              { text: "Free and actually helpful. Way better than textbooks. Worth every second I spend on it.", author: "— Aminu, SS3, Kano" },
            ].map((t) => (
              <div key={t.author} className={styles.testi}>
                <p className={styles.testiText}>&ldquo;{t.text}&rdquo;</p>
                <div className={styles.testiAuthor}>{t.author}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SIGNUP */}
      <section className={styles.signupSection} id="signup">
        <div className={styles.container}>
          <h2>Get Your Free JAMB Prep Access</h2>
          <p>One-minute signup. No credit card. Start immediately.</p>
          <form className={styles.formContainer} onSubmit={handleSubmit}>
            {submitted && <div className={styles.successMsg}>✅ Access granted! Check your email for the download link and onboarding video.</div>}
            <div className={styles.formGroup}>
              <label htmlFor="name">Full Name *</label>
              <input type="text" id="name" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="jambEmail">Email Address *</label>
              <input type="email" id="jambEmail" value={form.email} onChange={e => setForm({ ...form, email: e.target.value })} required />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="phone">Phone Number (WhatsApp) *</label>
              <input type="tel" id="phone" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} placeholder="+234..." required />
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="state">Your State *</label>
              <select id="state" value={form.state} onChange={e => setForm({ ...form, state: e.target.value })} required>
                <option value="">Select State</option>
                {["Lagos","Abuja","Kano","Rivers","Oyo","Enugu","Kaduna","Other"].map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className={styles.formGroup}>
              <label htmlFor="examMonth">Expected JAMB Exam Month *</label>
              <input type="month" id="examMonth" value={form.examMonth} onChange={e => setForm({ ...form, examMonth: e.target.value })} required />
            </div>
            <button type="submit" className={styles.submitBtn}>Get Free Access (No CC Required)</button>
          </form>
        </div>
      </section>

      {/* FAQ */}
      <section className={styles.faq} id="how">
        <div className={styles.container}>
          <h2>Frequently Asked Questions</h2>
          {faqs.map((f) => (
            <div key={f.q} className={styles.faqItem}>
              <strong>{f.q}</strong>
              <p>{f.a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.container}>
          <p>© 2026 Akudemy • Free JAMB Prep Campaign</p>
          <p><Link href="/">Back to Akudemy</Link></p>
        </div>
      </footer>
    </div>
  );
}
