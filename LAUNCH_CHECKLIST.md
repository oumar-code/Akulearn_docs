# 🚀 Akulearn Launch Checklist & Quick Start

> **Status:** Pre-launch — preparing for student onboarding  
> **Audience:** Core team (Umar, Munira, Zakwan, Balkisu, Hauwau)

---

## Part 1 — LAUNCH CHECKLIST

### 1.1 Infrastructure
- [ ] Supabase project created and live (`SUPABASE_URL` confirmed)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` saved securely (never committed to git)
- [ ] Resend API key configured (`RESEND_API_KEY`) for credential emails
- [ ] Vercel deployment live (dashboard URL reachable from the internet)
- [ ] Custom domain configured on Vercel (optional for launch)
- [ ] Environment variables set in Vercel dashboard (`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`)

### 1.2 Team Credentials
- [ ] Run `python supabase_provision.py` with live Supabase credentials to provision all 5 team accounts
- [ ] Confirm each team member received their credential email from `onboarding@akulearn.com`
- [ ] Each team member logs in and changes their temporary password immediately
- [ ] Verify each team member can access their assigned dashboard:

| Name | Email | Dashboard |
|------|-------|-----------|
| Umar Abubakar | umarabubakarg2018@gmail.com | Super Admin |
| Munira Abubakar | muniraabubakar6@gmail.com | Product & Brand |
| Zakwan Lawali | zakawanulawali2017@gmail.com | Skill Acquisition |
| Balkisu Sani Kaura | kaurabalkisusani@gmail.com | Finance & Content |
| Hauwau Abubakar | hauwauabubakargusau2009@gmail.com | Exam Prep & Access |

### 1.3 Content Readiness
- [ ] JAMB past questions uploaded (English, Biology, Physics, Chemistry)
- [ ] WAEC past questions uploaded (core O-Level subjects)
- [ ] NECO past questions uploaded (core subjects)
- [ ] Secondary school curriculum content uploaded (SS1–SS3, JSS1–JSS3)
- [ ] At least one practice quiz live per exam type

### 1.4 Student Onboarding Setup
- [ ] Student registration flow tested end-to-end (register → email → dashboard)
- [ ] Student roles configured in Supabase: `student_jamb`, `student_waec`, `student_neco`, `student_secondary`
- [ ] Exam Prep Coordinator (Hauwau) can view and manage student list from her dashboard
- [ ] Super Admin can view all students from the User Management panel

### 1.5 Quality Checks
- [ ] All 5 team dashboards tested with real login (not dry-run)
- [ ] Student dashboard tested with a sample student account
- [ ] Mobile browser tested (at least Chrome on Android)
- [ ] Magic-link emails arrive within 60 seconds

---

## Part 2 — QUICK START

### For Team Members

**Step 1 — Receive your credentials**  
You will receive an email from `onboarding@akulearn.com` with your email and a temporary password.

**Step 2 — Log in to the dashboard**  
1. Go to [https://akulearn.vercel.app/login](https://akulearn.vercel.app/login) (replace with the live URL)  
2. Enter your team email address  
3. Click **Send Magic Link** — check your inbox  
4. Click the link in the email — you are now logged in  
5. You will be redirected to your personalised dashboard

**Step 3 — Change your password**  
Navigate to **Profile → Security** and set a strong permanent password.

**Step 4 — Explore your dashboard**  
Each team member sees only the panels relevant to their role:

| Your Role | What you see |
|-----------|-------------|
| Umar (Super Admin) | System analytics, user management, audit logs, all panels |
| Munira (Product & Brand) | Product roadmap, marketing analytics, media kit, pitch tools |
| Zakwan (Skill Acquisition) | Course management, trainee progress, certification tools |
| Balkisu (Finance & Content) | Budget management, content pipeline, financial reports |
| Hauwau (Exam Prep) | JAMB/WAEC/NECO dashboards, student onboarding panel, quiz management |

---

### For Student Onboarding (Hauwau / Umar)

**To register a new student:**

1. Log in to the dashboard with your team credentials  
2. In the **Student Onboarding** panel, fill in the student's details:
   - Full name  
   - Email address  
   - Exam type: **JAMB**, **WAEC**, **NECO**, or **Secondary School**  
   - Class level: SS1 / SS2 / SS3 / JSS1 / JSS2 / JSS3  
   - Subjects (select from the list)  
3. Click **Register Student** — the student receives a magic-link email  
4. The student clicks the link and lands on their personalised exam-prep dashboard

**What students see on their dashboard:**
- Welcome screen with their name, exam type, and class level
- Subject cards with progress bars
- Quick access to past questions (JAMB / WAEC / NECO by year)
- Practice quiz launcher
- Study schedule and upcoming milestones
- Performance analytics (scores over time)

---

### For Students (JAMB / WAEC / NECO / Secondary)

**Step 1** — Check your email for a registration link from the Akulearn team  
**Step 2** — Click the link to activate your account  
**Step 3** — You are taken directly to your exam-prep dashboard  
**Step 4** — Select a subject → start a practice quiz  
**Step 5** — Review your results and track your progress over time

---

## Part 3 — EXAM TYPES & SUBJECTS REFERENCE

### JAMB (UTME)
- Compulsory: Use of English
- Science track: Mathematics, Biology, Physics, Chemistry
- Arts track: Literature, Government, Economics, CRK/IRK
- Commercial track: Mathematics, Economics, Accounting, Commerce

### WAEC (O-Level / SSCE)
- Core: English Language, Mathematics
- Sciences: Biology, Chemistry, Physics, Agricultural Science
- Arts: Literature, History, Government, CRK/IRK, Fine Art
- Commercial: Economics, Accounts, Commerce, Business Studies
- Technical: Technical Drawing, Foods & Nutrition, Home Economics

### NECO (SSCE)
- Same subject groups as WAEC (parallel exam body)
- Additional vocational electives available

### Secondary School (Non-Exam Students)
- JS1–JS3: Core curriculum per NERDC (English, Maths, Basic Science, Social Studies, etc.)
- SS1–SS3: Pre-exam curriculum with WAEC/NECO alignment

---

## Part 4 — TEAM RESPONSIBILITIES AT LAUNCH

| Responsibility | Owner |
|----------------|-------|
| System uptime & technical issues | Umar |
| Student/parent communications & social media | Munira |
| Skill acquisition programme registration | Zakwan |
| Content quality & financial tracking | Balkisu |
| Student exam-prep onboarding & support | Hauwau |

---

## Part 5 — POST-LAUNCH (WEEK 1 TARGETS)

- [ ] 20 students registered and active on the platform
- [ ] Each student completes at least one practice quiz
- [ ] Team reviews student progress reports together
- [ ] Gather feedback from first cohort for iteration
- [ ] Identify top-3 content gaps and escalate to Balkisu

---

_Last updated: 2026-04-09 | Akulearn Core Team_
