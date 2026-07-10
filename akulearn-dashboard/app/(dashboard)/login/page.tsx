"use client";
import { useEffect, useState } from "react";
import styles from "./login.module.css";
import { isSupabaseConfigured, supabase, supabaseConfigError } from "../../../lib/supabaseClient";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const checkExistingSession = async () => {
      if (!isSupabaseConfigured) return;
      const nextRoute = new URLSearchParams(window.location.search).get("next") || "/dashboard";
      const { data } = await supabase.auth.getSession();
      if (data.session) {
        router.push(nextRoute);
      }
    };
    checkExistingSession();
  }, [router]);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setMessage("");
    setError("");

    if (!isSupabaseConfigured) {
      setError(supabaseConfigError ?? "Supabase is not configured.");
      return;
    }

    setLoading(true);
    const nextRoute = new URLSearchParams(window.location.search).get("next") || "/dashboard";
    const callbackUrl = `${window.location.origin}/auth/callback?next=${encodeURIComponent(nextRoute)}`;
    const { error: signInError } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: callbackUrl },
    });
    setLoading(false);

    if (signInError) {
      setError(signInError.message);
      return;
    }

    setMessage("Magic link sent. Open your email and continue sign-in from the link.");
  };

  return (
    <div className={styles.loginWrapper}>
      <form onSubmit={handleLogin} className={styles.loginForm}>
        <div className={styles.loginLogo}>🎓</div>
        <h2 className={styles.loginTitle}>Akulearn Dashboard</h2>
        <p className={styles.loginSubtitle}>
          Team members and students — enter your registered email to receive a secure login link.
        </p>
        {!isSupabaseConfigured && (
          <div className={styles.loginError}>
            {supabaseConfigError}
          </div>
        )}
        <input
          type="email"
          placeholder="Enter your email address"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
          className={styles.loginInput}
        />
        <button type="submit" className={styles.loginButton} disabled={loading || !isSupabaseConfigured}>
          {loading ? "Sending..." : "Send Magic Link"}
        </button>
        {error && <div className={styles.loginError}>{error}</div>}
        {message && <div className={styles.loginMessage}>{message}</div>}
        <div className={styles.loginHint}>
          <strong>Team members:</strong> use your assigned team email.<br />
          <strong>Students:</strong> use the email provided during registration.
        </div>
      </form>
    </div>
  );
}
