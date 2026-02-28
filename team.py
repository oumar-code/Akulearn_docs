"""
Akulearn Team Members and Dashboard Configurations

This file defines the Akulearn core team members, their roles, and their
respective dashboard access configurations within the platform.
"""

# Team member definitions
TEAM = [
    {
        "name": "Umar Abubakar",
        "role": "System Designer, Project Manager & Technical Lead",
        "dashboard": "super_admin",
        "accesses": [
            "super_admin_dashboard",
            "aku_workspace",
            "analytics",
            "user_management",
            "content_management",
            "system_settings",
            "audit_logs",
            "aiops",
            "mlops",
            "devops",
            "hardware_integrations",
            "onboarding_training",
        ],
    },
    {
        "name": "Munira Abubakar",
        "role": "Head of Product & External Engagement",
        "dashboard": "product_brand_lead",
        "accesses": [
            "product_brand_dashboard",
            "aku_workspace",
            "product_roadmap",
            "pitch_deck",
            "investor_deck",
            "demo_materials",
            "marketing_analytics",
            "social_media_hub",
            "media_kit",
            "presentation_tools",
            "platform_overview",
            "onboarding_training",
        ],
    },
    {
        "name": "Zakwan Lawali",
        "role": "Head of Skill Acquisition & Vocational Training",
        "dashboard": "skill_acquisition",
        "accesses": [
            "skill_acquisition_dashboard",
            "aku_workspace",
            "course_management",
            "vocational_programmes",
            "trainee_progress",
            "certification_management",
            "partner_institutions",
            "analytics",
            "content_management",
            "onboarding_training",
        ],
    },
    {
        "name": "Balkisu Sani Kaura",
        "role": "Head of Finance & Content Management",
        "dashboard": "finance_content",
        "accesses": [
            "finance_content_dashboard",
            "aku_workspace",
            "budget_management",
            "financial_reporting",
            "content_pipeline",
            "content_approval",
            "content_management",
            "analytics",
            "audit_logs",
            "onboarding_training",
        ],
    },
    {
        "name": "Hauwau Abubakar",
        "role": "Exam Prep & Access Coordinator",
        "dashboard": "hauwau_special",
        "accesses": [
            "hauwau_dashboard",
            "aku_workspace",
            "jamb",
            "waec",
            "neco",
            "student_dashboard",
            "teacher_dashboard",
            "content_management",
            "analytics",
            "school_admin_dashboard",
            "onboarding_training",
        ],
    },
]


def get_member(name: str) -> dict | None:
    """Return the team member record matching the given name, or None."""
    for member in TEAM:
        if member["name"].lower() == name.lower():
            return member
    return None


def get_dashboard(name: str) -> str | None:
    """Return the dashboard key for the given team member name, or None."""
    member = get_member(name)
    return member["dashboard"] if member else None


def get_accesses(name: str) -> list[str]:
    """Return the list of access keys for the given team member name."""
    member = get_member(name)
    return member["accesses"] if member else []


if __name__ == "__main__":
    print("Akulearn Team Members")
    print("=" * 40)
    for member in TEAM:
        print(f"\nName    : {member['name']}")
        print(f"Role    : {member['role']}")
        print(f"Dashboard: {member['dashboard']}")
        print(f"Accesses: {', '.join(member['accesses'])}")
