import React from "react";
import Link from "next/link";
import styles from "./pricing.module.css";

export default function PricingPage() {
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
        <Link href="#plans" className={styles.navCta}>Get Started Free</Link>
      </nav>

      {/* PAGE HERO */}
      <div className={styles.pageHero}>
        <h1>Simple, Affordable Pricing</h1>
        <p>No tricks, no hidden fees. Pick the plan that works for you and start preparing today.</p>
      </div>

      {/* PLANS */}
      <div className={styles.pricingSection} id="plans">
        <div className={styles.pricingGrid}>
          {/* FREE */}
          <div className={styles.planCard}>
            <div className={styles.planName}>Free</div>
            <div className={styles.planPrice}>₦0 <sub>/ month</sub></div>
            <p className={styles.planDesc}>Get started with no commitment. Perfect for trying out the platform.</p>
            <Link href="/register" className={`${styles.planBtn} ${styles.planBtnOutline}`}>Sign Up Free</Link>
            <hr className={styles.planDivider} />
            <p className={styles.planFeaturesTitle}>What&apos;s included</p>
            <ul className={styles.planFeatures}>
              <li><span className={styles.fi}>✓</span> 100 past questions per month</li>
              <li><span className={styles.fi}>✓</span> 2 mock CBT exams per month</li>
              <li><span className={styles.fi}>✓</span> Basic performance dashboard</li>
              <li><span className={styles.fi}>✓</span> Community forum access</li>
              <li><span className={styles.fx}>✗</span> AI-powered explanations</li>
              <li><span className={styles.fx}>✗</span> Personalised study plan</li>
              <li><span className={styles.fx}>✗</span> Offline downloads</li>
              <li><span className={styles.fx}>✗</span> Full analytics</li>
            </ul>
          </div>
          {/* PRO */}
          <div className={`${styles.planCard} ${styles.popular}`}>
            <span className={styles.popularBadge}>⭐ Most Popular</span>
            <div className={styles.planName}>Pro</div>
            <div className={styles.planPrice}>₦2,500 <sub>/ month</sub></div>
            <p className={styles.planDesc}>Everything you need for serious JAMB preparation. Best for individual students.</p>
            <Link href="/register" className={`${styles.planBtn} ${styles.planBtnFilled}`}>Get Pro Now</Link>
            <hr className={styles.planDivider} />
            <p className={styles.planFeaturesTitle}>Everything in Free, plus:</p>
            <ul className={styles.planFeatures}>
              <li><span className={styles.fi}>✓</span> Unlimited past questions</li>
              <li><span className={styles.fi}>✓</span> Unlimited mock CBT exams</li>
              <li><span className={styles.fi}>✓</span> AI-powered step-by-step explanations</li>
              <li><span className={styles.fi}>✓</span> Personalised study plan</li>
              <li><span className={styles.fi}>✓</span> Full performance analytics</li>
              <li><span className={styles.fi}>✓</span> Offline question &amp; note downloads</li>
              <li><span className={styles.fi}>✓</span> Revision notes for all subjects</li>
              <li><span className={styles.fi}>✓</span> Priority email support</li>
            </ul>
          </div>
          {/* SCHOOL */}
          <div className={styles.planCard}>
            <div className={styles.planName}>School</div>
            <div className={styles.planPrice}>₦15,000 <sub>/ school/mo</sub></div>
            <p className={styles.planDesc}>For secondary schools. Manage up to 200 student accounts from one dashboard.</p>
            <Link href="/about#contact" className={`${styles.planBtn} ${styles.planBtnOutline}`}>Contact Sales</Link>
            <hr className={styles.planDivider} />
            <p className={styles.planFeaturesTitle}>Everything in Pro, plus:</p>
            <ul className={styles.planFeatures}>
              <li><span className={styles.fi}>✓</span> Up to 200 student accounts</li>
              <li><span className={styles.fi}>✓</span> Teacher / admin dashboard</li>
              <li><span className={styles.fi}>✓</span> Class-wide performance reports</li>
              <li><span className={styles.fi}>✓</span> Bulk student onboarding</li>
              <li><span className={styles.fi}>✓</span> Dedicated account manager</li>
              <li><span className={styles.fi}>✓</span> Custom branding (add-on)</li>
              <li><span className={styles.fi}>✓</span> Invoice-based billing available</li>
              <li><span className={styles.fi}>✓</span> Phone &amp; WhatsApp support</li>
            </ul>
          </div>
        </div>
      </div>

      {/* COMPARISON TABLE */}
      <div className={styles.comparison}>
        <h2>Compare Plans Side by Side</h2>
        <p>See exactly what you get with each plan.</p>
        <div className={styles.tableWrap}>
          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th>Free</th>
                <th className={styles.highlightCol}>Pro</th>
                <th>School</th>
              </tr>
            </thead>
            <tbody>
              <tr><td>Past questions per month</td><td>100</td><td className={styles.highlightCol}>Unlimited</td><td>Unlimited</td></tr>
              <tr><td>Mock CBT exams</td><td>2 / month</td><td className={styles.highlightCol}>Unlimited</td><td>Unlimited</td></tr>
              <tr><td>AI explanations</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.check}>✓</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Personalised study plan</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.check}>✓</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Full performance analytics</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.check}>✓</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Offline downloads</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.check}>✓</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Revision notes</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.check}>✓</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Teacher dashboard</td><td><span className={styles.cross}>✗</span></td><td className={styles.highlightCol}><span className={styles.cross}>✗</span></td><td><span className={styles.check}>✓</span></td></tr>
              <tr><td>Student accounts</td><td>1</td><td className={styles.highlightCol}>1</td><td>Up to 200</td></tr>
              <tr><td>Support</td><td>Community</td><td className={styles.highlightCol}>Email</td><td>Phone + WhatsApp</td></tr>
              <tr><td>Monthly price</td><td>₦0</td><td className={styles.highlightCol}><strong style={{color:"#1a56db"}}>₦2,500</strong></td><td>₦15,000</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* GUARANTEE */}
      <div className={styles.guarantee}>
        <div className={styles.guaranteeIcon}>🛡️</div>
        <h2>14-Day Money-Back Guarantee</h2>
        <p>Not satisfied after 14 days on a paid plan? Contact us and we&apos;ll issue a full refund—no questions asked. We stand behind the quality of Akudemy.</p>
      </div>

      {/* FAQ */}
      <div className={styles.faqSection}>
        <h2>Pricing FAQs</h2>
        {[
          { q: "Can I cancel my subscription at any time?", a: "Yes. You can cancel your Pro or School subscription at any time from your account settings. You'll retain access until the end of your billing period." },
          { q: "How do I pay? Is Paystack/Flutterwave supported?", a: "We support all major Nigerian payment methods including Paystack, Flutterwave, bank transfer, and USSD payments. No foreign card required." },
          { q: "What happens when my free limit runs out?", a: "Your access to past questions is paused until the next month, but you can upgrade to Pro at any time to get unlimited access immediately." },
          { q: "Is the annual plan significantly cheaper?", a: "Yes! The annual Pro plan is billed at ₦21,000 per year (equivalent to ₦1,750/month) — a saving of 30% compared to monthly billing." },
          { q: "Can a school pay by invoice?", a: "Absolutely. Schools and institutions can request invoice-based billing. Contact our sales team via the School plan button above and we'll set it up for you." },
        ].map((item) => (
          <div key={item.q} className={styles.faqItem}>
            <div className={styles.faqQuestion}>{item.q}</div>
            <div className={styles.faqAnswer}>{item.a}</div>
          </div>
        ))}
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
