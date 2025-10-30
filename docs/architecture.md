# Akulearn Aku Edge Hub: Local Learning Server & Edge Compute

## System Components

### Aku Edge Hub as Local Learning Server

The Akulearn Aku Edge Hub is designed to be much more than a simple projection device. It acts as a self-contained local learning server and edge compute node, enabling robust, scalable, and reliable educational experiences in environments with unreliable or no internet connectivity.

#### Key Technical Components & Functions

- **Integrated Wi-Fi Hotspot:**
  - Creates a local, isolated network for connected devices (laptops, tablets, smartphones).
  - Broadcasts a secure Wi-Fi signal (e.g., "Akulearn_SchoolName") for device access.

- **Local Web Server (Nginx/Apache/Lightweight Python server):**
  - Serves a browser-based version of the Akulearn learning portal (PWA) to all connected devices.
  - No app installation required; access via local IP address (e.g., 192.168.1.1).

- **Local Content Cache:**
  - Stores all learning modules, videos, quizzes, and associated media directly on the Hub.
  - Ensures full offline access to Akulearn content.

- **Local AI Inference Engine:**
  - Runs the Gemma AI model locally, processing AI Tutor chat requests from connected devices without internet.
  - Provides instant, personalized tutoring and curriculum generation offline.

- **Local Data Store (SQLite/Embedded DB):**
  - Temporarily stores student progress, quiz results, and AI chat histories from locally connected devices.
  - Ensures individual progress tracking even on shared devices.

- **Cloud Sync Module:**
  - Manages scheduled/opportunistic synchronization with the central Akulearn cloud backend.
  - Uploads local data, downloads new content/AI model updates.
  - Uses smart bandwidth management and data compression for efficient sync.

#### Interaction Flow

1. Devices connect to Hub's Wi-Fi.
2. Devices access local Akulearn portal via browser.
3. Learning content/AI requests are served locally by the Hub.
4. Local data is stored on Hub.
5. Hub periodically syncs with cloud backend when internet is available.

#### Architectural Benefits

- **Robustness:** Operates independently of internet reliability.
- **Scalability:** Multiple Hubs can serve large student populations and distributed classrooms.
- **Network Challenge Solution:** Decouples learning from persistent connectivity and device scarcity.

---

This architecture enables Akulearn to deliver high-quality, personalized, and scalable learning experiences in resource-constrained environments, maximizing the impact of existing school infrastructure.

