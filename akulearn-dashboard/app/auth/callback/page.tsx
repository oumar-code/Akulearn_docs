"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { isSupabaseConfigured, supabase, supabaseConfigError } from "../../../lib/supabaseClient";

const sanitizeNextRoute = (route: string | null) => {
  if (!route) return "/dashboard";
  if (!route.startsWith("/") || route.startsWith("//")) return "/dashboard";
  return route;
};

export default function AuthCallbackPage() {
  const router = useRouter();
  const [status, setStatus] = useState(
    isSupabaseConfigured ? "Finalizing sign-in..." : "Cannot complete sign-in."
  );
  const [error, setError] = useState(
    isSupabaseConfigured ? "" : (supabaseConfigError ?? "Supabase is not configured.")
  );
  const attemptsRef = useRef(0);
  const navigatedRef = useRef(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (!isSupabaseConfigured) return;

    let isMounted = true;
    const maxAttempts = 10;
    const nextRoute = sanitizeNextRoute(new URLSearchParams(window.location.search).get("next"));

    const navigateOnce = () => {
      if (navigatedRef.current) return;
      navigatedRef.current = true;
      router.replace(nextRoute);
    };

    const finishIfSession = async () => {
      const { data, error: sessionError } = await supabase.auth.getSession();
      if (!isMounted) return;

      if (sessionError) {
        setError(sessionError.message);
        setStatus("Unable to complete authentication.");
        return;
      }

      if (data.session) {
        navigateOnce();
        return;
      }

      attemptsRef.current += 1;
      if (attemptsRef.current >= maxAttempts) {
        setStatus("No active session found.");
        setError("Login link did not create a session. Request a new magic link and verify redirect URLs in Supabase.");
        return;
      }

      timeoutRef.current = window.setTimeout(finishIfSession, 500);
    };

    const { data: authSubscription } = supabase.auth.onAuthStateChange((event, session) => {
      if (!isMounted) return;
      if (event === "SIGNED_IN" && session) {
        navigateOnce();
      }
    });

    finishIfSession();

    return () => {
      isMounted = false;
      if (timeoutRef.current) {
        window.clearTimeout(timeoutRef.current);
      }
      authSubscription.subscription.unsubscribe();
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
