# Nigeria Regulatory Steps

This document outlines the regulatory requirements and compliance roadmap for operating Aku-Telhone as a licensed MVNO and eSIM provider in Nigeria.

## Regulatory Bodies

| Body | Role |
|------|------|
| **NCC** (Nigerian Communications Commission) | Primary telecoms regulator; issues MVNO licences |
| **CBN** (Central Bank of Nigeria) | Governs mobile money and payment services |
| **NIMC** (National Identity Management Commission) | Manages NIN linkage and biometric KYC |
| **CAC** (Corporate Affairs Commission) | Company registration and incorporation |

## MVNO Licensing

### Licence Types

Aku-Telhone targets a **Full MVNO** licence, which grants control over core network elements (HLR/HSS, billing, charging).

| Licence Type | RAN | Core Network | SIM Issuance |
|--------------|-----|-------------|--------------|
| MVNO Reseller | Leased | Host MNO | Host MNO |
| Light MVNO | Leased | Partial | Own |
| **Full MVNO** | Leased | **Own** | **Own** |

### Application Process

1. **Incorporate** Aku-Telhone as a separate legal entity with CAC
2. **Apply** to NCC for an Individual Licence (Unified Access Service Licence or MVNO-specific)
3. **Submit** technical and financial capability documentation
4. **Negotiate** RAN sharing agreement with a licensed MNO
5. **Complete** network readiness audit by NCC-approved inspector
6. **Receive** licence and commence operations

### Key NCC Requirements

- Minimum paid-up capital: ₦500 million (subject to NCC update)
- Rollout obligations: Coverage targets within defined timeframes
- Quality of Service (QoS) reporting: Monthly KPI reports to NCC
- Consumer protection compliance: NCC Consumer Code of Practice

## SIM Registration & KYC Compliance

Per NCC Directive and NIMC Act:

- All subscribers must link SIM to a valid NIN before activation
- Biometric capture required at point of sale or via NIN-verified agent
- Maximum of 3 active SIMs per NIN across all networks
- Non-compliant SIMs are subject to deactivation

## eSIM Regulatory Position

The NCC issued a framework for eSIM deployment in Nigeria. Key requirements:

- SM-DP+ servers must be registered with NCC
- Profile downloads must comply with GSMA SGP.22 security requirements
- KYC obligations identical to physical SIM registration

## Data Protection

Aku-Telhone complies with the **Nigeria Data Protection Act 2023 (NDPA)**:

- Subscriber data processed only for stated purposes
- Data retention policies aligned with NCC and NDPA requirements
- Data Protection Officer (DPO) appointed and registered with NDPC

## Compliance Roadmap

| Milestone | Target Quarter |
|-----------|---------------|
| CAC incorporation | Q1 2025 |
| NCC licence application submitted | Q2 2025 |
| MNO RAN agreement signed | Q3 2025 |
| NCC licence granted | Q4 2025 |
| Commercial launch (pilot LGAs) | Q1 2026 |
| National rollout | Q3 2026 |

## Related

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [eSIM](esim.md)
