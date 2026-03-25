# Login & Dashboard Access

This page explains where Aku Platform team members log in and which dashboard they land on after authentication.

## Login URL

All team members sign in at:

**[https://app.akulearn.com](https://app.akulearn.com)**

Authentication is powered by **Supabase Auth**. After a successful login the platform reads each user's `app_metadata.role` and redirects them to their assigned dashboard automatically.

## First Login

1. Navigate to **[https://app.akulearn.com](https://app.akulearn.com)**.
2. Enter your provisioned **email address** and the **temporary password** you received.
3. You will be prompted to set a new password immediately — do this before continuing.
4. Once your password is changed you will be redirected to your personal dashboard.

> **Important:** Temporary passwords are shared via an encrypted channel. If you have not received yours, contact the System Administrator.

## Team Dashboard Mapping

| Team Member | Email | Role | Dashboard |
|---|---|---|---|
| Umar Abubakar | umarabubakarg2018@gmail.com | System Designer, Project Manager & Technical Lead | [Super Admin](super_admin_dashboard.md) |
| Munira Abubakar | muniraabubakar6@gmail.com | Head of Product & External Engagement | [Munira Dashboard](munira_dashboard.md) |
| Zakwan Lawali | zakawanulawali2017@gmail.com | Head of Skill Acquisition & Vocational Training | [Zakwan Dashboard](zakwan_dashboard.md) |
| Balkisu Sani Kaura | kaurabalkisusani@gmail.com | Head of Finance & Content Management | [Balkisu Dashboard](balkisu_dashboard.md) |
| Hauwau Abubakar | hauwauabubakargusau2009@gmail.com | Exam Prep & Access Coordinator | [Hauwau Dashboard](hauwau_dashboard.md) |

## How Role-Based Routing Works

1. **Login** — the user submits their email and password at the login page.
2. **Token issued** — Supabase verifies the credentials and returns a signed JWT that includes `app_metadata.role`.
3. **Role check** — the platform frontend reads the role from the JWT.
4. **Redirect** — the user is sent to the dashboard that corresponds to their role.

| `app_metadata.role` | Dashboard |
|---|---|
| `super_admin` | Super Admin Dashboard |
| `product_brand_lead` | Munira Dashboard |
| `skill_acquisition` | Zakwan Dashboard |
| `finance_content` | Balkisu Dashboard |
| `hauwau_special` | Hauwau Dashboard |

All roles also include access to **Aku Workspace**.

## Resetting Your Password

If you forget your password, click **"Forgot password?"** on the login page and enter your email address. Supabase will send a password-reset link to your inbox.

## Further Reading

- [Team Provisioning](team_provisioning.md) — how accounts are created and credentials are distributed.
- [Super Admin Dashboard](super_admin_dashboard.md) · [Munira Dashboard](munira_dashboard.md) · [Zakwan Dashboard](zakwan_dashboard.md) · [Balkisu Dashboard](balkisu_dashboard.md) · [Hauwau Dashboard](hauwau_dashboard.md)

---

For technical details on authentication configuration, see [`supabase_provision.py`](../../supabase_provision.py) and [`team.py`](../../team.py).
