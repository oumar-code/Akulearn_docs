# Team Provisioning — Supabase Setup & Onboarding Strategy

`supabase_provision.py` is the authoritative script for onboarding the Akulearn core team into Supabase. It creates each member's account, assigns their role via `app_metadata`, grants Aku Workspace access, and generates a secure temporary password that must be changed on first login.

## Team Roster

| Name | Role | Email | Dashboard |
|---|---|---|---|
| Umar Abubakar | System Designer, Project Manager & Technical Lead | umarabubakarg2018@gmail.com | `super_admin` |
| Munira Abubakar | Head of Product & External Engagement | muniraabubakar6@gmail.com | `product_brand_lead` |
| Zakwan Lawali | Head of Skill Acquisition & Vocational Training | zakawanulawali2017@gmail.com | `skill_acquisition` |
| Balkisu Sani Kaura | Head of Finance & Content Management | kaurabalkisusani@gmail.com | `finance_content` |
| Hauwau Abubakar | Exam Prep & Access Coordinator | hauwauabubakargusau2009@gmail.com | `hauwau_special` |

## Prerequisites

1. A Supabase project with Row-Level Security (RLS) configured for role-based access.
2. The **service-role key** from **Project Settings → API** in the Supabase dashboard. Do **not** use the anon key.
3. Python 3.10+ (no third-party dependencies — uses only the standard library).
4. A `.env` file in the project root populated from `.env.example` (see **Setup** below). The script loads it automatically at startup.

## Setup

Copy `.env.example` to `.env` and fill in your Supabase (and optionally Resend) credentials:

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Optional — required only if you want credential emails sent via Resend
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=onboarding@akulearn.com
```

The script calls `_load_dotenv()` at startup and reads values from `.env` automatically, so you do **not** need to export variables manually before running it.

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
2. Set `user_metadata` (display name, role label, dashboard key, `aku_workspace: true`).
3. Set `app_metadata.role` — the field your RLS policies and client-side guards should check.
4. Generate a cryptographically secure 16-character temporary password.

The console output lists each member's credentials. **Share these via an encrypted channel** (e.g., encrypted email or a secure password manager share link).

## Supabase Role Mapping

| `app_metadata.role` | Department head | Platform access |
|---|---|---|
| `super_admin` | Umar Abubakar | Full platform — system design, AIOps, MLOps, DevOps, hardware integrations, team management |
| `product_brand_lead` | Munira Abubakar | Product roadmap, social media hub, pitch decks, investor docs, marketing analytics, media kit |
| `skill_acquisition` | Zakwan Lawali | Courses, vocational programmes, trainee progress, certifications, partner institutions |
| `finance_content` | Balkisu Sani Kaura | Budget management, financial reporting, content pipeline, content approval, audit logs |
| `hauwau_special` | Hauwau Abubakar | JAMB/WAEC/NECO prep, cross-dashboard coordinator access, student and teacher dashboards |

All roles also include **`aku_workspace`** access.

## Onboarding Strategy — 2-Week Training Plan

Each team member undergoes a structured 2-week onboarding programme before taking full ownership of their department. The goal is to ensure every person can navigate their dashboard, simulate real workflows, and understand what is expected of them.

### Week 1 — Platform Orientation

| Day | Activity |
|---|---|
| Day 1 | Welcome session: Aku platform overview, mission, and vision briefing |
| Day 2 | Supabase login setup, first-login password change, dashboard walkthrough |
| Day 3 | Aku Workspace orientation: documents, projects, communication channels |
| Day 4 | Role-specific dashboard deep dive (guided tour of each module) |
| Day 5 | Hands-on simulation: complete a representative task in each dashboard module |

### Week 2 — Role Simulation & Readiness Assessment

| Day | Activity |
|---|---|
| Day 6–7 | Simulate a realistic end-to-end workflow in your department (e.g., Munira: draft and present a pitch; Zakwan: enrol a trainee cohort; Balkisu: create a budget report) |
| Day 8 | Cross-team session: understand how departments interact on the platform |
| Day 9 | Review onboarding checklist, flag gaps, and raise support tickets for anything not working |
| Day 10 | Light assessment quiz + sign-off: confirm readiness to operate independently |

### Sending Credentials

1. Run `python supabase_provision.py` (with env vars set) to create accounts and print credentials.
2. Send each user their **email**, **temporary password**, and the platform URL (`https://app.akulearn.com`) via an **encrypted email or secure channel**.
3. Instruct each user to change their password immediately on first login.
4. Confirm all five users can log in and see their custom dashboard before Day 1 of Week 1.

For a step-by-step login guide to share with team members, see [Login & Dashboard Access](platform_login.md).

## Security Notes

- Temporary passwords are generated with Python's `secrets` module (CSPRNG) and are never stored in the repository.
- Each user **must** change their password on first login.
- Revoke and rotate the `SUPABASE_SERVICE_ROLE_KEY` immediately if it is ever exposed.
- The service-role key bypasses RLS — treat it like a root credential.

---

For the full team configuration, see [`team.py`](../../team.py) and [`supabase_provision.py`](../../supabase_provision.py).

