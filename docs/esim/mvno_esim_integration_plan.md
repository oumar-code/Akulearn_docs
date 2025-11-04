# eSIM & MVNO Integration Plan — Zamfara Pilot

## Objective
Define a pragmatic path to enable Aku eSIM provisioning and MVNO-style services that prioritize in-state local offload (calls/data) through Aku Edge and Super Hubs while using partner MNOs for external interconnect.

## Scope for Pilot
- eSIM provisioning for teacher/admin devices (pilot cohort of ~50 devices)
- SIP registration and intra-Aku calling for eSIM-enabled devices
- Billing integration via IG-Hub for trial prepaid bundles

## Technical components
- eSIM management: IG-Hub API for profile creation, activation, and lifecycle
- Device onboarding: secure QR code or OTA profile push for supported devices
- Local breakout: Edge Hub SIP proxy for local calls; Super Hub softswitch for state routing
- Network switching policy: prefer Aku network when in coverage, fallback to MNO when required

## Commercial & Regulatory
- MVNO agreement: identify MNO partner for interconnect and MMS/SMS termination
- Interconnect pricing negotiation to reduce in-state costs
- Regulatory: coordinate NCC notifications and any license needs for local VoIP services

## Pilot flows
1. Admin requests eSIM profile via IG-Hub portal
2. IG-Hub issues activation code / QR
3. Device installs profile and registers with Aku network
4. Device receives local policy: preferential local rates and Aku-only bundles

## KPIs for eSIM pilot
- Successful provisioning %
- % of calls routed locally vs via MNO
- User satisfaction (survey)

## Risks & mitigations
- Device compatibility: limit to known supported devices for pilot; increase device types after validation
- Regulatory: early engagement with NCC and MNOs
