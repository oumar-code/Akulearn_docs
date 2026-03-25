import React from "react";
import styles from "./pricing.module.css";

export default function PricingPage() {
  return (
    <main>
      {/* Converted from pricing.html */}
      <nav>
        <div className="container">
          <a href="/">Akudemy</a>
          <a href="/about">About</a>
          <a href="/blog">Blog</a>
        </div>
      </nav>
      <header>
        <div className="container">
          <h1>Simple, Flexible Pricing</h1>
          <p>Choose a plan that fits your goals—students and schools both welcome.</p>
        </div>
      </header>
      <section className="pricing">
        <div className="container grid">
          <div className="card">
            <h3>Free</h3>
            <p>For trying Akudemy</p>
            <div className="price">₦0<span>/month</span></div>
            <ul className="features">
              <li>100 practice questions</li>
              <li>Basic 3D models (5 topics)</li>
              <li>Progress tracking</li>
              <li>Offline access</li>
            </ul>
          </div>
          <div className="card featured">
            <span className="badge">Most Popular</span>
            <h3>Student Premium</h3>
            <p>Complete exam prep</p>
            <div className="price">₦1,500<span>/month</span></div>
            <ul className="features">
              <li>1,350+ practice questions</li>
              <li>All 3D models (unlimited)</li>
              <li>AI weak topic detection</li>
              <li>Readiness assessments</li>
              <li>Detailed analytics</li>
              <li>Priority support</li>
            </ul>
          </div>
          <div className="card">
            <h3>School License</h3>
            <p>For schools & teachers</p>
            <div className="price">₦500K<span>/year</span></div>
            <ul className="features">
              <li>Up to 500 students</li>
              <li>Teacher dashboard</li>
              <li>Class management</li>
              <li>Bulk device deployment</li>
              <li>Dedicated support</li>
            </ul>
          </div>
        </div>
      </section>
      <section className="details">
        <div className="container">
          <h2>Pricing Details</h2>
          <p>All plans include offline access, Nigerian curriculum alignment, and continuous content updates.</p>
          <div className={"grid " + styles.marginTop2rem}>
            <div className="card">
              <h4>Discounts & Partnerships</h4>
              <p>Special pricing for government programs, NGOs, and large school networks.</p>
            </div>
            <div className="card">
              <h4>Device Bundles</h4>
              <p>Bundle Akudemy with solar-powered tablets and projectors via Aku DaaS.</p>
            </div>
            <div className="card">
              <h4>Custom Content</h4>
              <p>We can add local language content or custom learning paths for schools.</p>
            </div>
          </div>
        </div>
      </section>
      <section className="cta">
        <div className="container">
          <h2>Ready to get started?</h2>
          <p>Start free or contact us for school licensing.</p>
          <a href="mailto:schools@akudemy.com">Contact Sales</a>
        </div>
      </section>
      <footer>
        <div className="container">© 2026 Akudemy • Pricing built for Nigerian students</div>
      </footer>
    </main>
  );
}
