# Aku-Hardware

Hardware design, firmware, and manufacturing documentation for the **Aku Platform**
physical devices — the Aku Edge Hub compute node, the Aku Projector module, and the
solar/wind hybrid power system that powers both.

[![Firmware CI](https://github.com/oumar-code/Aku-Hardware/actions/workflows/firmware-ci.yml/badge.svg)](https://github.com/oumar-code/Aku-Hardware/actions/workflows/firmware-ci.yml)

---

## Ecosystem Context

The Aku Platform is a tiered EdTech ecosystem delivering offline-first, AI-powered
education to connected and underserved communities across Nigeria and West Africa.
The hardware layer (this repo) is Tier 1 of that architecture:

```
Learner Devices
      │
  Aku Edge Hub  ◄─── this repo (hardware design + firmware)
  + Projector
  + Solar/Wind power
      │
  Aku-EdgeHub (software — oumar-code/Aku-EdgeHub)
      │
  Aku Super Hub (cloud — oumar-code/Aku-SuperHub)
      │
  Aku IG-Hub (global — oumar-code/Aku-IGHub)
```

Full ecosystem map: https://github.com/oumar-code/Akulearn_docs/blob/main/docs/ecosystem-map.md

---

## Repository Layout

```
Aku-Hardware/
├── hardware/
│   ├── edge-hub/          # Compute node — SBC, storage, connectivity
│   │   ├── README.md
│   │   ├── specs.md       # Full hardware specification table
│   │   ├── bom.md         # Bill of Materials (prototype + production)
│   │   ├── wiring.md      # Wiring & connector guide
│   │   └── assembly.md    # Step-by-step assembly procedure
│   ├── projector/         # Projector module (DLP/LED) + mounting
│   │   ├── README.md
│   │   ├── specs.md
│   │   └── bom.md
│   ├── power-system/      # Solar + wind hybrid power subsystem
│   │   ├── README.md      # System overview & block diagram
│   │   ├── solar-subsystem.md
│   │   ├── wind-turbine.md    # Includes blade aerodynamics
│   │   ├── battery-storage.md
│   │   └── energy-monitoring.md  # INA3221 sensor integration
│   └── enclosure/         # Ruggedised enclosure design
│       └── README.md
├── firmware/
│   ├── README.md          # Toolchain setup & flash instructions
│   ├── energy-monitor/    # INA3221 multi-channel sensor (MicroPython)
│   │   ├── README.md
│   │   └── main.py
│   └── device-watchdog/   # Hardware watchdog for SBC supervision
│       └── README.md
├── testing/
│   ├── README.md
│   ├── power-system-test.md        # Power system acceptance tests
│   └── edge-hub-integration-test.md
├── docs/
│   ├── manufacturing-guide.md  # Production manufacturing notes
│   ├── field-deployment.md     # Site installation & commissioning
│   └── maintenance.md          # Preventive & corrective maintenance
├── .github/
│   └── workflows/
│       └── firmware-ci.yml     # Lint & unit-test firmware on every PR
├── CONTRIBUTING.md
└── .gitignore
```

---

## Quick Start

### Read the Docs

Browse the documentation in this repo order:

1. [Hardware — Edge Hub](hardware/edge-hub/README.md)
2. [Hardware — Power System](hardware/power-system/README.md)
3. [Hardware — Projector](hardware/projector/README.md)
4. [Firmware](firmware/README.md)
5. [Testing](testing/README.md)
6. [Field Deployment](docs/field-deployment.md)

### Flash the Energy Monitor Firmware

```bash
# Prerequisites: Python 3.11+, mpremote
pip install mpremote

# Connect Raspberry Pi Pico (or equivalent RP2040 board) via USB
# Flash MicroPython firmware once (download from micropython.org/download/rp2-pico/)
mpremote connect auto run firmware/energy-monitor/main.py
```

---

## Hardware Overview

### Aku Edge Hub

| Subsystem | Prototype | Production Target |
|-----------|-----------|-------------------|
| SBC | Raspberry Pi 4B (4 GB) | Jetson Orin Nano / RK3588 |
| Storage | 256 GB NVMe SSD | Industrial eMMC + NVMe |
| Wi-Fi | AP mode, Wi-Fi 5 | Wi-Fi 6, dual-band |
| Power input | 24 V DC (hybrid charge controller) | 24 V / 48 V DC bus |
| Battery | LiFePO4 50 Ah @ 24 V (1.2 kWh) | Expandable to 2.4 kWh |
| Solar | 100–200 Wp monocrystalline | 200–400 Wp (site-specific) |
| Wind | 300–500 W small HAWT | 500 W–1 kW site-optimised |
| Energy sensor | INA3221 (3-channel I²C) | Same |

Full specs: [hardware/edge-hub/specs.md](hardware/edge-hub/specs.md)

### Power Block Diagram

```
Solar Panel(s) ──►┐
                  │  Hybrid MPPT Charge Controller
Wind Turbine  ──►─┤  + Dump-Load Controller
                  │
                  ▼
           LiFePO4 Battery Bank (BMS)
                  │
                  ▼
        DC-UPS / Inverter-Charger
        ├── 12 V / 19 V DC → SBC, Wi-Fi, Storage
        └── 230 V AC        → Projector Module
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching strategy, commit conventions,
and how to submit hardware changes (schematic diffs, BOM updates, firmware PRs).

---

## Related Repositories

| Repo | Role |
|------|------|
| [Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) | Software stack running on this hardware |
| [Akulearn_docs](https://github.com/oumar-code/Akulearn_docs) | Platform-level documentation & ecosystem map |
| [Aku-SmartBoard](https://github.com/oumar-code/Aku-SmartBoard) | Classroom client app (KMP/Compose Desktop) |
