"""
Akulearn Supabase User Provisioning Script

This is the canonical file for provisioning Akulearn core team members in
Supabase. Running it creates each user in your Supabase project, assigns
their role via app_metadata, generates a secure temporary password that
must be changed on first login, and e-mails the credentials to each user
via Resend.

Usage:
    python supabase_provision.py

Required environment variables (add to .env and never commit .env):
    SUPABASE_URL              - Your Supabase project URL
                                e.g. https://xxxx.supabase.co
    SUPABASE_SERVICE_ROLE_KEY - Service-role key from the Supabase dashboard
                                (Project Settings > API > service_role).
                                NEVER use the anon key here.

Optional environment variables:
    RESEND_API_KEY   - Resend API key for sending credential emails.
                       If omitted, email delivery is skipped.
    RESEND_FROM_EMAIL - "From" address used for credential emails.
                        Defaults to onboarding@akulearn.com.

Dry-run mode:
    If SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing, the script
    runs in dry-run mode: it prints the full team roster and sample
    credentials to the console without touching Supabase or sending email.
"""

import json
import os
import secrets
import string
import urllib.error
import urllib.request
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# .env loader — reads key=value pairs from a .env file into os.environ.
# Only sets variables that are not already present in the environment so that
# shell-level overrides always take precedence.
# ---------------------------------------------------------------------------

def _load_dotenv(path: str = ".env") -> None:
    """Load environment variables from *path* (.env) if it exists."""
    try:
        with open(path) as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                # Strip matching outer quotes from the value (e.g. KEY="val" or KEY='val').
                # partition("=") is used so values that contain "=" (e.g. base64) are preserved.
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                if key and key not in os.environ:
                    os.environ[key] = value
    except FileNotFoundError:
        pass

# ---------------------------------------------------------------------------
# Team roster — authoritative source of truth for Supabase provisioning
# ---------------------------------------------------------------------------
TEAM = [
    {
        "name": "Umar Abubakar",
        "role": "System Designer, Project Manager & Technical Lead",
        "responsibility": (
            "Overall system design, project management, and technical team leadership "
            "spanning AIOps, MLOps, DevOps, and hardware integrations"
        ),
        "email": "umarabubakarg2018@gmail.com",
        "supabase_role": "super_admin",
        "dashboard": "super_admin",
    },
    {
        "name": "Munira Abubakar",
        "role": "Head of Product & External Engagement",
        "responsibility": (
            "Product management, social media, brand representation, "
            "investor pitches, partnership presentations, and external engagements. "
            "Upcoming pitch scheduled for mid-March."
        ),
        "email": "muniraabubakar6@gmail.com",
        "supabase_role": "product_brand_lead",
        "dashboard": "product_brand_lead",
    },
    {
        "name": "Zakwan Lawali",
        "role": "Head of Skill Acquisition & Vocational Training",
        "responsibility": (
            "Leading the Aku platform's skill acquisition and vocational skills "
            "training programme — equivalent to the 3MTT initiative but fully "
            "integrated within the Aku ecosystem"
        ),
        "email": "zakawanulawali2017@gmail.com",
        "supabase_role": "skill_acquisition",
        "dashboard": "skill_acquisition",
    },
    {
        "name": "Balkisu Sani Kaura",
        "role": "Head of Finance & Content Management",
        "responsibility": (
            "Financial planning and oversight, content strategy, "
            "content creation pipelines, and budget management across departments"
        ),
        "email": "kaurabalkisusani@gmail.com",
        "supabase_role": "finance_content",
        "dashboard": "finance_content",
    },
    {
        "name": "Hauwau Abubakar",
        "role": "Exam Prep & Access Coordinator",
        "responsibility": (
            "JAMB exam preparation in English, Biology, Physics, and Chemistry "
            "targeting a Medicine & Surgery admission. Includes post-topic quizzes "
            "that mimic JAMB exam standard, cross-dashboard access oversight, "
            "and student support."
        ),
        "email": "hauwauabubakargusau2009@gmail.com",
        "supabase_role": "hauwau_special",
        "dashboard": "hauwau_special",
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def generate_temp_password(length: int = 16) -> str:
    """Return a cryptographically secure temporary password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def provision_user(supabase_url: str, service_key: str, member: dict) -> dict:
    """
    Create a team member in Supabase via the Admin API.

    Returns a result dict that includes the generated temporary password
    so it can be shared with the user securely.
    """
    temp_password = generate_temp_password()

    if not supabase_url:
        raise ValueError("SUPABASE_URL must be a non-empty string")

    payload = json.dumps(
        {
            "email": member["email"],
            "password": temp_password,
            "email_confirm": True,
            "user_metadata": {
                "name": member["name"],
                "role": member["role"],
                "dashboard": member["dashboard"],
                "aku_workspace": True,
                **(
                    {
                        "jamb_subjects": ["english", "biology", "physics", "chemistry"],
                        "study_goal": "medicine",
                        "topic_quiz_enabled": True,
                        "quiz_standard": "jamb",
                    }
                    if member.get("supabase_role") == "hauwau_special"
                    else {}
                ),
            },
            "app_metadata": {
                "role": member["supabase_role"],
            },
        }
    ).encode()

    req = urllib.request.Request(
        f"{supabase_url}/auth/v1/admin/users",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "apikey": service_key,
            "Authorization": f"Bearer {service_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            return {
                "name": member["name"],
                "email": member["email"],
                "role": member["role"],
                "dashboard": member["dashboard"],
                "temp_password": temp_password,
                "user_id": result.get("id", ""),
                "status": "created",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        return {
            "name": member["name"],
            "email": member["email"],
            "role": member["role"],
            "dashboard": member["dashboard"],
            "temp_password": temp_password,
            "status": f"error ({exc.code}): {body}",
        }


def send_credentials_email(
    resend_api_key: str,
    from_email: str,
    result: dict,
) -> str:
    """
    Send login credentials to a newly provisioned team member via Resend.

    Returns "email_sent", "email_skipped" (no API key), or an error string.
    """
    if not resend_api_key:
        return "email_skipped (no RESEND_API_KEY)"

    subject = "Welcome to Akulearn — Your Dashboard Access Credentials"
    html_body = f"""
<html>
<body style="font-family: sans-serif; color: #222;">
  <h2>Welcome to the Akulearn Platform, {result['name']}!</h2>
  <p>Your account has been created. Please use the credentials below to log in
  and <strong>change your password immediately</strong> after your first login.</p>
  <table style="border-collapse: collapse; margin-top: 16px;">
    <tr><td style="padding: 6px 12px; font-weight: bold;">Email</td>
        <td style="padding: 6px 12px;">{result['email']}</td></tr>
    <tr><td style="padding: 6px 12px; font-weight: bold;">Temporary Password</td>
        <td style="padding: 6px 12px; font-family: monospace;">{result.get('temp_password', '')}</td></tr>
    <tr><td style="padding: 6px 12px; font-weight: bold;">Role</td>
        <td style="padding: 6px 12px;">{result['role']}</td></tr>
    <tr><td style="padding: 6px 12px; font-weight: bold;">Dashboard</td>
        <td style="padding: 6px 12px;">{result['dashboard']}</td></tr>
  </table>
  <p style="margin-top: 20px; color: #c00;">
    ⚠ Keep this email confidential. Change your password on first login —
    this temporary password expires after 24 hours.
  </p>
  <p>— The Akulearn Team</p>
</body>
</html>
"""

    payload = json.dumps(
        {
            "from": from_email,
            "to": [result["email"]],
            "subject": subject,
            "html": html_body,
        }
    ).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {resend_api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as response:
            response.read()  # consume the response body
            return "email_sent"
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        return f"email_error ({exc.code}): {body}"


def print_credentials(results: list) -> None:
    """Pretty-print provisioned credentials to the console."""
    width = 72
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    print("\n" + "=" * width)
    print("  AKULEARN PLATFORM — TEAM LOGIN CREDENTIALS")
    print(f"  Generated : {now}")
    print("=" * width)
    for r in results:
        print(f"\n  Name      : {r['name']}")
        print(f"  Role      : {r['role']}")
        print(f"  Dashboard : {r['dashboard']}")
        print(f"  Email     : {r['email']}")
        print(f"  Temp Pass : {r.get('temp_password', 'N/A')}")
        print(f"  Status    : {r['status']}")
        if "email_status" in r:
            print(f"  Email     : {r['email_status']}")
    print("\n" + "=" * width)
    print("  ⚠  Share credentials via encrypted email or a secure channel.")
    print("  ⚠  Each user must change their password immediately after login.")
    print("=" * width + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _load_dotenv()
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    resend_api_key = os.environ.get("RESEND_API_KEY", "")
    from_email = os.environ.get("RESEND_FROM_EMAIL", "onboarding@akulearn.com")

    if not supabase_url or not service_key:
        print(
            "\n[DRY RUN] SUPABASE_URL and/or SUPABASE_SERVICE_ROLE_KEY not set.\n"
            "Displaying team roster with sample credentials — no users will be created.\n"
        )
        dry_results = [
            {
                "name": m["name"],
                "email": m["email"],
                "role": m["role"],
                "dashboard": m["dashboard"],
                "temp_password": generate_temp_password(),
                "status": "dry-run (not provisioned)",
            }
            for m in TEAM
        ]
        print_credentials(dry_results)
    else:
        print(f"Provisioning {len(TEAM)} team members in Supabase…")
        results = [provision_user(supabase_url, service_key, m) for m in TEAM]

        if resend_api_key:
            print(f"Sending credential emails via Resend…")
            for r in results:
                if r.get("status") == "created":
                    r["email_status"] = send_credentials_email(
                        resend_api_key, from_email, r
                    )

        print_credentials(results)
