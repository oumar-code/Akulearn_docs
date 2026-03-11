"use client";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabaseClient";
import styles from "./profile.module.css";

  type User = { email: string };
  const [user, setUser] = useState<User | null>(null);
  const [email, setEmail] = useState<string>("");
  const [message, setMessage] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    supabase.auth.getUser().then(({ data }) => {
      if (data?.user) {
        setUser(data.user as User);
        setEmail(data.user.email ?? "");
      }
    });
  }, []);

  const handleUpdateEmail = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const { error } = await supabase.auth.updateUser({ email });
    setMessage(error ? error.message : "Email updated! Check your inbox to confirm.");
  };

  const handleUpdatePassword = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const { error } = await supabase.auth.updateUser({ password });
    setMessage(error ? error.message : "Password updated!");
    setPassword("");
  };

  if (!user) return <div>Loading profile...</div>;

  return (
    <div className={styles.profilePanel}>
      <h2>Profile & Settings</h2>
      <form onSubmit={handleUpdateEmail} className={styles.profileForm}>
        <label htmlFor="profile-email">Email:</label>
        <input
          id="profile-email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className={styles.profileInput}
        />
        <button type="submit" className={styles.profileButton}>Update Email</button>
      </form>
      <form onSubmit={handleUpdatePassword} className={styles.profileForm}>
        <label htmlFor="profile-password">New Password:</label>
        <input
          id="profile-password"
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className={styles.profileInput}
        />
        <button type="submit" className={styles.profileButton}>Update Password</button>
      </form>
      <div className={styles.profileMessage}>{message}</div>
    </div>
  );
}
