# Physical SIM & MVNO

This document covers Aku-Telhone's physical SIM card distribution strategy and the MVNO (Mobile Virtual Network Operator) infrastructure that underpins it.

## MVNO Architecture

Aku-Telhone operates as a Full MVNO, managing its own HLR/HSS (Home Location Register / Home Subscriber Server) while leasing radio access network (RAN) capacity from a licensed Nigerian MNO partner.

```
Subscriber Device
      │
      ▼
MNO Radio Network (leased RAN)
      │
      ▼
Aku-Telhone Core Network
  ├── HLR / HSS (subscriber database)
  ├── MSC / VLR (call/SMS switching)
  ├── GGSN / PGW (data gateway)
  └── IN Platform (charging & billing)
      │
      ▼
Akulearn Content Platform (zero-rated)
```

## Physical SIM Distribution

### SIM Card Specifications

| Parameter | Value |
|-----------|-------|
| Form factor | Triple-cut (2FF / 3FF / 4FF) |
| Technology | 4G LTE with 2G/3G fallback |
| Storage | 128 KB EEPROM |
| OTA capability | Yes (remote provisioning) |

### Distribution Channels

1. **School Agent Network** — Trained school administrators and teachers act as SIM registration agents
2. **Community Kiosks** — Fixed-point activation kiosks co-located with Aku Edge Hubs
3. **Retail Partners** — Selected mobile phone retailers in pilot LGAs
4. **Online Activation** — Self-service registration via the Telhone App with NIN verification

### KYC & Registration

All SIM activations comply with NCC regulations:

- National Identity Number (NIN) linkage mandatory
- Biometric capture (fingerprint) at agent points
- BVN linkage optional (for financial services integration)
- Maximum of 3 SIMs per NIN

## MVNO Partner Agreements

Aku-Telhone maintains interconnect and roaming agreements with major Nigerian MNOs to ensure nationwide coverage. Specific partner details are confidential and documented in the internal legal repository.

## Billing & Charging

- Prepaid-first model with optional post-paid for institutional subscribers (schools, NGOs)
- Real-time charging via DIAMETER Gy interface
- Educational content zero-rating enforced at PGW level via traffic classification

## Related

- [eSIM](esim.md)
- [Nigeria Regulatory Steps](regulatory.md)
