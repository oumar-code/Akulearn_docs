# eSIM Integration

Aku-Telhone supports remote SIM provisioning (RSP) for eSIM-capable devices, enabling instant, over-the-air activation without a physical SIM card.

## What is eSIM?

An eSIM (embedded SIM) is a programmable SIM soldered directly into a device. Instead of swapping physical cards, profiles are downloaded over the air via the GSMA SGP.22 (Consumer eSIM) or SGP.02 (M2M) specification.

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

## Activation Flow

1. User opens the Telhone App and selects **Activate eSIM**
2. App generates a QR code or activation code pointing to the SM-DP+ server
3. Device LPA connects to SM-DP+ and downloads the Aku-Telhone profile
4. Profile is installed on the eUICC and activated
5. NIN verification completes KYC inline with NCC requirements

## Supported Devices

eSIM activation is supported on devices with a GSMA-certified eUICC, including:

- iPhone XS and later
- Google Pixel 3 and later
- Samsung Galaxy S20 and later
- Selected Android devices running Android 9+

## Zero-Rating for Educational Content

Once the Aku-Telhone eSIM profile is active, traffic to Akulearn platform endpoints is zero-rated — learners can access course content and the AI Tutor without consuming their data balance.

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| QR code scan fails | Ensure device supports eSIM; check that mobile data or Wi-Fi is active |
| Profile download timeout | Retry; contact support if it persists beyond 3 attempts |
| NIN verification rejected | Verify NIN at NIMC portal before re-attempting |

## Related

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [MVNO/eSIM Integration Plan](../esim/mvno_esim_integration_plan.md)
