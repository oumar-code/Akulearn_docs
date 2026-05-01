# Aku Edge Hub PCB — Design Rules

**KiCad file:** `aku-edge-hub-sensor-board.kicad_dru`  
**Board:** 2-layer FR4, 100 mm × 60 mm  
**Revision:** A

Use these rules when configuring the KiCad Board Setup → Design Rules dialog and when
writing the `.kicad_dru` constraint file. All values are **minimum** unless marked
as preferred.

---

## Layer Stackup

| Layer | Name | Copper weight | Purpose |
|-------|------|--------------|---------|
| F.Cu | Front copper | 1 oz (35 µm) | Signal + power routes |
| B.Cu | Back copper | 1 oz (35 µm) | Ground plane (poured) |
| F.Mask | Front solder mask | — | Green (standard) |
| B.Mask | Back solder mask | — | Green |
| F.SilkS | Front silkscreen | — | White |
| B.SilkS | Back silkscreen | — | White |
| F.Fab | Fab layer | — | Component courtyard notes |
| Edge.Cuts | Board outline | — | 100 × 60 mm rectangle |

**Dielectric:** FR4, Tg ≥ 130 °C, thickness 1.6 mm  
**Surface finish:** HASL lead-free (HF)  
**Min finished board thickness:** 1.4 mm / max 1.8 mm

---

## Clearances

| Rule | Min value | Notes |
|------|-----------|-------|
| Signal–signal clearance | 0.20 mm | All logic nets |
| Signal–24 V power clearance | 1.00 mm | `+24V_IN`, shunt nets |
| Signal–GND clearance | 0.20 mm | |
| 24 V–24 V clearance | 0.50 mm | Between power-rail pads/traces |
| Copper–board edge | 0.30 mm | All copper layers |
| Solder mask expansion | 0.05 mm | Standard |
| Courtyard clearance | 0.25 mm | No component courtyard overlap |

---

## Trace Widths

| Net class | Min width | Preferred width | Max current |
|-----------|-----------|-----------------|-------------|
| Default (signal) | 0.20 mm | 0.30 mm | — |
| I2C (SDA, SCL) | 0.20 mm | 0.25 mm | < 50 mA |
| 1-Wire (OW_DATA) | 0.20 mm | 0.25 mm | < 10 mA |
| GPIO (LED, PIR) | 0.20 mm | 0.25 mm | < 50 mA |
| +3V3 supply | 0.50 mm | 0.80 mm | ≤ 200 mA |
| +24V_IN (power) | 2.50 mm | 3.00 mm | ≤ 5 A |
| Shunt traces (SHUNT_CH*) | 2.50 mm | 3.00 mm | ≤ 5 A |

> **Rule of thumb:** Use the IPC-2221 trace-width calculator at 10 °C temperature rise,
> external conductor, 1 oz copper. Values above include a 25 % safety margin.

---

## Via Constraints

| Parameter | Value |
|-----------|-------|
| Min via drill | 0.30 mm |
| Min via annular ring | 0.15 mm (pad 0.60 mm) |
| Preferred signal via | drill 0.40 mm / pad 0.80 mm |
| Preferred power via | drill 0.60 mm / pad 1.20 mm |
| Via-in-pad | Not allowed (HASL fill issue) |
| Blind / buried vias | Not used |

---

## Drill Sizes

| Feature | Drill size | Pad size | Tolerance |
|---------|-----------|----------|-----------|
| Signal via | 0.40 mm | 0.80 mm | ±0.05 mm |
| Power via | 0.60 mm | 1.20 mm | ±0.05 mm |
| M3 mounting hole (MH1–MH4) | 3.20 mm | 6.00 mm (non-plated) | ±0.10 mm |
| Terminal block TB1, TB2 (THT) | 1.40 mm | 3.00 mm (plated) | ±0.05 mm |
| Pin header J1 (2.54 mm) | 1.10 mm | 1.80 mm (plated) | ±0.05 mm |
| JST-PH 2.00 mm header | 0.80 mm | 1.60 mm (plated) | ±0.05 mm |

---

## Ground Plane

- **B.Cu** is a full ground plane (copper pour, `GND` net, thermal reliefs on THT pads).
- Thermal relief: 4 spokes, 0.40 mm spoke width, 0.30 mm clearance.
- **F.Cu** has no poured plane; route signal traces individually.
- Split planes are **not** required — single ground plane acceptable for this board's
  frequency range (I²C max 400 kHz, 1-Wire max 15.4 kbps).

---

## Impedance

No controlled-impedance traces are required on this board. I²C and 1-Wire run at
frequencies well below the threshold where impedance matching is needed for this
trace length (< 150 mm).

---

## KiCad DRU File Template

Save as `aku-edge-hub-sensor-board.kicad_dru` in the project directory:

```
(version 1)
(rule "Signal clearance"
  (constraint clearance (min 0.2mm))
  (condition "A.NetClass == 'Default' && B.NetClass == 'Default'"))

(rule "24V clearance"
  (constraint clearance (min 1.0mm))
  (condition "A.NetClass == 'Power24V' || B.NetClass == 'Power24V'"))

(rule "Signal trace width"
  (constraint track_width (min 0.2mm) (opt 0.3mm))
  (condition "A.NetClass == 'Default'"))

(rule "Power trace width"
  (constraint track_width (min 2.5mm) (opt 3.0mm))
  (condition "A.NetClass == 'Power24V'"))

(rule "Mounting hole no copper"
  (constraint hole_clearance (min 0.5mm))
  (condition "A.Reference == 'MH*'"))

(rule "Edge clearance"
  (constraint edge_clearance (min 0.3mm)))
```

Assign net classes in KiCad Board Setup → Net Classes:
- `Power24V`: `+24V_IN`, `SHUNT_CH1_P`, `SHUNT_CH1_N`, `SHUNT_CH2_P`, `SHUNT_CH2_N`,
  `SHUNT_CH3_P`, `SHUNT_CH3_N`
- All other nets: `Default`

---

## DRC Sign-off Criteria

Before generating Gerbers, the KiCad DRC must report:

- **0 errors**
- **0 unconnected items**
- **0 footprint errors**
- Allowed warnings: silkscreen overlap with pads (cosmetic only, fab will handle)

Run DRC: KiCad PCB Editor → Inspect → Design Rules Checker → Run DRC.
