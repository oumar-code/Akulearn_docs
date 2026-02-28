"""
Akulearn Team Members and Dashboard Configurations

This file defines the Akulearn core team members, their roles, and their
respective dashboard access configurations within the platform.
"""

# Team member definitions
TEAM = [
    {
        "name": "Umar Abubakar",
        "role": "Founder & Lead Engineer",
        "dashboard": "super_admin",
        "accesses": [
            "super_admin_dashboard",
            "analytics",
            "user_management",
            "content_management",
            "system_settings",
            "audit_logs",
            "jamb",
            "waec",
            "neco",
        ],
    },
    {
        "name": "Zakwan Lawali",
        "role": "Backend Engineer",
        "dashboard": "it_support",
        "accesses": [
            "it_support_dashboard",
            "system_monitoring",
            "server_management",
            "deployment",
            "logs",
        ],
    },
    {
        "name": "Munira Abubakar",
        "role": "Content & Curriculum Lead",
        "dashboard": "teacher",
        "accesses": [
            "teacher_dashboard",
            "content_management",
            "curriculum_design",
            "student_progress",
            "jamb",
            "waec",
        ],
    },
    {
        "name": "Balkisu Sani",
        "role": "Community & NGO Relations",
        "dashboard": "ngo_partner",
        "accesses": [
            "ngo_partner_dashboard",
            "community_engagement",
            "partner_analytics",
            "school_outreach",
        ],
    },
    {
        "name": "Hauwau Abubakar",
        "role": "Exam Prep & Access Coordinator",
        "dashboard": "hauwau_special",
        "accesses": [
            "hauwau_dashboard",
            "jamb",
            "waec",
            "neco",
            "student_dashboard",
            "teacher_dashboard",
            "content_management",
            "analytics",
            "school_admin_dashboard",
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
