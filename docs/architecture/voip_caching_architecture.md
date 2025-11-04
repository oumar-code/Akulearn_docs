# VoIP & Caching Architecture — Technical Overview

This document describes the recommended technical architecture to implement local call offload and multi-tier caching for Aku's Edge Hubs and Super Hubs.

1. Logical components
- Edge Hub (Tier 1)
  - SIP proxy (lightweight) — handles device SIP registration and local call routing
  - RTP relay / media path — optimized for local low-latency audio
  - Content cache (HTTP/HTTPS cache + static assets for Aku Learn)
  - Local policy engine (decides when to allow local vs Super Hub routing)

- Super Hub (Tier 2)
  - Softswitch / Core SIP (call control, numbering, federation)
  - Aggregated cache (regional cache layer + prefetch orchestration)
  - Billing & mediation collector (CDR generation, event publishing to IG-Hub)
  - Model inference for predictive caching and routing optimization

- IG-Hub (Tier 3)
  - Global policy, eSIM provisioning API, cross-state routing, and interconnect clearing

2. Call routing rules (example)
- Device A and Device B in same Edge: route via Edge SIP proxy, media path peer-to-peer or relayed by Edge
- Device in Edge X calling device in Edge Y (same Super Hub domain): signaling via Super Hub; media path via best-effort relay (prefer local relaying)
- Calls outside Aku network: Super Hub softswitch routes to MNO gateway/partner (apply interconnect and charge rules)

3. Caching architecture
- Edge Cache: stores Aku Learn content, thumbnails, small video segments, and top-n predicted assets for the local community
- Super Hub Cache: larger store of popular content for the state/region; coordinates prefetch schedules
- Cache invalidation: use content versioning, TTL, and push-based invalidation for edu content updates

4. Predictive prefetch (workflow)
- Collect time-series content access logs centrally
- Train a light transformer / sequence model on Super Hub to predict top-k content per Edge Hub per day
- During off-peak hours, Super Hub pushes top-k content to each Edge Hub over scheduled sync

5. eSIM provisioning & policy enforcement
- IG-Hub issues eSIM profiles with metadata: preferred_network=aku, allowed_bundles, user_role (student/teacher)
- Edge Hub enforces local QoS prioritization (education traffic first)

6. Security considerations
- Mutual TLS for control and telemetry between Edge and Super Hub
- SRTP for media where supported; otherwise secure RTP relays and network isolation
- Local admin accounts should use short-lived tokens and two-person provisioning for recovery

7. Observability
- Expose /metrics endpoints for Prometheus on Edge services (SIP success, RTP packet loss, cache hit rate)
- Central alerting for low cache-hit, high packet loss, or sustained media jitter

8. Implementation notes & choices
- SIP stack: Kamailio for registration/proxy + FreeSWITCH/Asterisk for media (Edge needs lightweight footprint)
- Cache: nginx or Varnish for HTTP; local file store for larger video segments; rsync/HTTP+TLS for synchronization
- Containerization: Docker Compose for prototypes; Helm charts for production Kubernetes (on Super Hub)
