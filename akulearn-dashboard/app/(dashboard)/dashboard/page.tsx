"use client";


import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "../../../lib/supabaseClient";
import styles from "./dashboard.module.css";

import dynamic from "next/dynamic";
const QuizTopicManagement = dynamic(() => import("../content/quiz-topic-management").then(mod => mod.default), { ssr: false });
const StudentTeacherDashboard = dynamic(() => import("../content/student-teacher-dashboard").then(mod => mod.default), { ssr: false });
const UserManagementPanel = dynamic(() => import("../admin/user-management").then(mod => mod.default), { ssr: false });
const CourseContentPanel = dynamic(() => import("../content/course-content-panel").then(mod => mod.default), { ssr: false });
const CourseManagementPanel = dynamic(() => import("../content/course-management").then(mod => mod.default), { ssr: false });
const TraineeProgressTracker = dynamic(() => import("../content/trainee-progress").then(mod => mod.default), { ssr: false });
const BudgetManagementPanel = dynamic(() => import("../content/budget-management").then(mod => mod.default), { ssr: false });
const ContentPipelinePanel = dynamic(() => import("../content/content-pipeline").then(mod => mod.default), { ssr: false });
const SystemAnalyticsDashboard = dynamic(() => import("../admin/system-analytics").then(mod => mod.default), { ssr: false });
const AuditLogsViewer = dynamic(() => import("../admin/audit-logs").then(mod => mod.default), { ssr: false });
const ProductRoadmapKanban = dynamic(() => import("../product/roadmap-kanban").then(mod => mod.default), { ssr: false });
const MarketingAnalytics = dynamic(() => import("../product/marketing-analytics").then(mod => mod.default), { ssr: false });
const MediaKitPanel = dynamic(() => import("../product/media-kit").then(mod => mod.default), { ssr: false });

// Map team emails to roles and accesses (real emails from supabase_provision.py)
type TeamMember = {
  email: string;
  name: string;
  role: string;
  dashboard: string;
  accesses: string[];
};
const TEAM_MEMBERS: TeamMember[] = [
  {
    email: "umarabubakarg2018@gmail.com",
    name: "Umar Abubakar",
    role: "System Designer, Project Manager & Technical Lead",
    dashboard: "super_admin",
    accesses: [
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
    email: "muniraabubakar6@gmail.com",
    name: "Munira Abubakar",
    role: "Head of Product & External Engagement",
    dashboard: "product_brand_lead",
    accesses: [
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
    email: "zakawanulawali2017@gmail.com",
    name: "Zakwan Lawali",
    role: "Head of Skill Acquisition & Vocational Training",
    dashboard: "skill_acquisition",
    accesses: [
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
    email: "kaurabalkisusani@gmail.com",
    name: "Balkisu Sani Kaura",
    role: "Head of Finance & Content Management",
    dashboard: "finance_content",
    accesses: [
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
    email: "hauwauabubakargusau2009@gmail.com",
    name: "Hauwau Abubakar",
    role: "Exam Prep & Access Coordinator",
    dashboard: "hauwau_special",
    accesses: [
      "hauwau_dashboard",
      "aku_workspace",
      "jamb_english",
      "jamb_biology",
      "jamb_physics",
      "jamb_chemistry",
      "topic_quiz",
      "medicine_pathway",
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
];

interface SupabaseUser {
  email?: string;
  id?: string;
  // Add other expected user properties as needed
}

export default function DashboardPage() {
  const [user, setUser] = useState<SupabaseUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [member, setMember] = useState<TeamMember | null>(null);
  const router = useRouter();

  useEffect(() => {
    const getUser = async () => {
      const { data } = await supabase.auth.getUser();
      if (data?.user) {
        setUser(data.user);
        if (data.user.email) {
          const found = TEAM_MEMBERS.find(m => m.email.toLowerCase() === data.user.email!.toLowerCase()) || null;
          setMember(found);
        } else {
          setMember(null);
        }
      } else {
        router.push("/login");
      }
      setLoading(false);
    };
    getUser();
  }, [router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  if (!member) {
    return (
      <div className={styles.centeredBox}>
        <h2>Welcome</h2>
        <p>Email: {user.email}</p>
        <p className={styles.errorText}>You do not have a team dashboard assigned. Please contact admin.</p>
        <button onClick={async () => { await supabase.auth.signOut(); router.push("/login"); }}>
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <div className={styles.centeredBox}>
      <h2>Welcome, {member.name}</h2>
      <p>Email: {user.email}</p>
      <p><b>Role:</b> {member.role}</p>
      <p><b>Dashboard:</b> {member.dashboard}</p>
      <div>
        <b>Accesses:</b>
        <ul>
          {member.accesses.map((acc: string) => (
            <li key={acc}>{acc}</li>
          ))}
        </ul>
      </div>

      {/* Custom panels/features for each role */}
      {member.dashboard === "super_admin" && (
        <>
          <div className={styles.panelSuperAdmin}>
            <h3>Super Admin Panel</h3>
            <ul>
              <li>System analytics dashboard (user stats, system health)</li>
              <li>User management (invite, remove, assign roles)</li>
              <li>Content management overview</li>
              <li>System settings (feature toggles, integrations)</li>
              <li>Audit logs viewer</li>
              <li>AI/ML/DevOps status panels</li>
            </ul>
          </div>
          <SystemAnalyticsDashboard />
          <UserManagementPanel />
          <AuditLogsViewer />
        </>
      )}
      {member.dashboard === "product_brand_lead" && (
        <>
          <div className={styles.panelProductBrand}>
            <h3>Product & Brand Lead Panel</h3>
            <ul>
              <li>Product roadmap editor</li>
              <li>Marketing analytics (campaign stats, engagement)</li>
              <li>Pitch/investor deck upload & sharing</li>
              <li>Demo materials library</li>
              <li>Social media hub (scheduled posts, analytics)</li>
              <li>Media kit download</li>
            </ul>
          </div>
          <ProductRoadmapKanban />
          <MarketingAnalytics />
          <MediaKitPanel />
        </>
      )}
      {member.dashboard === "skill_acquisition" && (
        <>
          <div className={styles.panelSkillAcquisition}>
            <h3>Skill Acquisition & Vocational Training Panel</h3>
            <ul>
              <li>Course management (add/edit courses)</li>
              <li>Trainee progress tracker</li>
              <li>Certification management</li>
              <li>Partner institution management</li>
              <li>Vocational program analytics</li>
            </ul>
          </div>
          <CourseManagementPanel />
          <TraineeProgressTracker />
          <CourseContentPanel />
        </>
      )}
      {member.dashboard === "finance_content" && (
        <>
          <div className={styles.panelFinanceContent}>
            <h3>Finance & Content Management Panel</h3>
            <ul>
              <li>Budget management tools</li>
              <li>Financial reporting dashboard</li>
              <li>Content pipeline (submission, approval, publishing)</li>
              <li>Analytics for content performance</li>
              <li>Audit logs for content changes</li>
            </ul>
          </div>
          <BudgetManagementPanel />
          <ContentPipelinePanel />
          <CourseContentPanel />
        </>
      )}
      {member.dashboard === "hauwau_special" && (
        <>
          <div className={styles.panelExamPrep}>
            <h3>Exam Prep & Access Coordinator Panel</h3>
            <ul>
              <li>JAMB/WAEC/NECO subject dashboards</li>
              <li>Student/teacher dashboard access</li>
              <li>Quiz and topic management</li>
              <li>Medicine pathway tracker</li>
              <li>School admin dashboard</li>
            </ul>
          </div>
          <QuizTopicManagement />
          <StudentTeacherDashboard />
        </>
      )}

      {/* General features for all */}
      <div className={styles.generalFeaturesBox}>
        <h4>General Features</h4>
        <ul>
          <li>Notifications panel</li>
          <li>Profile/settings page</li>
          <li>Quick links to onboarding/training resources</li>
          <li>Secure sign out</li>
        </ul>
      </div>

      <button className={styles.signOutBtn} onClick={async () => { await supabase.auth.signOut(); router.push("/login"); }}>
        Sign Out
      </button>
    </div>
  );
}
