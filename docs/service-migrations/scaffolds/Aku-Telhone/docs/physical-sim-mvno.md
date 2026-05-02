# Aku-Telhone — Physical SIM & MVNO

> Issue Telhone-branded physical SIM cards under a Nigerian MVNO (Mobile Virtual Network Operator) agreement so that every device — including 3G feature phones and budget Android handsets — can connect to the Aku network.

---

## Why Physical SIM Is Non-Negotiable

The majority of Nigerian devices in education communities are 3G/4G feature phones and entry-level Android smartphones that do not support eSIM. Physical SIM is the baseline that delivers broad reach from day one.

---

## MVNO Agreement

### Host MNO Selection

Primary candidates: **MTN Nigeria** and **Airtel Nigeria**, chosen for:
- Widest national 2G/3G/4G coverage, including Zamfara state.
- Established MVNO frameworks and wholesale interconnect programmes.
- Existing regulatory track records with NCC.

The agreement must cover:
- National 2G/3G/4G roaming and voice/data pass-through.
- SMS and voice termination for calls leaving the Aku network.
- Bundled data pricing that enables Aku to offer competitive local rates.
- Emergency services obligations (999/112 call routing).

### Preferred Network Policy

| Device location | Traffic routing | Cost to user |
|---|---|---|
| In range of Aku Edge Hub (Wi-Fi or small-cell) | Routes locally via Edge SIP proxy | Zero-rated or deeply discounted |
| Outside Aku coverage | Falls back to host MNO network | Standard MVNO bundle rates |

The SIM profile encodes `preferred_network=aku`. The device's network selection logic (or a companion app rule) enforces local breakout when Aku coverage is detected.

---

## SIM Provisioning via IG-Hub

IG-Hub acts as the Telhone SIM provisioning backend:

1. **Profile creation** — IG-Hub generates SIM profile records (ICCID, IMSI, Ki/OPc) and sends them to the SIM personalization bureau.
2. **Lifecycle tracking** — IG-Hub maintains each SIM's state: `unactivated` → `active` → `suspended` → `ported-out` / `lost-stolen`.
3. **Metadata** — each profile carries `user_role` (student / teacher / admin) and `allowed_bundles`.
4. **NIN binding** — Nigeria's mandatory NIN-based SIM registration is enforced at activation: IG-Hub calls the NIMC API to verify the subscriber's National Identification Number before moving a SIM to `active`.

---

## SIM Distribution Channels

| Channel | Target users | Notes |
|---|---|---|
| Aku Edge Hub deployment teams | Teachers and admins on school installation day | Pre-activated; highest conversion |
| Community agents (LGA level) | Students and local households | Modeled on FMCG airtime agent network |
| State Ministry of Education | Student bulk issuance for school programmes | Co-branded with state government |
| Partner retail outlets | General public / urban users | Agent commission model |

---

## Numbering Plan

- Register a dedicated Number Range (or sub-range leased from host MNO) under NCC allocation.
- Assign Telhone numbers with a recognizable prefix for brand awareness.
- Support **port-in**: users who want to bring their existing number to Telhone initiate a port via the Telhone app or USSD menu, processed through the host MNO's number portability system.

---

## SIM Personalization

Engage a certified SIM manufacturing bureau with Nigerian operations:
- **Thales** (formerly Gemalto) — preferred; has West Africa presence.
- **Giesecke+Devrient (G+D)** — alternative with GSMA-certified manufacturing.

The bureau pre-personalizes SIMs with Aku's MVNO credentials and ships boxed or bulk SIM packs to Aku's distribution centres.

---

## Billing Integration

- Each SIM's data and voice events are reported as CDRs to the Super Hub mediation collector.
- Super Hub forwards cleared CDRs to IG-Hub for bundle deduction and revenue accounting.
- Prepaid model: bundle balance is checked before each call/session; subscriber is notified at low-balance thresholds via SMS or in-app push.

---

## Security

- **SIM cloning prevention:** Ki and OPc values are generated and stored only within HSM-protected infrastructure at the personalization bureau and IG-Hub.
- **Lost/stolen SIMs:** admin can suspend a SIM immediately via IG-Hub portal or API; suspension propagates to the host MNO within minutes via HLR update.
- **NIN verification logs** are stored in encrypted form and access-controlled per NDPR requirements.

---

## Related Documents

- [eSIM Pillar](esim.md)
- [Telhone Application](telhone-app.md)
- [Nigeria Regulatory & Commercial Steps](regulatory.md)
- [MVNO/eSIM Integration Plan (Zamfara Pilot)](../../../../esim/mvno_esim_integration_plan.md)
- [VoIP & Caching Architecture](../../../../architecture/voip_caching_architecture.md)
