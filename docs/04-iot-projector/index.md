# Akulearn IoT Projector & Edge Hub — Development Guidelines

This section covers the full hardware layer of the Aku Platform: the **Aku Edge Hub** compute node, the **Aku Projector Module**, and the **solar/wind hybrid power system** that powers both.

> **Canonical hardware repo:** [oumar-code/Aku-Hardware](https://github.com/oumar-code/Aku-Hardware)  
> **Software stack for Edge Hub:** [oumar-code/Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub)  
> **Classroom app (SmartBoard):** [oumar-code/Aku-SmartBoard](https://github.com/oumar-code/Aku-SmartBoard)

---

## Architecture Overview

```
Learner Devices (phones, tablets)
        │  Wi-Fi (Akulearn_Hub SSID)
        ▼
Aku Edge Hub  ◄─── Aku-Hardware repo (hardware design + firmware)
  │  Raspberry Pi 4B / Jetson Orin Nano
  │  INA3221 energy monitor (solar + wind + load telemetry)
  │  SQLite content cache + FAISS vector index
  │
  ├── HDMI ──► Aku Projector Module (LED/DLP, 2000–3600 lm)
  │
  └── 4G/Ethernet uplink ──► Aku-SuperHub (cloud)
```

The Edge Hub operates **offline-first** — all content, AI inference (Gemma 2B), and curriculum access are served locally from the device with no internet dependency.

---

## Hardware Specifications

Full technical documentation lives in [Aku-Hardware](https://github.com/oumar-code/Aku-Hardware):

| Document | Description |
|----------|-------------|
| [Edge Hub — Specs](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/edge-hub/specs.md) | SBC, storage, networking, power, sensors |
| [Edge Hub — BOM](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/edge-hub/bom.md) | ~275 USD prototype Bill of Materials |
| [Edge Hub — Wiring](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/edge-hub/wiring.md) | I²C, power rails, GPIO assignments |
| [Edge Hub — Assembly](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/edge-hub/assembly.md) | Step-by-step 11-stage assembly procedure |
| [Projector — Specs](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/projector/specs.md) | Display requirements, connectivity, power |
| [Projector — BOM](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/projector/bom.md) | ~490 USD projector kit |
| [Enclosure Design](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/enclosure/README.md) | IP54 steel enclosure, thermal management |

### Key Hardware Components

| Component | Prototype (Gen 1) | Production Target (Gen 2) |
|-----------|-------------------|---------------------------|
| SBC | Raspberry Pi 4B 4 GB | NVIDIA Jetson Orin Nano 8 GB |
| Storage | 256 GB NVMe SSD (M.2 + HAT) | 256 GB industrial eMMC |
| Wi-Fi AP | TP-Link EAP225 (Wi-Fi 5) | Wi-Fi 6 AP module |
| Projector | ViewSonic PA503W DLP, 3600 lm | 3000+ lm LED, short-throw |
| Energy sensor | INA3221 3-channel I²C | Same |
| Enclosure | IP54 steel, 300×200×120 mm | Same |

---

## Power System

The Edge Hub is powered by a **solar + wind hybrid system** with LiFePO4 battery storage — enabling fully off-grid operation:

| Document | Description |
|----------|-------------|
| [Solar Subsystem](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/power-system/solar-subsystem.md) | 100–200 Wp panel, MPPT controller |
| [Wind Turbine](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/power-system/wind-turbine.md) | 300–500 W HAWT, NACA 4412 blade aerodynamics |
| [Battery Storage](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/power-system/battery-storage.md) | 50 Ah LiFePO4 @ 24 V, BMS |
| [Energy Monitoring](https://github.com/oumar-code/Aku-Hardware/blob/main/hardware/power-system/energy-monitoring.md) | INA3221 Prometheus metrics, channel assignment |

Daily energy budget: **780 Wh/day** (SBC 24 h + projector 3 h). Target autonomy: **2 days** without generation.

---

## Firmware

| Firmware Module | Target MCU | Status |
|----------------|------------|--------|
| [INA3221 Energy Monitor](https://github.com/oumar-code/Aku-Hardware/blob/main/firmware/energy-monitor/main.py) | Raspberry Pi Pico (RP2040), MicroPython | ✅ Production-ready — 1 Hz JSON stream |
| [Device Watchdog](https://github.com/oumar-code/Aku-Hardware/blob/main/firmware/device-watchdog/main.py) | Raspberry Pi Pico (RP2040), MicroPython | ✅ Implemented — reboots SBC on heartbeat timeout |

The energy monitor firmware streams JSON telemetry over USB serial to the Aku-EdgeHub software stack, which exposes readings as Prometheus metrics at `/metrics`.

---

## Content Delivery & Offline Sync

The Edge Hub runs the [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) FastAPI service:

- **Local SQLite cache** — mirrors curriculum content chunks and LO catalog from Akudemy
- **FAISS vector index** — semantic search over cached content (≤ 500 MB)
- **Delta sync** — pulls content updates from Akudemy during connectivity windows (`GET /api/v1/content/sync?since=<ISO>`)
- **Offline AI inference** — Gemma 2B GGUF model served locally when internet is unavailable

---

## Security & Device Management

- **JWT authentication** — all API endpoints require a valid JWT (issued by Aku-SuperHub)
- **Device attestation** — Edge Hub registers with Aku-IGHub on first boot; hardware fingerprint stored
- **Encrypted storage** — PII fields in SQLite are field-level encrypted
- **OTA updates** — firmware and software updates delivered via Aku-SuperHub sync agent; SHA-256 verified before activation

---

## Facilitator Interface

The **Aku-SmartBoard** application ([oumar-code/Aku-SmartBoard](https://github.com/oumar-code/Aku-SmartBoard)) runs on the Edge Hub and provides:

- Lesson playback (video, PDF, interactive content)
- Attendance recording
- Quiz delivery and result collection
- Presenter remote support (Logitech R400 via Aku-SmartBoard facilitator interface)

---

## Testing & Commissioning

| Test Procedure | Location |
|----------------|----------|
| Power system acceptance test (7 stages) | [Aku-Hardware/testing/power-system-test.md](https://github.com/oumar-code/Aku-Hardware/blob/main/testing/power-system-test.md) |
| Edge Hub integration + 24 h soak test (8 stages) | [Aku-Hardware/testing/edge-hub-integration-test.md](https://github.com/oumar-code/Aku-Hardware/blob/main/testing/edge-hub-integration-test.md) |

Field deployment procedure: [Aku-Hardware/docs/field-deployment.md](https://github.com/oumar-code/Aku-Hardware/blob/main/docs/field-deployment.md)

---

## Integration with Aku Platform Services

| Integration | Description |
|-------------|-------------|
| **Aku-EdgeHub** | Consumes INA3221 JSON stream via `/dev/ttyACM0`; exposes Prometheus metrics at `/metrics` |
| **Aku-SuperHub** | Aggregates per-unit energy telemetry (fleet-level dashboards) |
| **AkuAI** | Anomaly detection on power system telemetry; flags faults in Prometheus alerts |
| **Akudemy** | Hardware provisioning checklist embedded in facilitator onboarding flow |
| **Aku-Content** | Hardware installation videos and maintenance SOPs stored as offline content |

---

## Related Documentation

| Document | Location |
|----------|----------|
| Ecosystem map (Aku-Hardware entry) | [`docs/ecosystem-map.md`](../ecosystem-map.md) |
| Clean energy power system (design reference) | [`docs/hardware/clean_energy_power_system.md`](../hardware/clean_energy_power_system.md) |
| KPI dashboard spec (Prometheus metrics) | [`monitoring/kpi_dashboard_spec.md`](../monitoring/kpi_dashboard_spec.md) |
| Pilot playbook | [`docs/rollout/zamfara_pilot_plan.md`](../rollout/zamfara_pilot_plan.md) |
