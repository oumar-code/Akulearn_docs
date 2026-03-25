"use client";
import { useState } from "react";
import Link from "next/link";
import styles from "./register.module.css";
import { supabase } from "../../lib/supabaseClient";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);
    const { error: signUpError } = await supabase.auth.signUp({ email, password });
    setLoading(false);
    if (signUpError) {
      setError(signUpError.message);
    } else {
      setMessage("Registration successful! Please check your email to confirm your account.");
    }
  };

  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <Link href="/" className={styles.navLogo}>Aku<span>demy</span></Link>
        <Link href="/login" className={styles.navLink}>Already have an account? Log in</Link>
      </nav>
      <div className={styles.container}>
        <h2>Sign Up Free</h2>
        <p className={styles.subtitle}>No credit card required. Start preparing for JAMB today.</p>
        <form onSubmit={handleRegister}>
          <label className={styles.label} htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            className={styles.input}
            value={email}
            onChange={e => setEmail(e.target.value)}
            placeholder="you@example.com"
            required
          />
          <label className={styles.label} htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            className={styles.input}
            value={password}
            onChange={e => setPassword(e.target.value)}
            placeholder="At least 8 characters"
            required
          />
          {error && <div className={styles.error}>{error}</div>}
          {message && <div className={styles.success}>{message}</div>}
          <button type="submit" className={styles.button} disabled={loading}>
            {loading ? "Creating account…" : "Create Free Account"}
          </button>
        </form>
        <p className={styles.loginLink}>Already have an account? <Link href="/login">Log in</Link></p>
      </div>
    </div>
  );
}
