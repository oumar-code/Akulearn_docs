import { createClient } from '@supabase/supabase-js';

// Next.js only bundles NEXT_PUBLIC_* variables into the browser bundle.
// Supabase calls in this app run client-side, so NEXT_PUBLIC_ prefix is required
// at runtime.  The SUPABASE_URL / SUPABASE_ANON_KEY fallbacks below help
// server-side build steps when only the plain-named variables are set.
const supabaseUrl =
  process.env.NEXT_PUBLIC_SUPABASE_URL ??
  process.env.SUPABASE_URL;

const supabaseAnonKey =
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ??
  process.env.SUPABASE_ANON_KEY;

if (typeof window !== 'undefined') {
  // Client-side: fail fast so misconfiguration is immediately obvious.
  if (!supabaseUrl || !supabaseAnonKey) {
    throw new Error(
      '[Supabase] NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY is not set. ' +
      'In your Vercel dashboard, rename SUPABASE_URL → NEXT_PUBLIC_SUPABASE_URL and ' +
      'SUPABASE_ANON_KEY → NEXT_PUBLIC_SUPABASE_ANON_KEY ' +
      '(same values, just the NEXT_PUBLIC_ prefix so Next.js exposes them to the browser).'
    );
  }
}

export const supabase = createClient(
  supabaseUrl ?? 'https://placeholder.supabase.co',
  supabaseAnonKey ?? 'placeholder-anon-key'
);
