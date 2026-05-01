# Aku Edge Hub PCB — Component Placement Guide

**Board size:** 100 mm × 60 mm  
**Origin:** Bottom-left corner of board outline (0, 0)  
**Layer F.Cu** = component side (top face of installed board)

This document gives the starting placement for every component. The KiCad layout
engineer should use these coordinates as the initial placement target and adjust for
routing, but **must not** change zone assignments (power vs. signal sides) without
updating this document.

---

## Board Zones

```
┌──────────────────────────────────────────────────────────────┐
│ Y=60mm                                                        │
│                                                               │
│  ┌──────────────────────────────┐   ┌────────────────────┐   │
│  │  POWER ZONE                  │   │ SENSOR ZONE        │   │
│  │  TB1, TB2, F1, D1, C2        │   │ U2 (INA3221)       │   │
│  │  R4, R5, R6 (shunts)         │   │ R1, R2, C1         │   │
│  └──────────────────────────────┘   │ J_U3A, J_U3B, R3   │   │
│                                     └────────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  RPi INTERFACE ZONE                                   │   │
│  │  J1 (40-pin header) — flush with left/bottom edge     │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                               │
│   LED ZONE (top-right corner, near board edge for lid holes) │
│   LED1, R7, LED2, R8, LED3, R9                               │
│                                                               │
│  MH1 ●                                             ● MH2    │
│      (5, 5)                                    (95, 5)       │
│  MH3 ●                                             ● MH4    │
│      (5, 55)                                   (95, 55)      │
│                                                               │
│ Y=0mm ────────────────────────────────────────────── X=100mm │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Placement Table

All coordinates are (X, Y) in mm from bottom-left origin.  
Rotation is in degrees, counter-clockwise positive, 0° = default KiCad orientation.

| Ref | Description | X (mm) | Y (mm) | Rot (°) | Layer | Notes |
|-----|-------------|--------|--------|---------|-------|-------|
| J1 | 40-pin RPi header | 10.0 | 8.0 | 0 | F.Cu | Bottom-left zone; pin 1 at (10, 27.9) |
| TB1 | 5-pole terminal block (24 V in) | 8.0 | 46.0 | 0 | F.Cu | Left edge, power entry; pin 1 nearest X=0 |
| TB2 | 3-pole terminal block (RPi out) | 8.0 | 38.0 | 0 | F.Cu | Left edge, below TB1 |
| F1 | Fuse holder (in-line, THT) | 22.0 | 46.0 | 0 | F.Cu | Series with +24V_RAW from TB1 |
| D1 | TVS SMBJ30CA (SMC) | 32.0 | 46.0 | 0 | F.Cu | Anode to GND (B.Cu pour), cathode to +24V_IN |
| C2 | 10 µF / 25 V electrolytic | 40.0 | 46.0 | 0 | F.Cu | Bulk decap; + terminal to +24V_IN |
| R4 | 0.1 Ω shunt CH1 (R_2512) | 55.0 | 50.0 | 0 | F.Cu | Solar shunt; wide traces, no soldermask bridge |
| R5 | 0.1 Ω shunt CH2 (R_2512) | 68.0 | 50.0 | 0 | F.Cu | Wind shunt |
| R6 | 0.1 Ω shunt CH3 (R_2512) | 81.0 | 50.0 | 0 | F.Cu | Load shunt |
| U2 | INA3221 WQFN-16 | 62.0 | 38.0 | 0 | F.Cu | Centre of sensor zone; pin 1 mark = top-left |
| C1 | 100 nF bypass (0402) | 62.0 | 33.5 | 0 | F.Cu | As close to U2 VCC pin 7 as possible (< 0.5 mm) |
| R1 | 4.7 kΩ I2C SDA pull-up (0402) | 55.0 | 38.0 | 0 | F.Cu | Between J1 pin 3 and +3V3 rail |
| R2 | 4.7 kΩ I2C SCL pull-up (0402) | 55.0 | 35.0 | 0 | F.Cu | Between J1 pin 5 and +3V3 rail |
| J_U3A | JST-PH 3-pin (DS18B20 ambient) | 75.0 | 30.0 | 0 | F.Cu | Facing board edge for cable routing |
| J_U3B | JST-PH 3-pin (DS18B20 encl.) | 83.0 | 30.0 | 0 | F.Cu | Adjacent to J_U3A |
| R3 | 4.7 kΩ 1-Wire pull-up (0402) | 75.0 | 24.0 | 0 | F.Cu | Between OW_DATA and +3V3 |
| LED1 | 3 mm green LED (Power) | 88.0 | 46.0 | 0 | F.Cu | Top-right zone; leads through lid hole |
| R7 | 330 Ω LED1 resistor (0402) | 88.0 | 41.0 | 0 | F.Cu | Series with LED1 |
| LED2 | 3 mm blue LED (Wi-Fi) | 93.0 | 46.0 | 0 | F.Cu | Adjacent to LED1 |
| R8 | 330 Ω LED2 resistor (0402) | 93.0 | 41.0 | 0 | F.Cu | Series with LED2 |
| LED3 | 3 mm amber LED (Sync) | 88.0 | 53.0 | 0 | F.Cu | Third LED |
| R9 | 330 Ω LED3 resistor (0402) | 88.0 | 48.0 | 0 | F.Cu | Series with LED3 |
| MH1 | M3 mounting hole | 5.0 | 5.0 | 0 | — | Bottom-left corner |
| MH2 | M3 mounting hole | 95.0 | 5.0 | 0 | — | Bottom-right corner |
| MH3 | M3 mounting hole | 5.0 | 55.0 | 0 | — | Top-left corner |
| MH4 | M3 mounting hole | 95.0 | 55.0 | 0 | — | Top-right corner |

---

## Routing Guidance

### Critical paths (route first)

1. **INA3221 shunt pairs** — `SHUNT_CH*_P` and `SHUNT_CH*_N` traces must be equal
   length (±1 mm) and routed in parallel to minimise differential noise.
   Use 3.0 mm traces; avoid sharp bends.

2. **+24V_IN bus** — run a 3.0 mm trace from TB1 pin 1 → F1 → D1 cathode → C2+ → R4/R5/R6 source pins.
   Keep all 24 V traces on the top-left and top-centre of the board, away from J1.

3. **I²C bus** — route SDA and SCL as a parallel pair (0.25 mm, 0.25 mm gap) from J1
   to R1/R2 pull-ups and then to U2. Keep total length < 100 mm.

4. **1-Wire bus** — single 0.25 mm trace from J1 pin 7 to R3, then to J_U3A and J_U3B.

### Keep-out rules

- No signal vias within 2 mm of shunt resistors R4, R5, R6.
- No 24 V traces within 1 mm of the INA3221 signal pins (pins 1–6, 13–14).
- Silkscreen reference labels must not overlap solder pads.

---

## Mechanical Constraints

- Board outline: 100 mm × 60 mm rectangle on `Edge.Cuts` layer.
- Corner radius: 1 mm (optional, eases handling).
- Mounting holes MH1–MH4: non-plated, 3.2 mm drill, no copper pad.
- Standoff clearance: 6 mm diameter keep-out zone around each mounting hole on all layers.
- Maximum component height F.Cu side: 15 mm (limited by DIN-rail standoff height inside enclosure).
- Maximum component height B.Cu side: 0 mm (board sits flat on standoff tops — no B.Cu components).
