# Telhone Application

The Telhone App is the subscriber-facing mobile application for Aku-Telhone services. It handles SIM management, data top-ups, eSIM activation, and account control.

## Overview

| Property | Detail |
|----------|--------|
| Platform | Android (primary), iOS |
| Min Android version | 8.0 (API 26) |
| Min iOS version | 14.0 |
| Authentication | Phone number + OTP; biometric unlock |
| State management | Kotlin: ViewModel + StateFlow; Swift: Combine |

## Core Features

### 1. SIM & eSIM Management
- Activate a new physical SIM or download an eSIM profile
- View SIM status, ICCID, MSISDN
- Enable / disable eSIM profiles (dual-SIM devices)

### 2. Data & Bundle Top-Up
- Purchase data bundles (daily, weekly, monthly)
- Zero-rated Akulearn content bundles
- Payment via card, bank transfer, USSD, or Aku Coin

### 3. Account & KYC
- NIN-linked profile registration
- View usage history and invoices
- Manage beneficiaries (family top-up)

### 4. Notifications
- Low balance alerts
- Bundle expiry reminders
- Promotional offers

## App Architecture

```
Telhone App (Android / iOS)
│
├── Presentation layer  (Jetpack Compose / SwiftUI)
├── Domain layer        (Use Cases)
├── Data layer
│   ├── Remote: Telhone REST API  (JWT auth)
│   └── Local:  Room DB / Core Data (offline cache)
└── Shared KMP module   (business logic, models)
```

## API Integration

The Telhone App communicates with the Aku-Telhone backend via a versioned REST API:

- **Base URL:** `https://api.telhone.ng/v1`
- **Auth:** ****** (JWT), refreshed via `/auth/refresh`
- **Key endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sim/activate` | POST | Activate physical SIM |
| `/esim/profile` | POST | Initiate eSIM profile download |
| `/bundle/list` | GET | List available data bundles |
| `/bundle/purchase` | POST | Purchase a data bundle |
| `/account/balance` | GET | Get current balance |

## Build & Release

```bash
# Android
./gradlew :telhone-app:assembleRelease

# iOS
xcodebuild -scheme TelhoneApp -configuration Release archive
```

Releases are signed and published via the CI/CD pipeline in `.github/workflows/`.

## Related

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [eSIM](esim.md)
