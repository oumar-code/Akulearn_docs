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
    <form onSubmit={handleLogin} className={styles.loginForm}>
      <h2>Team Login</h2>
      <input
        type="email"
        placeholder="Your team email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
        className={styles.loginInput}
      />
      <button type="submit" className={styles.loginButton}>
        Send Magic Link
      </button>
      <div className={styles.loginMessage}>{message}</div>
    </form>
  );
}
