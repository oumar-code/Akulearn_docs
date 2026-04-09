"use client";
import { useState } from "react";
import styles from "./login.module.css";
import { supabase } from "../../../lib/supabaseClient";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const { error } = await supabase.auth.signInWithOtp({ email });
    setMessage(error ? error.message : "Check your email for the login link!");
    if (!error) {
      setTimeout(() => router.push("/dashboard"), 2000);
    }
  };

  return (
    <div className={styles.loginWrapper}>
      <form onSubmit={handleLogin} className={styles.loginForm}>
        <div className={styles.loginLogo}>🎓</div>
        <h2 className={styles.loginTitle}>Akulearn Dashboard</h2>
        <p className={styles.loginSubtitle}>
          Team members and students — enter your registered email to receive a secure login link.
        </p>
        <input
          type="email"
          placeholder="Enter your email address"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          className={styles.loginInput}
        />
        <button type="submit" className={styles.loginButton}>
          Send Magic Link
        </button>
        {message && <div className={styles.loginMessage}>{message}</div>}
        <div className={styles.loginHint}>
          <strong>Team members:</strong> use your assigned team email.<br />
          <strong>Students:</strong> use the email provided during registration.
        </div>
      </form>
    </div>
  );
}
