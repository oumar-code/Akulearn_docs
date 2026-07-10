# Dashboard Login Troubleshooting

Use this guide when the dashboard login page accepts input but quickly shows an error, or when a magic-link login does not complete.

## 1) Verify required environment variables

For browser-based Supabase auth in Next.js, these variables must be present in your deployment and local environment:

- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

If you only set `SUPABASE_URL` / `SUPABASE_ANON_KEY`, client-side auth can fail because those values are not exposed to the browser bundle.

## 2) Confirm Supabase Auth redirect URLs

In Supabase Dashboard → Authentication → URL Configuration:

- Set **Site URL** to your frontend origin (for example, `https://app.akulearn.com`).
- Add a redirect URL for callback handling:
  - `https://app.akulearn.com/auth/callback`
  - Local dev example: `http://localhost:3000/auth/callback`

## 3) Magic-link callback behavior

The login flow should complete through `/auth/callback` and then route to `/dashboard`.  
If users are redirected to an error page:

1. Open browser dev tools and confirm no missing `NEXT_PUBLIC_SUPABASE_*` variables.
2. Check that the callback URL in Supabase exactly matches your app origin.
3. Re-request a fresh magic link and avoid older/expired links.

## 4) Quick validation checklist

- [ ] `NEXT_PUBLIC_SUPABASE_URL` is set correctly
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY` is set correctly
- [ ] Supabase **Site URL** matches deployment domain
- [ ] Supabase redirect URL includes `/auth/callback`
- [ ] Fresh magic link was used

## Related docs

- [Login & Dashboard Access](platform_login.md)
- [Team Provisioning](team_provisioning.md)
