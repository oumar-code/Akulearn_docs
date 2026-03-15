import Link from "next/link";
import styles from "./home.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      {/* NAV */}
      <nav className={styles.nav}>
        <div className={styles.navLogo}>Aku<span>demy</span></div>
        <div className={styles.navLinks}>
          <Link href="#features">Features</Link>
          <Link href="#subjects">Subjects</Link>
          <Link href="/pricing">Pricing</Link>
          <Link href="/blog">Blog</Link>
          <Link href="/about">About</Link>
        </div>
        <Link href="#pricing" className={styles.navCta}>Get Started Free</Link>
      </nav>

      {/* HERO */}
      <section className={styles.hero}>
        <span className={styles.heroBadge}>🎓 Nigeria&apos;s #1 JAMB Prep Platform</span>
        <h1>Ace Your <span className={styles.highlight}>JAMB Exam</span><br/>With Confidence</h1>
        <p>Practice thousands of past questions, get instant AI feedback, and track your progress—all in one place. Built for Nigerian students.</p>
        <div className={styles.heroActions}>
          <Link href="#pricing" className={styles.btnPrimary}>Start Practicing Free</Link>
          <Link href="/about" className={styles.btnSecondary}>How It Works</Link>
        </div>
        <div className={styles.heroStats}>
          <div className={styles.stat}>
            <div className={styles.statValue}>50,000+</div>
            <div className={styles.statLabel}>Students Enrolled</div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statValue}>10,000+</div>
            <div className={styles.statLabel}>Past Questions</div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statValue}>95%</div>
            <div className={styles.statLabel}>Pass Rate</div>
          </div>
          <div className={styles.stat}>
            <div className={styles.statValue}>200+</div>
            <div className={styles.statLabel}>Mock Tests</div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className={`${styles.section} ${styles.features}`} id="features">
        <span className={styles.sectionTag}>Why Akudemy</span>
        <h2 className={styles.sectionTitle}>Everything You Need to Pass JAMB</h2>
        <p className={styles.sectionSub}>We&apos;ve built every tool a Nigerian student needs to prepare smarter and perform better on exam day.</p>
        <div className={styles.featureGrid}>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📝</div>
            <h3>CBT Mock Exams</h3>
            <p>Simulate the real JAMB CBT environment with timed practice tests drawn from 20+ years of past questions.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🤖</div>
            <h3>AI-Powered Explanations</h3>
            <p>Get step-by-step explanations for every answer. Understand the &ldquo;why&rdquo; behind each solution, not just the result.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📊</div>
            <h3>Performance Analytics</h3>
            <p>Track your scores over time, identify weak topics, and see exactly where to focus your study sessions.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>🗓️</div>
            <h3>Personalised Study Plan</h3>
            <p>Our smart algorithm builds a custom study schedule based on your exam date, target score, and weak areas.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📚</div>
            <h3>Comprehensive Notes</h3>
            <p>Access concise, exam-focused revision notes for every JAMB subject—written by top Nigerian educators.</p>
          </div>
          <div className={styles.featureCard}>
            <div className={styles.featureIcon}>📱</div>
            <h3>Study Offline</h3>
            <p>Download questions and notes for offline study. Never let poor internet connection slow your preparation.</p>
          </div>
        </div>
      </section>

      {/* SUBJECTS */}
      <section className={styles.section} id="subjects">
        <span className={styles.sectionTag}>Coverage</span>
        <h2 className={styles.sectionTitle}>All JAMB Subjects Covered</h2>
        <p className={styles.sectionSub}>From English Language to the sciences, we have comprehensive content for every JAMB subject combination.</p>
        <div className={styles.subjectsGrid}>
          {["English Language","Mathematics","Physics","Chemistry","Biology","Economics","Government","Literature-in-English","Geography","Accounting","Commerce","Agricultural Science","Christian Religious Studies","Islamic Studies","History","Yoruba","Igbo","Hausa"].map(s => (
            <span key={s} className={styles.subjectPill}>{s}</span>
          ))}
        </div>
      </section>

      {/* PRICING */}
      <section className={`${styles.section} ${styles.pricingBg}`} id="pricing">
        <span className={styles.sectionTag}>Pricing</span>
        <h2 className={styles.sectionTitle}>Simple, Affordable Plans</h2>
        <p className={styles.sectionSub}>Choose the plan that works for you. All plans include access to past questions and performance tracking.</p>
        <div className={styles.pricingGrid}>
          <div className={styles.planCard}>
            <div className={styles.planName}>Free</div>
            <div className={styles.planPrice}>₦0 <span>/ month</span></div>
            <p className={styles.planDesc}>Perfect to get started and try out the platform.</p>
            <ul className={styles.planFeatures}>
              <li>100 past questions per month</li>
              <li>2 mock CBT exams per month</li>
              <li>Basic performance dashboard</li>
              <li>Community forum access</li>
            </ul>
            <Link href="/register" className={`${styles.planBtn} ${styles.planBtnOutline}`}>Sign Up Free</Link>
          </div>
          <div className={`${styles.planCard} ${styles.popular}`}>
            <span className={styles.popularBadge}>Most Popular</span>
            <div className={styles.planName}>Pro</div>
            <div className={styles.planPrice}>₦2,500 <span>/ month</span></div>
            <p className={styles.planDesc}>Full access for serious JAMB candidates.</p>
            <ul className={styles.planFeatures}>
              <li>Unlimited past questions</li>
              <li>Unlimited mock CBT exams</li>
              <li>AI-powered explanations</li>
              <li>Personalised study plan</li>
              <li>Full performance analytics</li>
              <li>Offline downloads</li>
            </ul>
            <Link href="/register" className={`${styles.planBtn} ${styles.planBtnFilled}`}>Get Pro</Link>
          </div>
          <div className={styles.planCard}>
            <div className={styles.planName}>School</div>
            <div className={styles.planPrice}>₦15,000 <span>/ school/mo</span></div>
            <p className={styles.planDesc}>For secondary schools preparing their students for JAMB.</p>
            <ul className={styles.planFeatures}>
              <li>Up to 200 student accounts</li>
              <li>Teacher dashboard &amp; reports</li>
              <li>Class-wide performance analytics</li>
              <li>Dedicated support</li>
              <li>Custom branding (optional)</li>
            </ul>
            <Link href="/about#contact" className={`${styles.planBtn} ${styles.planBtnOutline}`}>Contact Us</Link>
          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section className={`${styles.section} ${styles.testimonials}`}>
        <span className={styles.sectionTag}>Success Stories</span>
        <h2 className={styles.sectionTitle}>Students Love Akudemy</h2>
        <p className={styles.sectionSub}>Join thousands of Nigerian students who passed JAMB using Akudemy.</p>
        <div className={styles.testiGrid}>
          {[
            { text: "I scored 312 in JAMB after using Akudemy for just 6 weeks. The mock CBT exams made me so comfortable on the real exam day.", author: "Fatima A.", role: "Lagos State — scored 312, admitted to UNILAG" },
            { text: "The AI explanations helped me understand topics I had been struggling with for years. Chemistry finally makes sense to me!", author: "Emeka O.", role: "Enugu State — scored 298, admitted to UNN" },
            { text: "I live in a rural area with poor internet. The offline feature was a lifesaver. I downloaded everything at school and studied at home.", author: "Aminu S.", role: "Zamfara State — scored 287, admitted to BUK" },
            { text: "Our school subscribed to the School plan and our JAMB pass rate went from 60% to 91% in one year. Remarkable results.", author: "Mr. Bello I.", role: "Vice Principal, Government Secondary School, Kano" },
            { text: "The personalised study plan kept me on track. I knew exactly what to study every day and never felt overwhelmed.", author: "Chidinma E.", role: "Anambra State — scored 305, admitted to UNIZIK" },
            { text: "Worth every naira. I tried other platforms but Akudemy had the best explanations and the most realistic CBT simulator.", author: "Tunde B.", role: "Ogun State — scored 320, admitted to OAU" },
          ].map((t) => (
            <div key={t.author} className={styles.testiCard}>
              <div className={styles.testiStars}>★★★★★</div>
              <p className={styles.testiText}>&ldquo;{t.text}&rdquo;</p>
              <div className={styles.testiAuthor}>{t.author}</div>
              <div className={styles.testiRole}>{t.role}</div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA BANNER */}
      <div className={styles.ctaBanner}>
        <h2>Ready to Pass JAMB?</h2>
        <p>Join over 50,000 students already preparing on Akudemy. Start for free—no credit card required.</p>
        <Link href="#pricing" className={styles.btnWhite}>Start Practising Free</Link>
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
              <li><Link href="#features">Features</Link></li>
              <li><Link href="/pricing">Pricing</Link></li>
              <li><Link href="#subjects">Subjects</Link></li>
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

