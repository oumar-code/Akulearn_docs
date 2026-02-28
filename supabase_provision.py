"""
Akulearn Supabase User Provisioning Script

This is the canonical file for provisioning Akulearn core team members in
Supabase. Running it creates each user in your Supabase project, assigns
their role via app_metadata, and generates a secure temporary password that
must be changed on first login.

Usage:
    python supabase_provision.py

Required environment variables (add to .env and never commit .env):
    SUPABASE_URL              - Your Supabase project URL
                                e.g. https://xxxx.supabase.co
    SUPABASE_SERVICE_ROLE_KEY - Service-role key from the Supabase dashboard
                                (Project Settings > API > service_role).
                                NEVER use the anon key here.

Dry-run mode:
    If either environment variable is missing, the script runs in dry-run
    mode: it prints the full team roster and sample credentials to the
    console without touching Supabase.
"""

import json
import os
import secrets
import string
import urllib.error
import urllib.request
from datetime import datetime, timezone

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
    print("\n" + "=" * width)
    print("  ⚠  Share credentials via encrypted email or a secure channel.")
    print("  ⚠  Each user must change their password immediately after login.")
    print("=" * width + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

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
        print_credentials(results)
