# Team Provisioning — Supabase Setup

`supabase_provision.py` is the authoritative script for onboarding the Akulearn core team into Supabase. It creates each member's account, assigns their role via `app_metadata`, and generates a secure temporary password that must be changed on first login.

## Team Roster

| Name | Role | Email | Dashboard |
|---|---|---|---|
| Umar Abubakar | Founder & Technical Lead | umar@akulearn.com | `super_admin` |
| Zakwan Lawali | Backend & DevOps Engineer | zakwan@akulearn.com | `it_support` |
| Munira Abubakar | Brand Ambassador & Platform Spokesperson | munira@akulearn.com | `pitch_prep` |
| Balkisu Sani | Community & NGO Relations Lead | balkisu@akulearn.com | `ngo_partner` |
| Hauwau Abubakar | Exam Prep & Access Coordinator | hauwau@akulearn.com | `hauwau_special` |

## Prerequisites

1. A Supabase project with Row-Level Security (RLS) configured for role-based access.
2. The **service-role key** from **Project Settings → API** in the Supabase dashboard. Do **not** use the anon key.
3. Python 3.10+ (no third-party dependencies — uses only the standard library).

## Setup

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

> **Security**: `.env` is listed in `.gitignore` and must never be committed.

## Running the Script

```bash
python supabase_provision.py
```

### Dry-run mode

If the environment variables are not set, the script runs in **dry-run mode**: it prints the full team roster with sample credentials to the console without creating any Supabase accounts.

### Live mode

When both `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are set, the script calls the Supabase Admin API (`/auth/v1/admin/users`) to:

1. Create the user account with `email_confirm: true`.
2. Set `user_metadata` (display name, role label, dashboard key).
3. Set `app_metadata.role` — the field your RLS policies and client-side guards should check.
4. Generate a cryptographically secure 16-character temporary password.

The console output lists each member's credentials. **Share these via an encrypted channel** (e.g., encrypted email or a secure password manager share link).

## Supabase Role Mapping

| `app_metadata.role` | Platform access |
|---|---|
| `super_admin` | Full platform access — system design, infra, team management |
| `it_support` | Server/deployment management, monitoring, logs |
| `pitch_prep` | Pitch decks, demo materials, investor docs, media kit |
| `ngo_partner` | Community engagement, partner analytics, school outreach |
| `hauwau_special` | JAMB/WAEC/NECO prep + cross-dashboard coordinator access |

## Security Notes

- Temporary passwords are generated with Python's `secrets` module (CSPRNG) and are never stored in the repository.
- Each user **must** change their password on first login.
- Revoke and rotate the `SUPABASE_SERVICE_ROLE_KEY` immediately if it is ever exposed.
- The service-role key bypasses RLS — treat it like a root credential.

---

For the full team configuration, see [`team.py`](../../team.py) and [`supabase_provision.py`](../../supabase_provision.py).
