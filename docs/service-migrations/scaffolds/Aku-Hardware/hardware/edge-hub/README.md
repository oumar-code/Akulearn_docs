# Aku Edge Hub — Hardware Overview

The Aku Edge Hub is the **Tier 1 compute node** of the Aku Platform. It is
deployed at schools, clinics, and community centres to provide:

- Offline-first content delivery and local AI inference (Gemma)
- Wi-Fi hotspot for up to 50 simultaneous learner devices
- IoT sensor gateway with Prometheus metrics endpoint
- Resilient solar/wind hybrid power supply

---

## Hardware Generations

| Generation | SBC | Status |
|------------|-----|--------|
| **Prototype (Gen 1)** | Raspberry Pi 4 Model B (4 GB) | ✅ Active |
| **Production (Gen 2)** | NVIDIA Jetson Orin Nano 8 GB | ⏳ Planned (Phase 2) |
| **Production Alt** | Rockchip RK3588 SOM (8 GB) | ⏳ Under evaluation |

---

## Documents in this Directory

| File | Contents |
|------|----------|
| [`specs.md`](specs.md) | Complete hardware specification table |
| [`bom.md`](bom.md) | Bill of Materials — prototype and production |
| [`wiring.md`](wiring.md) | Connector pinouts, I²C/SPI bus map, power rails |
| [`assembly.md`](assembly.md) | Step-by-step assembly and test procedure |

---

## Block Diagram

```
┌──────────────────────────────────────────────────────────┐
│  Aku Edge Hub (Prototype — Raspberry Pi 4B)              │
│                                                          │
│  ┌─────────────┐   I²C   ┌──────────────────────────┐  │
│  │  RPi 4B     │ ◄──────► │  INA3221 Energy Monitor   │  │
│  │  (compute)  │         │  CH1: Solar PV             │  │
│  │             │         │  CH2: Wind turbine DC      │  │
│  │  USB 3.0    │─────────►│  CH3: Load current        │  │
│  │  GPIO 40-pin│         └──────────────────────────┘  │
│  └──────┬──────┘                                        │
│         │ PCIe (M.2)                                    │
│  ┌──────▼──────┐   USB    ┌──────────────────────────┐  │
│  │  256 GB     │         │  Wi-Fi 5 Access Point     │  │
│  │  NVMe SSD   │         │  (TP-Link EAP225 / hostapd│  │
│  └─────────────┘         └──────────────────────────┘  │
│                                                          │
│  Power Input: 24 V DC from Hybrid MPPT Charge Controller │
│  ├── 5 V / 3 A (USB-C PD — RPi 4B)                     │
│  └── 12 V / 2 A (Wi-Fi AP)                              │
└──────────────────────────────────────────────────────────┘
```

---

## Related

- [Power System](../power-system/README.md) — full solar/wind power design
- [Wiring Guide](wiring.md) — connector assignments and cable specs
- [Aku-EdgeHub software repo](https://github.com/oumar-code/Aku-EdgeHub)
