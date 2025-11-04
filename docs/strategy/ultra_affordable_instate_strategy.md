# Ultra-Affordable In-State Connectivity — Implementation Plan

This document translates the high-level strategy into concrete implementation steps for Aku's ultra-affordable in-state network model (Zamfara pilot → scale). It focuses on maximizing local offload (voice & data), predictive caching, eSIM enablement, and pricing that leverages Aku's tiered architecture.

1. Quick summary
- Objective: Keep in-state voice & data traffic on Aku-controlled infrastructure (Edge Hubs + Super Hubs) to minimize MNO interconnect/backhaul costs and offer dramatically lower prices.
- Approach: Deploy local SIP/VoIP at Edge, aggregate routing at Super Hubs, apply multi-tier caching and AI-driven prefetching, and provision users with Aku eSIM profiles for smart routing and billing.

2. High-level milestones
- M1: VoIP & Local Routing prototype (Edge SIP proxy + Super Hub softswitch)
- M2: Edge caching + predictive prefetch (Aku Learn + top web content)
- M3: eSIM provisioning & onboarding flow (pilot 50 devices)
- M4: Pricing model & billing integration with IG-Hub
- M5: Pilot MVNO/eSIM trial and measurement
- M6: Scale automation and operational playbook

3. Milestone Tasks (concrete)
- M1 tasks:
  - Select SIP stack (Asterisk or Kamailio + FreeSWITCH) for Edge and Super Hub roles
  - Build minimal Docker Compose prototype for Edge SIP proxy and softphone client
  - Implement local call routing rules (same-edge direct, edge-to-edge via Super Hub)
  - Test intra-edge call quality and call setup success in lab

- M2 tasks:
  - Define cache hierarchy: Edge (per-hub), Super Hub (state), IG-Hub (global)
  - Implement Aku Learn caching footprint and content invalidation policy
  - Build predictive prefetch service (batch job on Super Hub using transformer analytics)
  - Measure cache hit rate and backhaul reductions

- M3 tasks:
  - Integrate eSIM provisioning APIs with IG-Hub (profile create, activate, revoke)
  - Create onboarding UX (QR code / activation code) for supported devices
  - Enforce network policy on device profile (prefer Aku network, local bundles)

- M4 tasks:
  - Design pricing tiers (free education, in-state bundles, national bundles)
  - Implement billing events (call start/stop, data session usage, local zero-rating rules)
  - Integrate billing records with IG-Hub clearing service for revenue accounting

- M5 tasks:
  - Run a controlled MVNO pilot with partner MNO for non-Aku interconnect
  - Monitor call routing % kept on Aku vs handed to MNO, user satisfaction
  - Iterate pricing and policies

4. Success metrics
- Cache hit ratio >= 60% within 30 days for preloaded Aku Learn content
- In-state call routing >= 80% of calls remain on Aku network (pilot target)
- Cost per in-state minute < 10% of typical MNO local call cost (target)

5. Risks & mitigations
- Regulatory pushback: early NCC engagement and clear pilot scope
- Voice quality issues: start with local short tests and increase call quality monitoring
- Device diversity: restrict initial eSIM pilot to known compatible devices

6. Short-term deliverables (30 days)
- Working Docker Compose prototype for Edge SIP proxy + SIP client
- Edge caching prototype and a small predictive prefetch job (PoC)
- eSIM onboarding flow documented and tested with 10 devices
- Pricing model draft and CSV template for procurement and billing

7. Who does what
- Network Engineering: VoIP stack, routing rules, SIP handling
- Platform/ML: caching, predictive prefetch models, analytics
- Product/Commercial: pricing tiers, MVNO negotiations, billing rules
- Compliance: regulatory engagement and approvals

8. Next steps
1. Approve M1 resources (compute, test devices, engineer time)
2. Kick off VoIP prototype and Edge caching PoC in lab
3. Schedule regulatory briefing with NCC and state stakeholders
