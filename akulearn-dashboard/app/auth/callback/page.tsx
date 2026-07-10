"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isSupabaseConfigured, supabase, supabaseConfigError } from "../../../lib/supabaseClient";

export default function AuthCallbackPage() {
  const router = useRouter();
  const [status, setStatus] = useState(
    isSupabaseConfigured ? "Finalizing sign-in..." : "Cannot complete sign-in."
  );
  const [error, setError] = useState(
    isSupabaseConfigured ? "" : (supabaseConfigError ?? "Supabase is not configured.")
  );

  useEffect(() => {
    if (!isSupabaseConfigured) return;

    let isMounted = true;
    let attempts = 0;
    const maxAttempts = 10;
    const nextRoute =
      new URLSearchParams(window.location.search).get("next") || "/dashboard";

    const finishIfSession = async () => {
      const { data, error: sessionError } = await supabase.auth.getSession();
      if (!isMounted) return;

      if (sessionError) {
        setError(sessionError.message);
        setStatus("Unable to complete authentication.");
        return;
      }

      if (data.session) {
        router.replace(nextRoute);
        return;
      }

      attempts += 1;
      if (attempts >= maxAttempts) {
        setStatus("No active session found.");
        setError("Login link did not create a session. Request a new magic link and verify redirect URLs in Supabase.");
        return;
      }

      window.setTimeout(finishIfSession, 500);
    };

    const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
      if (!isMounted) return;
      if (event === "SIGNED_IN" && session) {
        router.replace(nextRoute);
      }
    });

    finishIfSession();

    return () => {
      isMounted = false;
      authListener.subscription.unsubscribe();
    };
  }, [router]);

  return (
    <main style={{ maxWidth: "42rem", margin: "4rem auto", padding: "0 1rem", textAlign: "center" }}>
      <h1>Completing Login</h1>
      <p>{status}</p>
      {error && (
        <p style={{ color: "#b00020" }}>
          {error}
        </p>
      )}
    </main>
  );
}
