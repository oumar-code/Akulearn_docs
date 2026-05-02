# Aku-Telhone — Mobile Application

> The Telhone app gives any user access to Aku telephony — even without a physical or eSIM Telhone SIM — using VoIP over data. It is also the management surface for SIM accounts, bundles, and community calling.

---

## Why an App?

- Removes the SIM as an access prerequisite: any user with a data connection can make and receive Telhone calls.
- Provides a unified UI for eSIM activation, SIM management, bundle purchase, and usage monitoring.
- Enables community features (group calls, school directory) that are not accessible from a SIM alone.
- Serves as the primary channel for urban and tech-savvy users who prefer digital-first access.

---

## Core Features

### 1 — Soft SIM / VoIP Calling

- The app registers with the nearest Aku SIP proxy (Edge Hub SIP proxy when on Aku Wi-Fi; Super Hub softswitch over the internet) using **SIP over TLS** (port 5061).
- Each app account is assigned a Telhone number independent of any physical or eSIM.
- **Intra-Aku calls** (app-to-app, app-to-Telhone SIM): free or zero-rated.
- **Calls outside Aku network**: routed via Super Hub softswitch → host MNO PSTN gateway; charged from the user's active bundle.
- Media encryption: **SRTP** where supported.
- NAT traversal: **ICE / STUN / TURN** for calls across different networks.
- Incoming call wake-up: **Firebase Cloud Messaging (Android)** / **Apple Push Notification Service (iOS)** triggers the app when a call arrives while the app is in the background.

### 2 — eSIM Self-Service

- **QR code scanner**: user points camera at the Telhone eSIM QR code to trigger install.
- **One-tap app-assisted install**: on supported Android devices, uses `EuiccManager.downloadSubscription()`; on iOS, deep-links to Settings with a pre-filled activation URL.
- eSIM status display: active profile, network preference, bundle entitlements.
- **Physical SIM request**: for users on non-eSIM devices, the app submits a physical SIM request — delivered via agent pickup or post.

### 3 — Bundle & Account Management

- Browse and purchase prepaid data, call, and SMS bundles.
- View real-time usage: data consumed, minutes used, SMS remaining.
- Top-up via card payment, bank transfer, or airtime-to-data conversion (where available).
- Share a bundle allocation with another Telhone user (family / classroom sharing).
- **Education bundle integration**: student accounts with a validated school enrolment automatically unlock zero-rated access to Aku Learn content, regardless of remaining data balance.

### 4 — Community Features

- **Group calling**: school cohort or class group calls facilitated by the Edge Hub media relay (supports up to the Edge Hub's configured participant limit).
- **School / community directory**: searchable list of Telhone users within the same Edge Hub community; in-app tap-to-call.
- **Teacher–student messaging**: lightweight text channel for assignment reminders and announcements (stored locally at the Edge Hub; synced to Super Hub when connectivity allows).

### 5 — Connectivity Awareness

The app continuously monitors the active network and displays a connectivity tier badge:

| Badge | Meaning | Call cost |
|---|---|---|
| 🟢 Aku Wi-Fi | On Aku Edge Hub local network | Free / zero-rated |
| 🔵 Telhone Mobile | On Telhone MVNO mobile data | Bundle rate |
| 🟡 External MNO | On another operator's data | Bundle rate (may be higher) |
| 🔴 Offline | No data connection | SIM voice only |

---

## Tech Stack

### Android (primary)

| Layer | Technology |
|---|---|
| Language | Kotlin |
| UI | Jetpack Compose |
| SIP / VoIP | Linphone SDK (open-source, LGPL) |
| Networking | Retrofit + OkHttp |
| Push | Firebase Cloud Messaging (FCM) |
| eSIM | Android `EuiccManager` API (API level 28+) |

### iOS (Phase 2)

| Layer | Technology |
|---|---|
| Language | Swift |
| UI | SwiftUI |
| SIP / VoIP | Linphone SDK or PJSIP |
| Push | Apple Push Notification Service (APNs) |
| eSIM | Core Telephony / `CTCellularPlanProvisioning` |

### Backend (shared)

| Component | Technology |
|---|---|
| SIP registration & routing | Kamailio (Edge Hub) + FreeSWITCH (Super Hub softswitch) |
| Account, bundle & eSIM APIs | IG-Hub REST API (HTTPS/TLS) |
| Billing events | Super Hub CDR mediation → IG-Hub clearing |
| Media relay (fallback) | RTP relay on Edge Hub; TURN server on Super Hub |

---

## App Distribution

| Channel | Phase | Notes |
|---|---|---|
| Direct APK download (Aku portal) | Phase 0 (pilot) | For schools with restricted Play Store access |
| Google Play Store | Phase 1 (state rollout) | Primary public channel |
| Apple App Store | Phase 2 (national expansion) | After Android validation complete |

---

## Offline Behaviour

When the device has no data connection:
- VoIP calling is unavailable; the app prompts the user to use their physical SIM for voice.
- Previously cached community directory and bundle information remain viewable.
- Teacher–student messages are queued locally and sent when connectivity resumes (leveraging the Edge Hub pending events buffer).

---

## Security

- All API calls use HTTPS with certificate pinning for the IG-Hub domain.
- SIP signalling over TLS (SIPS); media encrypted with SRTP.
- App-level authentication: Aku account JWT issued by IG-Hub IdP; short-lived access tokens with silent refresh.
- Biometric / PIN lock option for devices used in shared settings (e.g. school tablet pools).

---

## Related Documents

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [eSIM Pillar](esim.md)
- [Nigeria Regulatory & Commercial Steps](regulatory.md)
- [VoIP & Caching Architecture](../../../../architecture/voip_caching_architecture.md)
- [Aku Edge Hub Service](../../../../services/aku-edgehub.md)
- [Mobile App Overview](../../../../03-mobile/index.md)
