# Functional Specification

## User Journeys

This section details the core user flows for Akulearn, including onboarding, learning sessions, assessment, credentialing, and facilitator workflows.

- **Student Onboarding**
- **Facilitator Session Workflow**
- **Exam Preparation & Practice**
- **Credential Verification**


---

## Offline & Local Learning Experience via Projector Hub

### Student Experience (Device Sharing)

- Students connect their personal devices (laptops, tablets, phones) or school-provided computers/tablets to the Projector Hub's local Wi-Fi network.
- Access the Akulearn learning portal through a web browser (local IP address, e.g., 192.168.1.1).
- Multiple students can share devices: each logs into their own Akulearn account, ensuring individual progress tracking even on shared devices.
- All learning modules, videos, quizzes, and the AI Tutor are available without any internet connection.
- Individual student progress is saved locally on the Hub.

### Teacher Experience

- Teachers leverage the Hub's local network for classroom activities, assigning lessons, and monitoring in-class progress via their own connected devices.
- The Hub facilitates group learning using the projector, combined with individual device-based learning.

### School Admin Experience

- School Admins manage Hub content updates and monitor sync status via their dashboard (connected to the Hub's local Wi-Fi or when the Hub syncs).

### Offline Data Flow

- Student data is collected locally on the Hub and then synced to the cloud when an internet connection becomes available.

---
