# Aku Edge Hub — Enclosure Design

---

## Overview

The Aku Edge Hub is housed in a ruggedised steel enclosure rated **IP54**
(dust-protected, splash-resistant). The enclosure protects the electronics from
the harsh environmental conditions of rural deployments — dust, humidity, insects,
and occasional rain splash.

---

## Enclosure Specification

| Parameter | Value |
|-----------|-------|
| Material | 1.5 mm powder-coated mild steel (RAL 7035 light grey) |
| Dimensions (W × H × D) | 300 × 200 × 120 mm |
| IP rating | IP54 |
| Wall thickness | 1.5 mm |
| Lid fastening | 4 × M4 captive screws (quarter-turn) |
| Cable entry | 4 × PG-thread knockouts (bottom face) |
| Mounting | M5 keyhole slots on rear (wall mount) or DIN-rail mounting |
| Operating temperature | 0 °C to +55 °C ambient |
| Ventilation | Passive louvres with insect mesh (IP54 maintained) |

---

## Internal Layout

```
┌─────────────────────────────────────────────┐
│  ┌──────────────┐   ┌─────────────────────┐ │
│  │ RPi 4B +     │   │  INA3221 breakout   │ │
│  │ M.2 HAT      │   │  DS18B20 connectors │ │
│  └──────────────┘   └─────────────────────┘ │
│                                              │
│  ┌────────────┐  ┌────────────┐             │
│  │ 24V→5V     │  │ 24V→12V   │             │
│  │ Buck conv. │  │ Buck conv. │             │
│  └────────────┘  └────────────┘             │
│                                              │
│  ┌─────────────────────────────────────────┐ │
│  │  DIN rail — terminal blocks TB1–TB4     │ │
│  └─────────────────────────────────────────┘ │
│                                              │
│  (Lid — top face)                            │
│  ┌──┐ ┌──┐ ┌──┐   Status LEDs              │
│  │ ●│ │ ●│ │ ●│   Power / Wi-Fi / Sync     │
│  └──┘ └──┘ └──┘                             │
└─────────────────────────────────────────────┘
```

---

## Cable Gland Layout (Bottom Face)

| Gland | Thread | Cable | Purpose |
|-------|--------|-------|---------|
| KO1 | PG16 (25 mm) | 18 AWG 2-core | 24 V DC input from charge controller |
| KO2 | PG13.5 (20 mm) | HDMI cable | Projector video output |
| KO3 | PG11 (16 mm) | Cat5e Ethernet | ISP / satellite modem uplink |
| KO4 | PG11 (16 mm) | USB 3.0 | Optional external SSD |

---

## Thermal Management

- The Argon ONE M.2 HAT aluminium case acts as the primary SBC heatsink.
- Passive louvres allow convective cooling; enclosure internal temperature should
  remain ≤ 20 °C above ambient under typical operating conditions.
- If enclosure temperature exceeds 50 °C (read from DS18B20), the Edge Hub firmware
  throttles the CPU and sends a `HIGH_TEMP` alert to the Super Hub.

---

## Production Enclosure Options

| Option | Description | IP | Est. Cost |
|--------|-------------|-----|-----------|
| Custom sheet-metal | Locally fabricated (Kano / Lagos metal shops) | IP54 | ~$25 |
| Fibox PC series | Off-the-shelf polycarbonate | IP65 | ~$45 |
| Spelsberg TG series | Off-the-shelf steel | IP66 | ~$55 |

---

## Future Work

- [ ] Finalise cable gland positions and drill template
- [ ] Create CAD drawing (FreeCAD) for custom enclosure fabrication
- [ ] Validate IP54 rating with water spray test
- [ ] Add asset tag / QR code slot to lid for field inventory scanning
