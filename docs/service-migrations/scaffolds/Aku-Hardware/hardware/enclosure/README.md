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

## CAD / DXF Files

> **Status:** ⏳ FreeCAD design in progress — DXF drill template pending

This directory will contain the following FreeCAD and DXF design files for
locally fabricating the custom sheet-metal enclosure:

| File | Description |
|------|-------------|
| `enclosure-body.FCStd` | FreeCAD 0.21 main model — sheet-metal body, lid, DIN-rail bosses |
| `enclosure-body.dxf` | DXF R12 — flat pattern for CNC sheet-metal cutting |
| `enclosure-lid.dxf` | DXF R12 — lid flat pattern + LED and cable-gland punch positions |
| `enclosure-drill-template.dxf` | DXF drill template: M4 lid holes, M5 wall-mount keyhole, KO1–KO4 |
| `enclosure-assembly.step` | STEP AP214 — full assembly for clearance check |

### DXF Drill Template Details

The drill template covers:

| Feature | Position (from bottom-left corner) | Diameter |
|---------|-------------------------------------|----------|
| M4 lid screws (×4 corners) | (10,10), (290,10), (10,190), (290,190) | 4.5 mm |
| M5 wall-mount keyholes (×2) | (60,100), (240,100) | 8 mm head / 5.5 mm slot |
| KO1 (PG16, 24 V input) | (50, bottom) | 22 mm |
| KO2 (PG13.5, HDMI) | (120, bottom) | 20 mm |
| KO3 (PG11, Ethernet) | (190, bottom) | 16 mm |
| KO4 (PG11, USB) | (250, bottom) | 16 mm |
| Status LED holes (×3) | Lid top face: (130,30), (150,30), (170,30) | 5 mm |
| PIR aperture | Lid top face: (250,30) | 8 mm |

All dimensions in millimetres. Tolerance: ±0.5 mm for cable glands, ±0.2 mm for mounting holes.

### Fabrication Instructions (Custom Sheet-Metal)

1. Export `enclosure-body.dxf` and `enclosure-drill-template.dxf` to a USB stick.
2. Take to a sheet-metal shop (Kano / Lagos market); request 1.5 mm mild steel, powder-coat RAL 7035.
3. Request CNC plasma or laser cutting from the flat DXF pattern.
4. Specify the following cable-gland knockouts: 1 × PG16, 1 × PG13.5, 2 × PG11 (all bottom face).
5. Request M4 captive-screw inserts in the lid corners (or supply quarter-turn fasteners).
6. After fabrication, validate fit against the STEP assembly file before powder coating.

---

## Status Checklist

- [x] Enclosure specification defined (dimensions, IP rating, material)
- [x] Internal layout and cable gland positions defined
- [x] DXF drill template dimensions documented
- [ ] FreeCAD model (`enclosure-body.FCStd`) — **in progress**
- [ ] DXF flat patterns exported and verified at sheet-metal shop
- [ ] Prototype enclosure fabricated (custom or off-the-shelf Fibox)
- [ ] IP54 rating validated with water-spray test
- [ ] Asset tag / QR code slot added to lid for field inventory scanning
- [ ] STEP assembly clearance check passed

---

## Related

- [Assembly procedure](../edge-hub/assembly.md) — references enclosure drill positions
- [Wiring guide](../edge-hub/wiring.md) — cable gland assignments
- [PCB design](../edge-hub/pcb/README.md) — PCB mounts on M3 standoffs inside enclosure

