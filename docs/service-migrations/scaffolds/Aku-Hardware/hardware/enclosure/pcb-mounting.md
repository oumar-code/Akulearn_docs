# Aku Edge Hub — PCB-to-Enclosure Interface

**Drawing ref:** AKU-EH-ENC-002  
**Revision:** A

This document defines how the PCB mounts inside the enclosure and verifies that all
components fit without collision. Use this alongside the STEP assembly file for
pre-fabrication clearance checks.

---

## Mounting Configuration

The PCB is mounted on four M3 × 15 mm hex standoffs screwed to the enclosure base plate.

| Parameter | Value |
|-----------|-------|
| Standoff type | M3 hex brass, female–female |
| Standoff height | 15 mm (base plate to PCB underside) |
| PCB fastener | M3 × 6 mm machine screw (4 off) |
| Base plate fastener | M3 × 5 mm self-tapping screw into base (4 off) |
| PCB size | 100 mm × 60 mm |
| Max component height (F.Cu side) | 15 mm above PCB surface |

---

## Standoff Positions

Standoff positions use the same coordinate system as the PCB: origin at bottom-left
corner of board outline.

| Standoff | PCB hole (Ref) | PCB X (mm) | PCB Y (mm) | Enclosure base X (mm) | Enclosure base Y (mm) |
|----------|----------------|-----------|-----------|----------------------|----------------------|
| S1 | MH1 | 5 | 5 | 40 | 20 |
| S2 | MH2 | 95 | 5 | 130 | 20 |
| S3 | MH3 | 5 | 55 | 40 | 70 |
| S4 | MH4 | 95 | 55 | 130 | 70 |

> **Enclosure base coordinates** are measured from the bottom-left corner of the
> enclosure base (inner surface), with X = width direction, Y = depth direction.

---

## 2D Top View — Enclosure Interior

All dimensions in mm. View from above (lid removed). Origin = bottom-left inner corner.

```
 Enclosure inner width: 297 mm
 ┌────────────────────────────────────────────────────────────────┐
 │                                         Inner depth: 117mm     │
 │   ●─────────────────────────────────────────────●             │
 │   S3(40,70)                              S4(130,70)            │
 │   │  ┌──────────────────────────────┐    │                     │
 │   │  │    PCB  100 mm × 60 mm       │    │                     │
 │   │  │                              │    │                     │
 │   │  │  [U2]  [R4][R5][R6]          │    │    [DIN rail]       │
 │   │  │  [J1 RPi header]             │    │    [TB1][TB2]       │
 │   │  │                              │    │    [U7 buck]        │
 │   │  │  [LED1][LED2][LED3]──────────┼────┼──► to lid holes     │
 │   │  └──────────────────────────────┘    │                     │
 │   S1(40,20)                              S2(130,20)            │
 │   ●─────────────────────────────────────────────●             │
 │                                                                │
 │  KO1  KO2  KO3  KO4  ← cable glands on bottom face           │
 └────────────────────────────────────────────────────────────────┘
      Rear face (wall-mount keyholes)                  Front face
```

---

## Component Clearance Check

For each component on the PCB, verify clearance to nearest enclosure wall.

| Component | PCB Position | Enclosure wall | Gap (mm) | Min required | Pass? |
|-----------|-------------|----------------|----------|--------------|-------|
| J1 pin header (left) | X=10 from PCB left | Left inner wall (PCB left edge at X=40 encl.) | 40 − 10 = 30 | 5 mm | ✅ |
| TB1 (left edge) | X=8 from PCB left | Left inner wall | 40 − 8 = 32 | 10 mm (cable clearance) | ✅ |
| R4/R5/R6 shunts (top) | Y=50 from PCB bottom | Rear wall (PCB top at Y=70+60=130) | 117−130+117 → check STEP | 5 mm | ⚠️ verify in STEP |
| LED1 (right) | X=88 from PCB left | Right inner wall (PCB right at 130+100=230, encl. inner=297) | 297−230=67 | 5 mm | ✅ |
| Terminal block TB1 height | 8.5 mm above PCB | Lid underside (117−15−8.5=93.5 mm clear) | 93 mm | 10 mm | ✅ |
| INA3221 WQFN-16 height | < 1 mm above PCB | Lid clearance | >> 10 mm | 2 mm | ✅ |
| Fuse holder F1 height | ~12 mm above PCB | Lid clearance (117−15−12=90 mm clear) | 90 mm | 10 mm | ✅ |

> ⚠️ Rows marked "verify in STEP" must be confirmed using `enclosure-assembly.step`
> once the FreeCAD model is complete.

---

## DIN Rail Zone (adjacent to PCB)

The DIN rail and power converters (U7, U8) sit beside the PCB on the enclosure base.

| Item | Enclosure base X (mm) | Enclosure base Y (mm) | Notes |
|------|----------------------|----------------------|-------|
| DIN rail start | 145 | 10 | 260 mm long, runs toward X=260+145=405 → trim to 297-145=152 mm |
| U7 (24→5V buck) | 150 | 15 | Snap-on DIN bracket |
| U8 (24→12V buck) | 180 | 15 | Snap-on DIN bracket |
| TB1 power terminal | 210 | 12 | DIN mounted |

Minimum clearance between PCB right edge (at X=130+100=230 mm) and DIN rail (at X=145):
230 − 145 = **85 mm** — adequate for wiring.

---

## LED Alignment to Lid Holes

The PCB LED positions must align with the lid holes within ±1 mm.

| LED | PCB board X (mm) | PCB board Y (mm) | Enclosure base X | Enclosure base Y | Lid hole X | Lid hole Y | Δ |
|-----|-----------------|-----------------|-----------------|-----------------|-----------|-----------|---|
| LED1 | 88 | 46 | 40+88=128 | 20+46=66 | 130 | — | 2 mm — adjust standoff S2 X by +2 mm or shift PCB |
| LED2 | 93 | 46 | 40+93=133 | 20+46=66 | 150 | — | 17 mm gap — **LED2 requires a flexible lead-out or PCB position adjustment** |
| LED3 | 88 | 53 | 128 | 73 | 170 | — | see note |

> 📌 **Action required:** The LED positions in the current PCB placement produce an
> X-offset from the lid hole positions (defined in `mechanical-drawing.md`). Resolution
> options:
> 1. Use short flexible wire extensions from PCB LED pads to through-lid LED holders
>    (recommended — allows lid to open freely).
> 2. Adjust PCB `component-placement.md` LED positions to match lid holes exactly,
>    then re-check routing clearances.
>
> **Recommended:** Option 1 (flex leads). Update `assembly.md` to reflect LED wiring
> extension step.

---

## Wiring Clearance

Cables from TB1/TB2 route from the DIN zone toward J1 on the PCB. Maintain:

- Minimum bend radius: 5 × cable diameter.
- All cables must be tie-wrapped to DIN rail or base plate — no free-hanging cables.
- I²C and 1-Wire cables must be separated from 24 V power cables by ≥ 10 mm or
  enclosed in separate cable conduit.

---

## Related

- [`mechanical-drawing.md`](mechanical-drawing.md) — enclosure dimensions and hole table
- [`freecad-setup.md`](freecad-setup.md) — how to build and validate in FreeCAD
- [`../edge-hub/pcb/component-placement.md`](../edge-hub/pcb/component-placement.md) — PCB component coordinates
- [`../edge-hub/assembly.md`](../edge-hub/assembly.md) — assembly procedure references standoff positions
