import React from "react";
import Link from "next/link";
import styles from "./about.module.css";

export default function AboutPage() {
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
        <h1>About Akudemy</h1>
        <p>We&apos;re on a mission to make quality JAMB preparation accessible to every Nigerian student—regardless of location or income.</p>
      </div>

      {/* MISSION */}
      <section className={`${styles.section} ${styles.mission}`} id="mission">
        <div className={styles.inner}>
          <div className={styles.missionGrid}>
            <div className={styles.missionText}>
              <span className={styles.sectionTag}>Our Mission</span>
              <h2>Education Without Barriers</h2>
              <p>Every year, hundreds of thousands of Nigerian students sit the JAMB Unified Tertiary Matriculation Examination (UTME). For many, it&apos;s the difference between a university education and a deferred dream. Yet quality preparation materials remain inaccessible to millions due to cost, geography, and poor infrastructure.</p>
              <p>Akudemy exists to change that. We provide affordable, world-class JAMB preparation tools that work even in low-bandwidth environments, so every student—from Lagos to Zamfara—gets an equal shot at their dreams.</p>
              <p>We are part of the broader <strong>Akulearn EdTech Platform</strong>, building technology to make personalised, verifiable education universally accessible across Africa.</p>
            </div>
            <div className={styles.missionIconWrap}>🎓</div>
          </div>
        </div>
      </section>

      {/* VALUES */}
      <section className={styles.section}>
        <div className={styles.inner}>
          <span className={styles.sectionTag}>What We Stand For</span>
          <h2>Our Core Values</h2>
          <div className={styles.valuesGrid}>
            <div className={styles.valueCard}>
              <div className={styles.valueIcon}>🌍</div>
              <h3>Accessibility</h3>
              <p>Education must be available to every Nigerian student, regardless of where they live or what they can afford.</p>
            </div>
            <div className={styles.valueCard}>
              <div className={styles.valueIcon}>🏆</div>
              <h3>Excellence</h3>
              <p>We hold ourselves to the highest standard in content quality, platform reliability, and student outcomes.</p>
            </div>
            <div className={styles.valueCard}>
              <div className={styles.valueIcon}>🤝</div>
              <h3>Student-First</h3>
              <p>Every decision we make is guided by one question: does this help a student pass their exam?</p>
            </div>
            <div className={styles.valueCard}>
              <div className={styles.valueIcon}>🔬</div>
              <h3>Data-Driven</h3>
              <p>We use performance data and learning science to constantly improve how students prepare and retain knowledge.</p>
            </div>
          </div>
        </div>
      </section>

      {/* TEAM */}
      <section className={`${styles.section} ${styles.teamBg}`}>
        <div className={styles.inner}>
          <span className={styles.sectionTag}>The People Behind Akudemy</span>
          <h2>Our Team</h2>
          <p>We&apos;re a team of Nigerian educators, engineers, and dreamers who believe technology can transform education.</p>
          <div className={styles.teamGrid}>
            {[
              { avatar: "👨‍💻", name: "Umar Abubakar", role: "System Designer, Project Manager & Technical Lead" },
              { avatar: "👩‍💼", name: "Munira Abubakar", role: "Head of Product & External Engagement" },
              { avatar: "👨‍🏫", name: "Zakwan Lawali", role: "Head of Skill Acquisition & Vocational Training" },
              { avatar: "👩‍💰", name: "Balkisu Sani Kaura", role: "Head of Finance & Content Management" },
              { avatar: "👩‍🎓", name: "Hauwau Abubakar", role: "Exam Prep & Access Coordinator" },
            ].map((m) => (
              <div key={m.name} className={styles.teamCard}>
                <div className={styles.teamAvatar}>{m.avatar}</div>
                <h3>{m.name}</h3>
                <p>{m.role}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className={styles.section} id="faq">
        <div className={styles.inner}>
          <span className={styles.sectionTag}>FAQ</span>
          <h2>Frequently Asked Questions</h2>
          <div className={styles.faqList}>
            {[
              { q: "What is JAMB and why is exam prep important?", a: "JAMB (Joint Admissions and Matriculation Board) administers the UTME—the entrance exam required for admission into Nigerian universities and polytechnics. A high score dramatically increases your chances of admission to your dream institution." },
              { q: "How is Akudemy different from other prep platforms?", a: "Akudemy combines a realistic CBT simulator, AI-powered step-by-step explanations, personalised study plans, and offline support—all in one affordable package designed specifically for Nigerian students." },
              { q: "Can I use Akudemy without a strong internet connection?", a: "Yes! Our offline download feature lets you save questions, notes, and mock exams for use without an internet connection—perfect for students in areas with unreliable connectivity." },
              { q: "How up-to-date are the past questions?", a: "Our question bank is updated annually after each JAMB exam cycle. We include questions going back 20+ years, with particular emphasis on the most recent 5 years which reflect current JAMB trends." },
              { q: "Is there a free plan?", a: "Yes! Our Free plan gives you access to 100 past questions per month and 2 mock CBT exams—completely free, no credit card required. Upgrade to Pro when you're ready for full access." },
            ].map((item) => (
              <div key={item.q} className={styles.faqItem}>
                <div className={styles.faqQuestion}>{item.q}</div>
                <div className={styles.faqAnswer}>{item.a}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CONTACT */}
      <section className={`${styles.section} ${styles.contact}`} id="contact">
        <div className={styles.inner}>
          <span className={styles.sectionTag}>Get In Touch</span>
          <h2>Contact Us</h2>
          <p>Have questions? We&apos;d love to hear from you. Reach out through any of the channels below.</p>
          <div className={styles.contactGrid}>
            {[
              { icon: "📧", label: "Email", value: "hello@akudemy.ng" },
              { icon: "📱", label: "WhatsApp", value: "+234 803 294 2461" },
              { icon: "🐦", label: "Twitter / X", value: "@AkudemyNG" },
              { icon: "📘", label: "Facebook", value: "facebook.com/AkudemyNG" },
            ].map((c) => (
              <div key={c.label} className={styles.contactItem}>
                <div className={styles.contactIcon}>{c.icon}</div>
                <h4>{c.label}</h4>
                <p>{c.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

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
              <li><Link href="#mission">Our Mission</Link></li>
              <li><Link href="#contact">Contact</Link></li>
            </ul>
          </div>
          <div className={styles.footerCol}>
            <h4>Resources</h4>
            <ul>
              <li><Link href="/blog">Blog</Link></li>
              <li><Link href="#faq">FAQ</Link></li>
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
