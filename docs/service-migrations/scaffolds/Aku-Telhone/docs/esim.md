# Aku-Telhone — eSIM

> Offer GSMA SGP.22-compliant Remote SIM Provisioning (RSP) for eSIM-capable devices, enabling over-the-air profile delivery, dual-SIM coexistence, and seamless Aku network policy enforcement.

---

## Target Devices

eSIM support is available on:
- **iPhone XR and later** (iOS 12.1+)
- **Samsung Galaxy S20 series and later**
- **Google Pixel 3a and later**
- Mid-range Android devices with embedded eSIM chips (device compatibility list maintained in IG-Hub)

For all other devices, Telhone issues a [physical SIM](physical-sim-mvno.md) instead.

---

## Technical Foundation — GSMA SGP.22

Aku-Telhone implements the **GSMA SGP.22 Consumer eSIM RSP** standard:

| Component | Role |
|---|---|
| **SM-DP+** (Subscription Manager Data Preparation+) | Prepares and delivers eSIM profiles to devices |
| **SM-DS** (Subscription Manager Discovery Server) | Notifies devices that a new profile is ready (push-based) |
| **LPA** (Local Profile Assistant) | Device-side component that communicates with SM-DP+ to download and install the profile |

### SM-DP+ Deployment Options

1. **Managed eSIM platform partner** (recommended for pilot and Phase 1): partner with a GSMA-certified SM-DP+ provider such as Giesecke+Devrient (G+D) or Thales to reduce time-to-market and compliance burden.
2. **Own SM-DP+ server** (target for Phase 2 national scale): deploy IG-Hub's own SGP.22-compliant SM-DP+ for full control over profile lifecycle and reduced per-profile fees.

---

## eSIM Profile Contents

Each Telhone eSIM profile carries:

| Field | Values / Notes |
|---|---|
| `preferred_network` | `aku` — device prefers Aku network when in coverage |
| `user_role` | `student` / `teacher` / `admin` |
| `allowed_bundles` | List of bundle IDs the user is entitled to |
| `local_breakout_policy` | When Aku SSID or small-cell detected → route via Edge SIP proxy |
| `mno_fallback` | Host MNO credentials for coverage outside Aku network |

---

## Activation Flows

### 1 — QR Code (manual)
1. Admin requests an eSIM profile via the IG-Hub portal.
2. IG-Hub calls SM-DP+ to create a profile and generate an LPA activation QR code.
3. QR code is displayed in the portal or sent to the user by SMS/email.
4. User scans the QR code in device Settings → Mobile/Cellular → Add eSIM.
5. LPA contacts SM-DP+, downloads the profile, and installs it.

### 2 — Push OTA (managed devices)
1. IG-Hub creates a profile on SM-DP+ and registers it with SM-DS.
2. SM-DS notifies the device's LPA that a profile is waiting.
3. LPA silently downloads and installs the profile (user may see a confirmation prompt depending on OS).
4. Suitable for school-managed devices where an MDM policy is in place.

### 3 — App-assisted (one-tap)
1. User opens the Telhone app and taps **Activate eSIM**.
2. App checks device eSIM support via OS APIs.
3. App calls IG-Hub API to generate an activation code.
4. On Android (API 28+): app uses `EuiccManager.downloadSubscription()` to trigger install without leaving the app.
5. On iOS: app deep-links into Settings with the activation URL (`esim.apple.com/activate?...`), requiring one user confirmation tap.

---

## Device Compatibility Registry

IG-Hub maintains a validated device list used during onboarding:

- On first app launch or SIM request, the app reports device model and OS version.
- IG-Hub checks the registry and routes the user to the correct flow:
  - **eSIM supported** → offer QR or app-assisted activation.
  - **eSIM not supported** → prompt user to request a physical SIM via agent or mail.
- The registry is updated continuously as new device models are validated by the Telhone engineering team.

---

## eSIM + Physical SIM Coexistence

On dual-SIM capable phones:
- User can run the Telhone eSIM alongside their existing MNO physical SIM.
- Telhone eSIM is set as the **default for data** when in Aku network coverage.
- The existing MNO SIM handles voice calls when outside Aku coverage (on devices supporting automatic SIM switching, e.g. Android Dual SIM Dual Standby).
- Users can manually override the default SIM selection from the Telhone app.

---

## Profile Lifecycle Management

| Event | Action in IG-Hub |
|---|---|
| New user onboarded | Create profile on SM-DP+; generate activation code |
| User transfers device | Revoke old profile; issue new activation code for new device |
| SIM suspended (non-payment / admin action) | Disable profile via SM-DP+ management API |
| User ports out | Profile deleted from SM-DP+; number returned to portability pool |
| Bundle change | Push policy update OTA via SM-DP+ profile refresh |

---

## Security

- Profile download uses **mutual TLS** between device LPA and SM-DP+.
- Profile credentials (Ki, OPc) never leave SM-DP+ HSM-protected storage.
- SM-DS push tokens are single-use and short-lived.
- IG-Hub audit log records every profile lifecycle event with timestamp and operator identity.

---

## Related Documents

- [Physical SIM & MVNO](physical-sim-mvno.md)
- [Telhone Application](telhone-app.md) — app-assisted eSIM activation
- [Nigeria Regulatory & Commercial Steps](regulatory.md)
- [Aku eSIM Service Overview](../../../../services/aku-esim.md)
- [eSIM Provisioning Handbook](../../../../handbooks/eSIM_Provisioning_Handbook.md)
