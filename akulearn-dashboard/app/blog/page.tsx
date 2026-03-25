import React from "react";
import Link from "next/link";
import styles from "./blog.module.css";

const articles = [
  { bg: "#dbeafe", icon: "📝", tag: "Study Tips", title: "How to Score 300+ in JAMB: A Proven 8-Week Study Plan", excerpt: "Consistent, structured preparation is the single biggest predictor of JAMB success. This step-by-step 8-week plan tells you exactly what to study each week to hit 300+.", date: "Jan 15, 2025", read: "8 min read" },
  { bg: "#d1fae5", icon: "🔬", tag: "Subject Guides", title: "JAMB Chemistry: 10 High-Frequency Topics You Must Master", excerpt: "Over 60% of JAMB Chemistry marks come from just 10 topic areas. We break down each one with the key formulas, reactions, and common question types you'll face.", date: "Jan 22, 2025", read: "10 min read" },
  { bg: "#fef3c7", icon: "📢", tag: "JAMB News", title: "JAMB 2025 Registration: Key Dates, Requirements & What's New", excerpt: "JAMB has announced important changes for the 2025 UTME. Here's everything you need to know about registration dates, biometric requirements, and new subject combinations.", date: "Feb 3, 2025", read: "6 min read" },
  { bg: "#ede9fe", icon: "🏆", tag: "Success Stories", title: "\"I Failed JAMB Twice—Then I Used Akudemy and Scored 318\"", excerpt: "Kelechi from Imo State shares his honest story of two failed attempts, how he changed his approach, and how targeted CBT practice helped him finally crack JAMB with a 318.", date: "Feb 10, 2025", read: "7 min read" },
  { bg: "#fce7f3", icon: "📐", tag: "Subject Guides", title: "JAMB Mathematics: Tackling Word Problems Without a Calculator", excerpt: "JAMB Maths questions are designed to be solved without a calculator. Learn the estimation techniques, number tricks, and shortcuts that top scorers use to work quickly.", date: "Feb 17, 2025", read: "9 min read" },
  { bg: "#ecfdf5", icon: "🧠", tag: "Study Tips", title: "5 Memory Techniques That Actually Work for JAMB Students", excerpt: "Cramming doesn't work. These five science-backed memory techniques—spaced repetition, active recall, mnemonics, chunking, and the Feynman method—will help you retain more.", date: "Feb 24, 2025", read: "7 min read" },
];

export default function BlogPage() {
  return (
    <div className={styles.page}>
      {/* NAV */}
      <nav className={styles.nav}>
        <Link href="/" className={styles.navLogo}>Aku<span>demy</span></Link>
        <div className={styles.navLinks}>
          <Link href="/#features">Features</Link>
          <Link href="/#subjects">Subjects</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/blog">Blog</Link>
          <Link href="/about">About</Link>
        </div>
        <Link href="/#pricing" className={styles.navCta}>Get Started Free</Link>
      </nav>

      {/* PAGE HERO */}
      <div className={styles.pageHero}>
        <h1>Akudemy Blog</h1>
        <p>Study tips, JAMB updates, subject guides, and success stories from Nigerian students just like you.</p>
      </div>

      {/* BLOG */}
      <div className={styles.blogSection}>
        <div className={styles.blogFilter}>
          <button className={`${styles.filterBtn} ${styles.active}`}>All</button>
          <button className={styles.filterBtn}>Study Tips</button>
          <button className={styles.filterBtn}>Subject Guides</button>
          <button className={styles.filterBtn}>JAMB News</button>
          <button className={styles.filterBtn}>Success Stories</button>
        </div>
        <div className={styles.blogGrid}>
          {articles.map((a) => (
            <div key={a.title} className={styles.blogCard}>
              <div className={styles.blogCardImg} style={{ background: a.bg }}>{a.icon}</div>
              <div className={styles.blogCardBody}>
                <span className={styles.blogTag}>{a.tag}</span>
                <h3>{a.title}</h3>
                <p>{a.excerpt}</p>
                <div className={styles.blogMeta}>
                  <span>{a.date} · {a.read}</span>
                  <Link href="#" className={styles.readMore}>Read →</Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* NEWSLETTER */}
      <div className={styles.newsletter}>
        <h2>Get Weekly Study Tips in Your Inbox</h2>
        <p>Join 12,000+ students who receive our free JAMB prep newsletter every week.</p>
        <div className={styles.newsletterForm}>
          <input type="email" placeholder="Enter your email address" />
          <button type="button">Subscribe Free</button>
        </div>
      </div>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.footerInner}>
          <div className={styles.footerBrand}>
            <div className={styles.footerLogo}>Aku<span>demy</span></div>
            <p>Nigeria&apos;s smartest JAMB<br/>exam preparation platform.</p>
          </div>
          <div className={styles.footerCol}>
            <h4>Platform</h4>
            <ul>
              <li><Link href="/#features">Features</Link></li>
              <li><Link href="/pricing">Pricing</Link></li>
              <li><Link href="/#subjects">Subjects</Link></li>
              <li><Link href="/blog">Blog</Link></li>
            </ul>
          </div>
          <div className={styles.footerCol}>
            <h4>Company</h4>
            <ul>
              <li><Link href="/about">About Us</Link></li>
              <li><Link href="/about#mission">Our Mission</Link></li>
              <li><Link href="/about#contact">Contact</Link></li>
            </ul>
          </div>
          <div className={styles.footerCol}>
            <h4>Resources</h4>
            <ul>
              <li><Link href="/blog">Blog</Link></li>
              <li><Link href="/about#faq">FAQ</Link></li>
              <li><Link href="#">Privacy Policy</Link></li>
              <li><Link href="#">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        <div className={styles.footerBottom}>© 2025 Akudemy · Part of the Akulearn EdTech Platform · Built for Nigerian students.</div>
      </footer>
    </div>
  );
}
