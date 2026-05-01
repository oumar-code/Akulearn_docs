# Aku Edge Hub — PCB Design Files

**Status:** ⏳ In progress — KiCad schematic and PCB layout pending fabrication sign-off

---

## Quick Start (KiCad 7)

1. Install [KiCad 7](https://www.kicad.org/download/) (7.0.x or later).
2. Open `aku-edge-hub-sensor-board.kicad_pro` from this directory.
3. The schematic (`.kicad_sch`) and PCB layout (`.kicad_pcb`) open from the project manager.
4. Custom symbols and footprints are in `.kicad_sym` / `.kicad_fp` — KiCad loads them
   automatically from the project library paths (no global library changes needed).
5. Review [`schematic-notes.md`](schematic-notes.md) before editing the schematic —
   all net names and pin assignments are defined there.
6. Review [`design-rules.md`](design-rules.md) before touching the PCB layout.
7. Import `aku-edge-hub-sensor-board.kicad_dru` in Board Setup → Design Rules to
   load the project-specific DRC rules.

---

## Design Documentation

| Document | Purpose |
|----------|---------|
| [`schematic-notes.md`](schematic-notes.md) | Full net-level schematic description — every pin, net name, and passive value |
| [`design-rules.md`](design-rules.md) | Layer stackup, trace widths, clearances, via sizes, DRU template |
| [`component-placement.md`](component-placement.md) | Board floorplan with X/Y coordinates and routing guidance |
| [`bom-pcb.csv`](bom-pcb.csv) | Machine-readable BOM (JLCPCB SMT assembly ready) |

---

## Overview

This directory will contain the **KiCad EDA files** for the Aku Edge Hub sensor and
power-distribution PCB. The PCB consolidates:

- INA3221 3-channel current/voltage monitor breakout (I²C to RPi header)
- DS18B20 1-Wire temperature sensor connectors (×2, JST-PH 3-pin)
- Status LED driver board (3 × LED, 330 Ω resistors, GPIO 22/23/24)
- Terminal block connectors for 24 V DC input and load outputs
- In-line fuse holder footprint (5 A automotive blade, polarity-marked)

---

## Planned Files

| File | Description |
|------|-------------|
| `aku-edge-hub-sensor-board.kicad_pro` | KiCad 7 project file |
| `aku-edge-hub-sensor-board.kicad_sch` | Schematic — INA3221, DS18B20, LEDs, fuse |
| `aku-edge-hub-sensor-board.kicad_pcb` | PCB layout — 100×60 mm, 2-layer FR4 |
| `aku-edge-hub-sensor-board.kicad_sym` | Custom symbol library (INA3221, DS18B20) |
| `aku-edge-hub-sensor-board.kicad_fp`  | Custom footprint library (terminal blocks) |
| `gerbers/`                             | Gerber RS-274X files + drill file for fab |
| `bom-pcb.csv`                          | PCB-level BOM (pick-and-place ready) |

---

## Schematic Notes

### INA3221 Circuit

```
RPi GPIO 2 (SDA) ──4.7kΩ──┐
RPi GPIO 3 (SCL) ──4.7kΩ──┤── 3.3 V
                           │
               INA3221 (U2 — Adafruit 4162 footprint)
               SDA ←── GPIO 2
               SCL ←── GPIO 3
               VCC ──── 3.3 V (RPi pin 1)
               GND ──── GND  (RPi pin 6)
               A0  ──── GND  (I²C addr 0x40)
               A1  ──── GND
               IN1+/IN1- ── CH1 solar shunt (0.1 Ω, 3 W, series in 24 V+ solar line)
               IN2+/IN2- ── CH2 wind shunt  (0.1 Ω, 3 W, series in 24 V+ wind line)
               IN3+/IN3- ── CH3 load shunt  (0.1 Ω, 3 W, series in 24 V+ load bus)
```

### Power Input Section

```
24 V DC input (KO1 cable gland)
       │
   [5 A automotive blade fuse]
       │
   TB1 (5-pole DIN terminal block)
       ├── TB1-1 (+24 V) → U7 buck in+, U8 buck in+, INA3221 CH3 IN3+
       └── TB1-GND (0 V) → U7 buck in−, U8 buck in−, INA3221 CH3 IN3−
```

---

## PCB Layout Guidelines

- **Board size:** 100 mm × 60 mm (fits inside the 300×200×120 mm enclosure on M3 standoffs)
- **Layers:** 2-layer FR4, 1.6 mm, HASL surface finish
- **Trace width:** ≥ 0.3 mm signal, ≥ 2.5 mm power (24 V bus at 5 A)
- **Clearance:** ≥ 0.2 mm signal, ≥ 1.0 mm 24 V to logic
- **Mounting holes:** 4 × M3 (2.5 mm pad), positioned for enclosure DIN-rail standoffs

---

## Fabrication

Once design files are complete, fabricate using:

- **Prototype:** [JLCPCB](https://jlcpcb.com) or [PCBWay](https://www.pcbway.com)
  — 5 boards, 2-layer, green, HASL, lead-free, standard (5–7 day)
- **Production:** Local Nigerian PCB fab (Kano / Lagos electronics market) or
  JLCPCB SMT assembly service for INA3221 placement

---

## ERC / DRC Pass Criteria

Before generating Gerbers the following must all be green:

| Check | Tool | Acceptance |
|-------|------|-----------|
| Electrical Rules Check (ERC) | KiCad Schematic Editor → Inspect → ERC | 0 errors |
| Design Rule Check (DRC) | KiCad PCB Editor → Inspect → DRC | 0 errors, 0 unconnected |
| Gerber visual check | KiCad Gerber Viewer or gerbv | All copper, mask, silk look correct |
| Drill file check | KiCad Gerber Viewer | All holes present, no missing pads |

---

## Fab Submission Checklist (JLCPCB)

- [ ] Export Gerbers: `File → Plot` → Gerber, all layers checked, use Protel extensions
- [ ] Export drill file: `File → Plot → Generate Drill Files` — Excellon format, metric
- [ ] Zip all files: `gerbers/` folder → `aku-edge-hub-sensor-board-gerbers.zip`
- [ ] Upload to JLCPCB order page; verify board outline in online viewer
- [ ] Set: 2 layers, 1.6 mm, green, HASL lead-free, 5 pcs (prototype)
- [ ] If SMT: upload `bom-pcb.csv` and pick-and-place CSV from KiCad fabrication output
- [ ] Confirm SMT parts: U2 (INA3221), C1, R1–R9, D1 — all others hand-soldered

---

## Status

- [x] Schematic notes documented ([schematic-notes.md](schematic-notes.md))
- [x] Design rules documented ([design-rules.md](design-rules.md))
- [x] Component placement guide documented ([component-placement.md](component-placement.md))
- [x] Pick-and-place BOM created ([bom-pcb.csv](bom-pcb.csv))
- [ ] KiCad schematic complete
- [ ] PCB layout complete
- [ ] Design Rule Check (DRC) passed — 0 errors
- [ ] Gerbers generated and verified in Gerber viewer
- [ ] Prototype batch ordered (5 boards)
- [ ] Prototype assembled and bench-tested
- [ ] Production BOM updated with PCB line item

---

## Related

- [Wiring guide](../wiring.md) — all connector and pin assignments sourced from this schematic
- [BOM](../bom.md) — PCB board added as a line item in the production BOM
- [Energy monitoring](../../power-system/energy-monitoring.md) — INA3221 metrics spec
- [Design status tracker](../DESIGN_STATUS.md) — overall PCB + mechanical milestone gates
