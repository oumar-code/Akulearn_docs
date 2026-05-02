# Aku-Telhone — Nigeria Strategy Overview

> **Aku-Telhone** is the telephony and connectivity brand of the Aku platform. In Nigeria it is delivered through three complementary pillars: a **physical SIM (MVNO)**, an **eSIM**, and a **Telhone mobile application**. All three connect into the same Aku Hub infrastructure (Edge Hub → Super Hub → IG-Hub) and share a unified Telhone identity and number.

---

## Why Three Pillars?

| User segment | Primary channel | Secondary channel |
|---|---|---|
| Teacher / Admin | Physical SIM | Always install app |
| Student (smartphone) | Physical SIM | eSIM where supported + app |
| Student (feature phone) | Physical SIM only | — |
| Urban / external user | eSIM (preferred) | App standalone |

Nigeria's device landscape spans flagship eSIM-capable smartphones down to basic 3G feature phones. A single-channel approach leaves large groups unserved. The three-pillar model ensures every user can connect on the channel their device supports while the app acts as a universal management and calling surface for all.

---

## Three-Pillar Summary

### Pillar 1 — Physical SIM (MVNO)
Issue Telhone-branded physical SIM cards under a Nigerian MVNO agreement. Covers the widest device base. When a device is in range of an Aku Edge Hub, traffic offloads locally (zero-rated or discounted); otherwise it falls back to the host MNO network.

See → [Physical SIM & MVNO](physical-sim-mvno.md)

### Pillar 2 — eSIM
Offer GSMA SGP.22-compliant Remote SIM Provisioning for eSIM-capable devices. No physical distribution cost; supports dual-SIM scenarios and over-the-air policy updates. Activated via QR code, push OTA, or one-tap in the Telhone app.

See → [eSIM](esim.md)

### Pillar 3 — Telhone Application
A mobile app (Android-first) that gives any user access to Telhone VoIP calling, eSIM self-service, bundle management, and community features — without needing a Telhone SIM as a prerequisite.

See → [Telhone Application](telhone-app.md)

---

## Unified Identity

- One Aku account → one Telhone number, portable across physical SIM, eSIM, and app.
- IG-Hub IdP manages identity, device binding, and active profile.
- Find-me / follow-me: a call to a Telhone number rings all active devices simultaneously (SIM + app).

---

## Phased Rollout

### Phase 0 — Zamfara Pilot (months 1–6)
- ~50 physical SIMs issued to teachers and admins under a test MVNO arrangement.
- Telhone App available as internal Android APK beta.
- eSIM for the pilot cohort of eSIM-capable devices only.
- Validate SIP call quality, local offload percentage, and NIN registration integration.

### Phase 1 — State Rollout (months 6–18)
- Full MVNO commercial launch in Zamfara state.
- Telhone App published on Google Play Store.
- Physical SIM distribution via LGA agent network.
- eSIM expanded to all compatible devices in the network.

### Phase 2 — National Expansion (months 18–36)
- Roll out to additional states using the Super Hub per-state model.
- Negotiate national MVNO coverage (multiple MNO partners for redundancy).
- iOS app launch.
- eSIM-only "digital-first" Telhone plans for urban professionals.

---

## Key Success Metrics

| Metric | Target |
|---|---|
| SIM activation rate per cohort | > 80% within 30 days of distribution |
| % of calls routed locally via Aku | > 60% in Edge Hub coverage zones |
| App Monthly Active Users vs SIM users ratio | Tracked per cohort; target 1:1 by Phase 1 |
| NIN verification success rate | ≥ 95% (regulatory requirement) |
| Intra-Aku call success rate | ≥ 95% |
| Bundle renewal rate | Tracked as retention proxy |

---

## Related Documents

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [eSIM](esim.md)
- [Telhone Application](telhone-app.md)
- [Nigeria Regulatory & Commercial Steps](regulatory.md)
- [VoIP & Caching Architecture](../../../../architecture/voip_caching_architecture.md)
- [MVNO/eSIM Integration Plan (Zamfara Pilot)](../../../../esim/mvno_esim_integration_plan.md)
- [Zamfara Pilot Plan](../../../../rollout/zamfara_pilot_plan.md)
- [Ultra-Affordable In-State Connectivity Strategy](../../../../strategy/ultra_affordable_instate_strategy.md)
