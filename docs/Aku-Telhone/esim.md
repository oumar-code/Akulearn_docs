# eSIM Integration

## Phase 3 Context: Borderless, Frictionless Growth

This phase follows physical SIM expansion and removes SIM manufacturing, shipping, and field-distribution constraints.
Users can activate connectivity digitally from inside the app, supporting faster regional scale.

## Pan-African Alignment

The eSIM model matches Coo-Cah Technologies Holdings' multi-country structure by enabling cross-border continuity.
A user can activate in one market and continue service across partner regions (for example Nigeria, Rwanda, and Kenya) without physical SIM swaps.

## How It Works

Aku-Telhone supports remote SIM provisioning (RSP) for eSIM-capable devices, enabling instant, over-the-air activation.

1. User opens the Telhone App and selects **Activate eSIM**
2. App generates a QR code or activation code pointing to the SM-DP+ server
3. Device LPA connects to SM-DP+ and downloads the Aku-Telhone profile
4. Profile is installed on the eUICC and activated
5. NIN verification completes KYC inline with NCC requirements

## Aku-Telhone eSIM Architecture

```
Device (eUICC)
      │  LPA (Local Profile Assistant)
      ▼
SM-DP+ (Subscription Manager – Data Preparation+)
      │  GSMA SGP.22 compliant
      ▼
Aku-Telhone BSS / SM-SR
      │
      ▼
HLR / HSS (subscriber activation)
```

### Key Components

| Component | Role |
|-----------|------|
| **eUICC** | Embedded Universal Integrated Circuit Card in the device |
| **LPA** | Local Profile Assistant — manages profile download on-device |
| **SM-DP+** | Prepares and securely delivers operator profiles |
| **SM-SR** | Manages profile lifecycle (enable, disable, delete) |

## Supported Devices

eSIM activation is supported on devices with a GSMA-certified eUICC, including:

- iPhone XS and later
- Google Pixel 3 and later
- Samsung Galaxy S20 and later
- Selected Android devices running Android 9+

## Zero-Rating for Educational Content

Once the Aku-Telhone eSIM profile is active, traffic to Akulearn platform endpoints is zero-rated — learners can access course content and the AI Tutor without consuming their data balance.

## Related

- [Telhone Application](telhone-app.md)
- [Physical SIM & MVNO](physical-sim-mvno.md)
- [MVNO/eSIM Integration Plan](../esim/mvno_esim_integration_plan.md)
