# Go/No-Go Gates & Evaluation Criteria — Zamfara Pilot

This document defines decision gates for the pilot and criteria to move between phases.

Gate 0 — Procurement & Permits (Pre-deploy)
- Criteria to pass:
  - Prototype kits procured and tested (2 bench-test units)
  - Site survey schedule completed for all 10 pilot schools
  - Required permits and school permissions obtained
- Action if fail: address procurement delays, obtain missing permits, revalidate procurement choices

Gate 1 — Post-Install Validation (After each site install)
- Criteria to pass (per site):
  - Edge Hub achieves successful boot and content sync
  - Battery/solar system reports correct voltages and charging behavior
  - Wi‑Fi and local services (SIP registration) are functional
  - Local admin/training done and teacher confirms basic access
- Action if fail: repair/replace hardware, re-train teacher, re-test within 72 hours

Gate 2 — Pilot Acceptance (After 30 days of operations)
- Criteria to pass (pilot-wide):
  - Average Edge Hub uptime >= 95%
  - Teacher adoption: >= 60% active weekly users among trained teachers
  - Student reach: >= 300 unique students/week across the pilot
  - Cache hit ratio >= 60% for preloaded content
  - Intra-Aku call success >= 95% where VoIP is enabled
- Action if fail: identify systemic issues (hardware, content, training), run a 2-week remediation plan and reassess

Gate 3 — Super Hub & LGA Scale Readiness
- Criteria to pass:
  - Super Hub deployed and stable (network, power, softswitch functional)
  - Central monitoring receives telemetry from all pilot Edge Hubs reliably
  - MVNO/eSIM pilot results acceptable for provisioning flows and local calls
  - Regulatory issues resolved for scale (NCC, interconnect agreements)
- Action if fail: delay scale until Super Hub stability and regulatory issues are cleared; continue incremental LGA rollouts as permitted

Gate 4 — Statewide Expansion Approval
- Criteria to pass:
  - Clear operational SOPs and runbooks in place
  - Funding committed for scale (procurement + ops for first 12 months)
  - Local partners (resellers, maintenance teams) recruited and trained
  - Measured learning outcome improvement (baseline vs pilot) or clear case for further evaluation
- Action if fail: prepare revised scale plan focusing on weakest areas (ops, funding or outcomes)

Decision process & cadence
- Gates are reviewed by a cross-functional steering committee (Project Lead, Ministry rep, Procurement, Legal, Technical Lead) within 7 days of data submission.
- For Gate 2 and later, include external evaluation (independent school observer or NGO report) where practical.
