# Aku Edge Hub — Hardware Design Status Tracker

**Last updated:** 2025-Q2  
**Revision:** A

This is the single-page readiness tracker for PCB and mechanical design milestones.
Update this file as each gate is passed. Link to evidence (files, test reports, orders)
where possible.

---

## PCB Design Milestones

| # | Gate | Status | Owner | Evidence / Notes |
|---|------|--------|-------|-----------------|
| P1 | Schematic notes documented | ✅ Done | — | [pcb/schematic-notes.md](pcb/schematic-notes.md) |
| P2 | Design rules documented | ✅ Done | — | [pcb/design-rules.md](pcb/design-rules.md) |
| P3 | Component placement guide | ✅ Done | — | [pcb/component-placement.md](pcb/component-placement.md) |
| P4 | Pick-and-place BOM | ✅ Done | — | [pcb/bom-pcb.csv](pcb/bom-pcb.csv) |
| P5 | KiCad schematic complete | ⏳ Pending | EDA engineer | `pcb/aku-edge-hub-sensor-board.kicad_sch` |
| P6 | ERC passed (0 errors) | ⏳ Pending | EDA engineer | KiCad ERC report |
| P7 | PCB layout complete | ⏳ Pending | EDA engineer | `pcb/aku-edge-hub-sensor-board.kicad_pcb` |
| P8 | DRC passed (0 errors, 0 unconnected) | ⏳ Pending | EDA engineer | KiCad DRC report |
| P9 | Gerbers generated and verified | ⏳ Pending | EDA engineer | `pcb/gerbers/` + Gerber viewer screenshot |
| P10 | Prototype order placed (5 boards) | ⏳ Pending | Hardware lead | JLCPCB order confirmation |
| P11 | Prototype received and assembled | ⏳ Pending | Tech | Build log in `pcb/build-log.md` |
| P12 | Bench test passed (I²C, 1-Wire, LEDs) | ⏳ Pending | Tech | Test report |
| P13 | Production BOM updated with PCB line item | ⏳ Pending | Hardware lead | [bom.md](bom.md) |

---

## Mechanical Design Milestones

| # | Gate | Status | Owner | Evidence / Notes |
|---|------|--------|-------|-----------------|
| M1 | Enclosure specification defined | ✅ Done | — | [../enclosure/README.md](../enclosure/README.md) |
| M2 | Internal layout and cable gland positions defined | ✅ Done | — | [../enclosure/README.md](../enclosure/README.md) |
| M3 | Fabrication drawing documented | ✅ Done | — | [../enclosure/mechanical-drawing.md](../enclosure/mechanical-drawing.md) |
| M4 | FreeCAD modeling guide written | ✅ Done | — | [../enclosure/freecad-setup.md](../enclosure/freecad-setup.md) |
| M5 | PCB-to-enclosure interface defined | ✅ Done | — | [../enclosure/pcb-mounting.md](../enclosure/pcb-mounting.md) |
| M6 | FreeCAD model (`enclosure-body.FCStd`) created | ⏳ Pending | Mech. engineer | `../enclosure/enclosure-body.FCStd` |
| M7 | DXF flat patterns exported and verified | ⏳ Pending | Mech. engineer | `../enclosure/enclosure-body.dxf`, `enclosure-lid.dxf` |
| M8 | STEP assembly clearance check passed | ⏳ Pending | Mech. engineer | `../enclosure/enclosure-assembly.step` + screenshot |
| M9 | Prototype enclosure fabricated | ⏳ Pending | Hardware lead | Sheet-metal shop invoice / photo |
| M10 | PCB fits in enclosure (dry-fit test) | ⏳ Pending | Tech | Photo, any rework noted |
| M11 | IP54 rating validated (water-spray test) | ⏳ Pending | Tech | Test report per IEC 60529 §14.2.5 |
| M12 | Asset tag / QR code slot added to lid | ⏳ Pending | Mech. engineer | FreeCAD update + fab re-order |

---

## Integration Milestones

| # | Gate | Status | Owner | Evidence / Notes |
|---|------|--------|-------|-----------------|
| I1 | PCB assembled and installed in enclosure | ⏳ Pending | Tech | Assembly log |
| I2 | Full wiring complete (per wiring.md) | ⏳ Pending | Tech | Wiring checklist signed off |
| I3 | Firmware boot and sensor readings verified | ⏳ Pending | SW engineer | `/metrics` endpoint screenshot |
| I4 | Enclosure sealed and IP54 re-tested with PCB inside | ⏳ Pending | Tech | Test report |
| I5 | Unit shipped to Zamfara pilot site | ⏳ Pending | Hardware lead | Shipping confirmation |

---

## Definition of Done (Hardware Rev A)

A hardware unit is considered **pilot-ready** when all of the following are true:

- [ ] PCB gates P1–P12 complete
- [ ] Mechanical gates M1–M11 complete
- [ ] Integration gates I1–I5 complete
- [ ] Serial number applied (`AEH-YYYYMM-NNN` format)
- [ ] Field repair guide reviewed and up to date

---

## Key Documents

| Document | Path |
|----------|------|
| PCB schematic notes | [pcb/schematic-notes.md](pcb/schematic-notes.md) |
| PCB design rules | [pcb/design-rules.md](pcb/design-rules.md) |
| PCB component placement | [pcb/component-placement.md](pcb/component-placement.md) |
| PCB BOM (pick-and-place) | [pcb/bom-pcb.csv](pcb/bom-pcb.csv) |
| PCB README | [pcb/README.md](pcb/README.md) |
| Enclosure fabrication drawing | [../enclosure/mechanical-drawing.md](../enclosure/mechanical-drawing.md) |
| FreeCAD modeling guide | [../enclosure/freecad-setup.md](../enclosure/freecad-setup.md) |
| PCB mounting interface | [../enclosure/pcb-mounting.md](../enclosure/pcb-mounting.md) |
| Enclosure README | [../enclosure/README.md](../enclosure/README.md) |
| Edge Hub BOM | [bom.md](bom.md) |
| Wiring guide | [wiring.md](wiring.md) |
| Assembly procedure | [assembly.md](assembly.md) |
| Hardware specs | [specs.md](specs.md) |
