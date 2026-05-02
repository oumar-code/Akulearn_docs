# Aku-Telhone — Nigeria Regulatory & Commercial Steps

> This document lists every regulatory filing, license, and commercial agreement required to operate Aku-Telhone legally in Nigeria across all three pillars (physical SIM, eSIM, and app-based VoIP).

---

## 1 — NCC MVNO / VNO License

**Why:** Nigerian Communications Commission (NCC) requires operators that issue SIM cards and subscriber numbers to hold an appropriate license.

**Steps:**
- File for a **Mobile Virtual Network Operator (MVNO)** license or, if a full MVNO is not feasible for the pilot, a **Virtual Network Operator (VNO)** notification.
- Submit the application to NCC's licensing unit with:
  - Corporate registration documents (CAC certificate)
  - Technical proposal describing Aku's MVNO architecture and host MNO arrangement
  - Evidence of host MNO letter of intent or signed wholesale agreement
- Estimated NCC processing time: 60–90 days; begin the application at least 3 months before planned commercial launch.

**Pilot shortcut:** NCC has approved limited-scope MVNO trials under a test-and-trial licence framework. Aku should apply for a trial authorisation covering the Zamfara pilot cohort while the full MVNO application is in process.

---

## 2 — NCC VoIP Notification

**Why:** NCC's *Voice over Internet Protocol Regulations, 2012* requires any entity providing VoIP services commercially (including the Telhone app) to submit a mandatory notification to NCC.

**Steps:**
- Prepare and submit the VoIP service notification form to NCC, including:
  - Description of the VoIP service (intra-Aku SIP calling and app-to-PSTN via Super Hub)
  - Technical architecture summary (reference the VoIP & Caching Architecture document)
  - Interconnect arrangements for calls leaving Aku network
- NCC may issue conditions relating to lawful intercept readiness and emergency call routing.

---

## 3 — NCC Type Approval

**Why:** All radio and telecommunications equipment sold or operated in Nigeria requires NCC type approval.

**Applies to:**
- Aku Edge Hub (radio module — Wi-Fi, LoRa, small-cell)
- Any SIM card reader or provisioning device used for distribution
- Telhone-branded devices (if Aku procures or distributes handsets)

**Steps:**
- Submit each device model for NCC type approval testing through an accredited test lab.
- Display the NCC approval mark (NAPP) on equipment packaging and documentation.
- Allow 6–12 weeks per device model for NCC testing and approval.

---

## 4 — Host MNO Wholesale Agreement

**Why:** Telhone physical SIMs and eSIM profiles require a host MNO to provide national coverage, interconnect, and SMS/voice termination outside the Aku network.

**Key commercial terms to negotiate:**

| Term | Notes |
|---|---|
| MVNO wholesale data rate | Target: competitive rate to allow Telhone pricing below standard MNO retail |
| Voice termination (per minute) | Interconnect rate for calls to and from other Nigerian networks |
| SMS termination | Per-message rate for A2P and P2P SMS |
| Emergency services | Mandatory 999/112 routing obligation; agree liability allocation |
| Number Range sub-lease | If Aku does not yet hold its own NCC number range, lease a sub-range from the MNO |
| SIM card format | Confirm MNO support for MVNO SIMs and eSIM MVNO profile hosting |
| SLA for HLR updates | Agreed response time for SIM suspension / restore requests |

**Candidates:** MTN Nigeria and Airtel Nigeria (see [Physical SIM & MVNO](physical-sim-mvno.md)).

---

## 5 — SIM Personalization Agreement

**Why:** Physical SIM cards must be manufactured and personalized (ICCID/IMSI/Ki/OPc loaded) by a certified SIM bureau before distribution.

**Steps:**
- Sign a SIM manufacturing and personalization agreement with a GSMA-certified bureau (Thales or G+D preferred for Nigerian operations).
- Provide MVNO credentials (MCC/MNC, IMSI range, authentication algorithms) once NCC MVNO license is issued.
- Agree on minimum order quantities and lead times for the pilot (recommend ordering 200 SIMs for the Phase 0 pilot to cover attrition and spares).
- Ensure the bureau's HSM-protected facilities comply with GSMA SAS-UP (SIM vendor) accreditation.

---

## 6 — NIN-Based SIM Registration (NIMC API)

**Why:** Nigerian law (SIM Card Registration Regulations, 2011 and subsequent NCC directives) mandates that every SIM be registered against the subscriber's National Identification Number (NIN) before activation.

**Steps:**
- Register Aku as an approved SIM registration agency with NCC and NIMC (National Identity Management Commission).
- Integrate the **NIMC NIN Verification API** into the Telhone onboarding flow (IG-Hub provisioning service):
  - On SIM activation request, the subscriber provides their NIN and date of birth.
  - IG-Hub calls the NIMC API to verify the NIN and retrieve the subscriber's legal name.
  - If verification passes, IG-Hub moves the SIM to `active` state and logs the NIN binding.
  - If verification fails, SIM remains `unactivated` and the user is guided to update their NIMC record.
- NIN verification responses and binding records must be stored in IG-Hub in encrypted form; access restricted to compliance officers per NDPR.

**Target:** ≥ 95% NIN verification success rate (operational KPI per the Telhone strategy).

---

## 7 — NDPR / NDPA Compliance (Data Privacy)

**Why:** The Nigerian Data Protection Regulation (NDPR) 2019, now enforced by the Nigeria Data Protection Commission (NDPC) under the Nigeria Data Protection Act (NDPA) 2023, applies to all personal data of Nigerian subscribers, including NIN bindings, call records, and location data.

**Requirements:**

- **Privacy Notice:** publish a clear, plain-language privacy notice covering what data Telhone collects, how it is used, and subscriber rights.
- **Data Processing Agreements:** sign DPAs with all sub-processors (host MNO, SIM bureau, SM-DP+ partner, cloud providers).
- **Data Minimization:** collect only the minimum subscriber data needed for SIM registration, billing, and service provision.
- **Retention & Deletion:** define retention periods for CDRs, NIN bindings, and app logs; implement automated deletion schedules.
- **Annual Audit:** NDPA requires data controllers processing sensitive data to conduct and submit an annual Data Protection Audit report to NDPC.
- **DPIA:** complete a Data Protection Impact Assessment before launching SIM registration and NIN collection at scale.

---

## 8 — Emergency Services (999 / 112)

**Why:** Nigerian telecoms operators are required to route emergency calls (999, 112) without charge, regardless of the subscriber's bundle status.

**Implementation:**
- Telhone app: emergency numbers (999, 112) bypass bundle balance checks and route directly to the Super Hub PSTN gateway → host MNO emergency routing.
- Physical SIM / eSIM: emergency call routing is handled by the host MNO under the MVNO agreement.
- Confirm with the host MNO that their agreement explicitly covers emergency call obligations for MVNO subscribers.

---

## Regulatory Contacts & Owners

| Body / Activity | Internal Owner | External Contact |
|---|---|---|
| NCC MVNO/VNO License | Legal/Compliance Lead | NCC Licensing Department |
| NCC VoIP Notification | Legal/Compliance Lead | NCC Consumer Affairs Bureau |
| NCC Type Approval | Hardware / Procurement Lead | NCC Technical Standards Department |
| Host MNO Agreement | Commercial Lead | MTN / Airtel wholesale team |
| NIMC NIN Integration | Platform Engineering | NIMC API team |
| NDPR / NDPA Compliance | Data Protection Officer | Nigeria Data Protection Commission |

---

## Related Documents

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [eSIM Pillar](esim.md)
- [Telhone Application](telhone-app.md)
- [Regulatory Compliance Checklist (Zamfara Pilot)](../../../../regulatory/regulatory_compliance_checklist.md)
- [MVNO/eSIM Integration Plan](../../../../esim/mvno_esim_integration_plan.md)
