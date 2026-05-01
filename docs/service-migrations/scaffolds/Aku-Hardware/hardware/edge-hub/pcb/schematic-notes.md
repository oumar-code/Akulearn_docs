# Aku Edge Hub — Net-Level Schematic Notes

**KiCad project:** `aku-edge-hub-sensor-board.kicad_sch`  
**Board rev:** A  
**Last updated:** 2025-Q2

This document is the single source of truth for the EDA engineer building the KiCad
schematic. Every net name, every pin assignment, and every passive value is defined here.
Do **not** deviate from these names; they are referenced by the firmware and the wiring
guide.

---

## Net Naming Convention

| Prefix | Example | Meaning |
|--------|---------|---------|
| `+24V` | `+24V_IN` | 24 V DC power rail |
| `+5V` | `+5V_SBC` | 5 V logic / SBC rail |
| `+3V3` | `+3V3` | 3.3 V logic rail |
| `GND` | `GND` | Signal and power ground (single ground plane) |
| `I2C_` | `I2C_SDA`, `I2C_SCL` | I²C bus |
| `OW_` | `OW_DATA` | 1-Wire bus |
| `GPIO_` | `GPIO_LED_PWR` | RPi GPIO net |
| `SHUNT_` | `SHUNT_CH1_P`, `SHUNT_CH1_N` | INA3221 shunt sense pair |

---

## Component List

| Ref | Value / Part | Footprint | MPN |
|-----|-------------|-----------|-----|
| U1 | Raspberry Pi 4B 40-pin header (J1) | PinHeader_2x20_P2.54mm | — |
| U2 | INA3221AIRGVR | WQFN-16_3x3mm | TI INA3221AIRGVR |
| U3A | DS18B20 waterproof (Sensor 1 — ambient) | JST_PH_S3B-PH_1x03_P2.00mm | DS18B20 |
| U3B | DS18B20 waterproof (Sensor 2 — enclosure) | JST_PH_S3B-PH_1x03_P2.00mm | DS18B20 |
| F1 | Fuse 5A/32V automotive blade (in-line holder) | Fuse_Holder_Inline_5A | Littelfuse 0251005 |
| D1 | TVS diode 30V bidirectional 600W | DO-214AB (SMC) | Vishay SMBJ30CA |
| R1 | 4.7 kΩ 0402 (I²C SDA pull-up) | R_0402 | — |
| R2 | 4.7 kΩ 0402 (I²C SCL pull-up) | R_0402 | — |
| R3 | 4.7 kΩ 0402 (1-Wire pull-up) | R_0402 | — |
| R4 | 0.1 Ω 1 % 3 W (shunt CH1 solar) | R_2512 | Vishay WSL2512 |
| R5 | 0.1 Ω 1 % 3 W (shunt CH2 wind) | R_2512 | Vishay WSL2512 |
| R6 | 0.1 Ω 1 % 3 W (shunt CH3 load) | R_2512 | Vishay WSL2512 |
| R7 | 330 Ω 0402 (LED Power — green) | R_0402 | — |
| R8 | 330 Ω 0402 (LED Wi-Fi — blue) | R_0402 | — |
| R9 | 330 Ω 0402 (LED Sync — amber) | R_0402 | — |
| LED1 | 3 mm green LED (Power status) | LED_D3.0mm | Kingbright L-7113GD |
| LED2 | 3 mm blue LED (Wi-Fi status) | LED_D3.0mm | Kingbright L-7113QBC |
| LED3 | 3 mm amber LED (Sync status) | LED_D3.0mm | Kingbright L-7113SYC |
| C1 | 100 nF 0402 (INA3221 VCC bypass) | C_0402 | — |
| C2 | 10 µF 25 V electrolytic (24 V rail bulk) | CP_Radial_D5.0mm_P2.00mm | — |
| TB1 | 5-pole screw terminal 5.08 mm (24 V input) | TerminalBlock_Phoenix_PT-5_5P | Phoenix 1984617 |
| TB2 | 3-pole screw terminal 5.08 mm (RPi power out) | TerminalBlock_Phoenix_PT-5_3P | Phoenix 1984580 |
| J1 | 40-pin 2×20 2.54 mm pin header (RPi GPIO) | PinHeader_2x20_P2.54mm_Vertical | — |
| MH1–MH4 | M3 mounting holes (3.2 mm drill) | MountingHole_3.2mm_M3 | — |

---

## Power Input Section

### Net: `+24V_IN`

```
TB1 pin 1 (+24V_RAW)
    │
   [F1 — 5 A automotive fuse]
    │
   [D1 — SMBJ30CA TVS, cathode to +24V_IN, anode to GND]
    │
  +24V_IN ──────────────────────────────────────────────
            │               │                 │
         SHUNT_CH3_P    TB1 pin 4 (+24V_OUT)  C2 (+)
```

```
TB1 pin 5 (GND_IN) → GND plane
C2 (−) → GND plane
```

**Protection notes:**
- F1 in-line fuse interrupts on overcurrent (>5 A sustained).
- D1 TVS clamps inductive transients on the 24 V bus (e.g., motor loads on the same battery).
- C2 provides 10 µF bulk decoupling at the board entry point.

---

## INA3221 Section (U2)

### Pin Table

| INA3221 Pin | Net | Connected to |
|-------------|-----|-------------|
| VCC (pin 7) | `+3V3` | RPi J1 pin 1 (3.3 V) via C1 bypass to GND |
| GND (pin 8) | `GND` | Ground plane |
| SDA (pin 13) | `I2C_SDA` | J1 pin 3 (GPIO 2) via R1 pull-up to +3V3 |
| SCL (pin 14) | `I2C_SCL` | J1 pin 5 (GPIO 3) via R2 pull-up to +3V3 |
| A0 (pin 10) | `GND` | Ground plane (I²C addr bit 0 = 0) |
| A1 (pin 11) | `GND` | Ground plane (I²C addr bit 1 = 0) → addr **0x40** |
| IN1+ (pin 1) | `SHUNT_CH1_P` | Solar PV 24 V line (source side) |
| IN1− (pin 2) | `SHUNT_CH1_N` | Solar PV 24 V line (load side) via R4 0.1 Ω |
| IN2+ (pin 3) | `SHUNT_CH2_P` | Wind turbine 24 V line (source side) |
| IN2− (pin 4) | `SHUNT_CH2_N` | Wind turbine 24 V line (load side) via R5 0.1 Ω |
| IN3+ (pin 5) | `SHUNT_CH3_P` | Load bus 24 V (from +24V_IN after TVS) |
| IN3− (pin 6) | `SHUNT_CH3_N` | Load bus 24 V (output to TB1 pin 4) via R6 0.1 Ω |
| VBUS1 (pin 15)| `SHUNT_CH1_P` | Bus voltage sense CH1 (same as IN1+) |
| VBUS2 (pin 16)| `SHUNT_CH2_P` | Bus voltage sense CH2 (same as IN2+) |
| ALERT (pin 9) | — | NC (no alert interrupt used in Rev A) |
| VSCOM (pin 12)| `GND` | Ground |

**I²C pull-ups:**
- R1: 4.7 kΩ from `I2C_SDA` to `+3V3`
- R2: 4.7 kΩ from `I2C_SCL` to `+3V3`
- C1: 100 nF from U2 VCC pin to GND (place within 0.5 mm of pin)

### Shunt Resistor Wiring

Each shunt is in **series** with the positive power rail:

```
Source (+24V) → R_shunt (0.1 Ω) → Load (+24V)
               ↑ IN+              ↑ IN−
               └── INA3221 sense pins
```

> ⚠️ **Polarity:** IN+ must face the source (higher potential). Reversed polarity gives
> a negative reading and may damage U2 if the differential exceeds ±26 V.

---

## DS18B20 1-Wire Section (U3A, U3B)

Both sensors share a single 1-Wire bus on `OW_DATA`.

### Net: `OW_DATA`

```
J1 pin 7 (GPIO 4) ─────── OW_DATA ─────── R3 (4.7 kΩ) ── +3V3
                                  │
                           JST-PH J_U3A pin 2 (DATA)
                           JST-PH J_U3B pin 2 (DATA)
```

### JST-PH 3-pin Connector Pinout (both U3A and U3B)

| Pin | Signal | Net |
|-----|--------|-----|
| 1 | GND | `GND` |
| 2 | DATA | `OW_DATA` |
| 3 | VCC | `+3V3` |

**Notes:**
- R3 (4.7 kΩ) is the single bus pull-up; do **not** add a second pull-up at the sensor.
- U3A (ambient) connects via a long cable (≤ 2 m); U3B (enclosure) connects via a short tail (≤ 0.3 m).
- Both devices coexist on the same bus; the firmware discovers them by ROM address at boot.

---

## Status LED Section (LED1, LED2, LED3)

All LEDs are driven directly from RPi GPIO pins through current-limiting resistors.
GPIO output voltage = 3.3 V; LED forward voltage V_f ≈ 2.0 V (green/amber), 2.8 V (blue).
Resistor calculation: R = (3.3 − V_f) / 10 mA ≈ 330 Ω.

### Net Connections

| Ref | Anode net | Cathode net | GPIO pin | RPi physical pin |
|-----|-----------|-------------|----------|-----------------|
| LED1 (green) | `GPIO_LED_PWR` via R7 (330 Ω) | `GND` | GPIO 22 | Pin 15 |
| LED2 (blue) | `GPIO_LED_WIFI` via R8 (330 Ω) | `GND` | GPIO 23 | Pin 16 |
| LED3 (amber) | `GPIO_LED_SYNC` via R9 (330 Ω) | `GND` | GPIO 24 | Pin 18 |

```
J1 pin 15 (GPIO 22) ─── R7 (330 Ω) ─── LED1 anode → LED1 cathode → GND
J1 pin 16 (GPIO 23) ─── R8 (330 Ω) ─── LED2 anode → LED2 cathode → GND
J1 pin 18 (GPIO 24) ─── R9 (330 Ω) ─── LED3 anode → LED3 cathode → GND
```

---

## RPi 40-Pin Header (J1) — Used Nets

Only pins used on this board are listed; all others are NC on the PCB.

| Physical Pin | BCM GPIO | Net on PCB | Destination |
|-------------|----------|-----------|-------------|
| 1 | 3.3 V | `+3V3` | Pull-up rails (R1, R2, R3), INA3221 VCC |
| 2 | 5 V | — | NC |
| 3 | GPIO 2 (SDA) | `I2C_SDA` | U2 SDA |
| 5 | GPIO 3 (SCL) | `I2C_SCL` | U2 SCL |
| 6 | GND | `GND` | Ground plane |
| 7 | GPIO 4 | `OW_DATA` | DS18B20 bus |
| 9 | GND | `GND` | Ground plane |
| 15 | GPIO 22 | `GPIO_LED_PWR` | R7 → LED1 |
| 16 | GPIO 23 | `GPIO_LED_WIFI` | R8 → LED2 |
| 18 | GPIO 24 | `GPIO_LED_SYNC` | R9 → LED3 |

---

## ERC / Schematic Sign-off Checklist

- [ ] All VCC / GND pins connected (no unconnected power pins)
- [ ] INA3221 A0, A1 explicitly tied to GND (not floating)
- [ ] DS18B20 pull-up R3 present on `OW_DATA`
- [ ] C1 bypass placed next to U2 VCC pin in schematic
- [ ] TVS D1 anode-to-GND, cathode-to-+24V_IN orientation correct
- [ ] Fuse F1 on positive (+24V) rail only
- [ ] All mounting holes MH1–MH4 as non-electrical
- [ ] Net names match firmware constants in `src/sensors/ina3221.py`
- [ ] ERC run in KiCad — 0 errors, 0 warnings
