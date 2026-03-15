"use client";
import { useState } from "react";
import Link from "next/link";
import styles from "./jamb-feedback.module.css";

const FEATURES = [
  { value: "cbt-simulator", label: "CBT Simulator" },
  { value: "3d-models", label: "3D Science Models" },
  { value: "offline-mode", label: "Offline Mode" },
  { value: "progress-tracking", label: "Progress Tracking" },
  { value: "ai-explanations", label: "AI Explanations" },
  { value: "study-plan", label: "Study Plan" },
];

const RATINGS = ["😞", "😕", "😐", "🙂", "😄"];

export default function JambFeedbackPage() {
  const [rating, setRating] = useState<number | null>(null);
  const [whatWorks, setWhatWorks] = useState("");
  const [whatNeeds, setWhatNeeds] = useState("");
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);
  const [topics, setTopics] = useState("");
  const [scoreImprovement, setScoreImprovement] = useState("");
  const [device, setDevice] = useState("");
  const [internet, setInternet] = useState("");
  const [featureRequest, setFeatureRequest] = useState("");
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const toggleFeature = (val: string) => {
    setSelectedFeatures(prev => prev.includes(val) ? prev.filter(f => f !== val) : [...prev, val]);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 4000);
  };

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div className={styles.container}>
          <h1>JAMB Prep Feedback</h1>
          <p>Help us improve. Your feedback directly impacts Akudemy.</p>
        </div>
      </div>

      <div className={styles.container}>
        <div className={styles.formContainer}>
          {submitted && <div className={styles.successMsg}>✅ Thank you! Your feedback has been submitted and will help us improve Akudemy for all JAMB students.</div>}
          <form onSubmit={handleSubmit}>
            {/* RATING */}
            <div className={styles.formGroup}>
              <label>Overall Rating *</label>
              <div className={styles.ratingGroup}>
                {RATINGS.map((emoji, i) => (
                  <button
                    key={i}
                    type="button"
                    className={`${styles.ratingBtn} ${rating === i + 1 ? styles.selected : ""}`}
                    onClick={() => setRating(i + 1)}
                  >
                    {emoji}
                  </button>
                ))}
              </div>
            </div>

            {/* WHAT WORKS */}
            <div className={styles.formGroup}>
              <label htmlFor="whatWorks">What&apos;s working well? *</label>
              <textarea
                id="whatWorks"
                value={whatWorks}
                onChange={e => setWhatWorks(e.target.value)}
                placeholder="Tell us what you love about Akudemy…"
                required
              />
            </div>

            {/* WHAT NEEDS IMPROVEMENT */}
            <div className={styles.formGroup}>
              <label htmlFor="whatNeeds">What needs improvement? *</label>
              <textarea
                id="whatNeeds"
                value={whatNeeds}
                onChange={e => setWhatNeeds(e.target.value)}
                placeholder="What would make Akudemy better for you…"
                required
              />
            </div>

            {/* FEATURES USED */}
            <div className={styles.formGroup}>
              <label>Which features have you used?</label>
              <div className={styles.checkboxGroup}>
                {FEATURES.map(f => (
                  <label key={f.value} className={styles.checkboxItem}>
                    <input
                      type="checkbox"
                      checked={selectedFeatures.includes(f.value)}
                      onChange={() => toggleFeature(f.value)}
                    />
                    {f.label}
                  </label>
                ))}
              </div>
            </div>

            {/* SUBJECTS STRUGGLED WITH */}
            <div className={styles.formGroup}>
              <label htmlFor="topics">Which topics/subjects did you struggle with most?</label>
              <input
                type="text"
                id="topics"
                value={topics}
                onChange={e => setTopics(e.target.value)}
                placeholder="e.g. Chemistry organic reactions, Maths word problems…"
              />
            </div>

            {/* SCORE IMPROVEMENT */}
            <div className={styles.formGroup}>
              <label htmlFor="scoreImprovement">Did your mock test scores improve while using Akudemy?</label>
              <select id="scoreImprovement" value={scoreImprovement} onChange={e => setScoreImprovement(e.target.value)}>
                <option value="">Select an option</option>
                <option value="yes-significantly">Yes, significantly (20+ points)</option>
                <option value="yes-slightly">Yes, slightly (5–20 points)</option>
                <option value="same">About the same</option>
                <option value="no">No improvement yet</option>
                <option value="not-enough">Haven&apos;t used it enough to tell</option>
              </select>
            </div>

            {/* DEVICE */}
            <div className={styles.formGroup}>
              <label htmlFor="device">What device do you primarily use?</label>
              <select id="device" value={device} onChange={e => setDevice(e.target.value)}>
                <option value="">Select a device</option>
                <option value="android">Android phone</option>
                <option value="iphone">iPhone</option>
                <option value="tablet">Tablet</option>
                <option value="laptop">Laptop / PC</option>
              </select>
            </div>

            {/* INTERNET */}
            <div className={styles.formGroup}>
              <label>Do you have reliable internet access?</label>
              <div className={styles.radioGroup}>
                {[{ val: "yes", label: "Yes, always" }, { val: "sometimes", label: "Sometimes" }, { val: "no", label: "Rarely / Never" }].map(opt => (
                  <label key={opt.val} className={styles.radioItem}>
                    <input type="radio" name="internet" value={opt.val} checked={internet === opt.val} onChange={() => setInternet(opt.val)} />
                    {opt.label}
                  </label>
                ))}
              </div>
            </div>

            {/* FEATURE REQUEST */}
            <div className={styles.formGroup}>
              <label htmlFor="featureRequest">Is there a feature you wish Akudemy had?</label>
              <textarea
                id="featureRequest"
                value={featureRequest}
                onChange={e => setFeatureRequest(e.target.value)}
                placeholder="Describe a feature that would help you prepare better…"
              />
            </div>

            {/* EMAIL */}
            <div className={styles.formGroup}>
              <label htmlFor="feedbackEmail">Your email (optional — for follow-up)</label>
              <input
                type="email"
                id="feedbackEmail"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="you@example.com"
              />
            </div>

            <button type="submit" className={styles.submitBtn}>Submit Feedback</button>
          </form>
        </div>
      </div>

      <footer className={styles.footer}>
        <p>© 2026 Akudemy • JAMB Prep Feedback</p>
        <p><Link href="/">Back to Akudemy</Link></p>
      </footer>
    </div>
  );
}
