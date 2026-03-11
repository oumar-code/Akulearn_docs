import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? 'https://placeholder.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? 'placeholder-anon-key';

if (typeof window !== 'undefined' && !process.env.NEXT_PUBLIC_SUPABASE_URL) {
  console.error(
    'Missing NEXT_PUBLIC_SUPABASE_URL. Set this environment variable in your Vercel project dashboard.'
  );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
