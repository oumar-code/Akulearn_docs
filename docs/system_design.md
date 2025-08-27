# System Design

This document will provide high-level and low-level system design details, including diagrams and technical specifications.


## Akulearn Hybrid Localized Content Delivery Model

### Strategy for Schools with Devices & Network Interruption

Akulearn's best strategy for serving schools or communities with computers/tablets but unreliable internet is a hybrid, localized content delivery model that leverages the strengths of both Projector Hubs and existing devices.

#### 1. Projector Hub as a Local Server (The "Brain")
* **Integrated Wi-Fi Hotspot:** Every Akulearn Projector Hub has a built-in, local Wi-Fi hotspot (e.g., "Akulearn_SchoolName").
* **Local Content Delivery:** The Hub is pre-loaded with Akulearn learning modules, videos, past questions, and the Gemma AI model. Students connect via browser to a local IP (e.g., 192.168.1.1) and access a browser-friendly Akulearn portal (PWA) for lessons, practice, and AI tutoring—all offline.
* **AI Tutor on the Hub:** The Gemma AI model runs directly on the Hub, processing student requests locally for instant, offline AI tutoring.

#### 2. Scheduled & Opportunistic Syncing (The "Update Mechanism")
* **Scheduled Sync Windows:** The Hub syncs with the cloud backend during off-peak hours or when stable internet is detected, updating content, AI models, and student progress data.
* **Smart Bandwidth Usage:** Sync prioritizes essential updates and uses data compression to minimize bandwidth.
* **User Notification:** School Admin dashboard shows last sync status and new content availability.

#### 3. Teacher-Led Content Distribution & Collection
* **Offline Assignment & Collection:** Teachers assign lessons/quizzes from the local portal; student progress is stored locally on the Hub.
* **Batch Upload/Download:** Teachers can transfer data via USB or authenticated cloud sync when in a connected environment.

#### 4. Simplified Device Integration
* **No App Installation Needed:** Browser-based portal means students don't need to install an app.
* **Device-Agnostic Access:** Works on any device with a modern browser.
* **Focus on Security:** Local Wi-Fi is secure (WPA2/3) and isolated from external internet.

---

### Prototype vs. Final Product Comparison Table

| Feature                | Prototype (Raspberry Pi Hub)      | Final Product (Custom Akulearn Hub) |
|------------------------|-----------------------------------|-------------------------------------|
| Hardware               | Raspberry Pi 4 Model B            | Custom board w/ high-performance SoC & NPU |
| AI Copilot Model       | Compact, quantized LLM            | Advanced, high-parameter model      |
| Connectivity           | Local Wi-Fi only                  | Local network + cloud sync          |
| Power Management       | Basic                             | Robust, optimized                   |
| Scalability            | Small classroom/school            | Entire school/community             |
| Offline Functionality  | Full                              | Full                               |
| Online Sync            | None                              | Seamless cloud synchronization      |

---

### Architecture Diagrams

#### 1. Prototype Architecture (Offline Only)

```
 +--------------------------+
 | Raspberry Pi Hub         |
 |--------------------------|
 | - Local Wi-Fi Network    |
 | - Lightweight Linux OS   |
 | - Offline AI Copilot     |
 | - Local Web App (PWA)    |
 +--------------------------+
			|
			v
 +--------------------------+
 | Connected Devices        |
 | (PCs, Tablets, Phones)   |
 +--------------------------+
			|
			v
 +--------------------------+
 | Akulearn PWA (Offline)   |
 +--------------------------+
```

#### 2. Final Product Architecture (Hybrid Model)

```
 +-------------------------------+
 | Akulearn Hub (Custom SoC/NPU) |
 |-------------------------------|
 | - Local Network               |
 | - Advanced AI Copilot         |
 | - Robust Power Management     |
 | - Offline & Online Modes      |
 +-------------------------------+
			|
			v
 +-------------------------------+
 | Connected Devices             |
 | (PCs, Tablets, Phones)        |
 +-------------------------------+
			|
			v
 +-------------------------------+
 | Akulearn PWA                  |
 | (Offline/Online Experience)   |
 +-------------------------------+
			|
			v
 +-------------------------------+
 | Cloud Server (when online)    |
 | - Data Sync                   |
 | - Content Updates             |
 | - Analytics                   |
 +-------------------------------+
```

---

### Why This Strategy Wins for Akulearn

* **Maximizes Existing Assets:** Leverages schools' existing computers/tablets, reducing new hardware costs.
* **True Offline Capability:** Entire learning experience, including AI tutoring, is genuinely offline within the school.
* **Addresses Connectivity:** Works around unreliable internet, using it only for necessary updates.
* **Scalability:** Each Projector Hub is an independent, self-contained learning unit; expansion means deploying more Hubs.
* **Data Collection:** Student progress is tracked offline and synced when possible, supporting teachers, admins, and KPIs.
* **Simplicity for Users:** "Connect to Akulearn Wi-Fi, open browser, learn." Minimal technical hurdles.

This refined strategy positions Akulearn as an adaptable solution for diverse connectivity and infrastructure realities across Nigeria, Africa, and beyond. The Projector Hub is not just a projection device, but the intelligent, localized learning server at the heart of the school.
