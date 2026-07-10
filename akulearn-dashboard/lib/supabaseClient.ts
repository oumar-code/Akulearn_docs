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

export const isSupabaseConfigured = Boolean(supabaseUrl && supabaseAnonKey);

export const supabaseConfigError = isSupabaseConfigured
  ? null
  : '[Supabase] NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY are required for browser auth. ' +
    'In Vercel/project env vars, keep the same values but use NEXT_PUBLIC_ prefixed names.';

export const supabase = createClient(
  supabaseUrl ?? 'https://placeholder.supabase.co',
  supabaseAnonKey ?? 'placeholder-anon-key',
  {
    auth: {
      detectSessionInUrl: true,
      persistSession: true,
      autoRefreshToken: true,
    },
  }
);
