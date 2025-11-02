# KiCad project scaffold - Edge Hub (alpha)

This folder is a scaffold for the Edge Hub KiCad project. It contains a short checklist and a placeholder for the KiCad project files.

What's included
- `PLACEHOLDER_NOTE.txt` — notes about starting the KiCad project and naming conventions.
- Guidance below for converting the block diagrams into an initial KiCad schematic.

Checklist to start the KiCad schematic
1. Install KiCad 7.x (or 6.x if preferred) on your workstation.
2. Create a new project named `edge-alpha` under this folder (`edge-alpha.kicad_pro`).
3. Use the block diagrams in `../diagrams/` as your top-level functional schematic pages.
4. Start with the PMU schematic: create a `pmu.sch` sheet with the MPPT, battery, BMS, and DC-DC blocks.
5. Add a `compute_carrier.sch` sheet with the compute module footprint, power pins, and key peripherals (JTAG, UART, USB, Ethernet).
6. Keep the initial schematic at block-level for the alpha; leave board-level pin mapping to the first layout iteration.

Notes
- This repository intentionally stores only schematic sources and documentation; binary or large KiCad files are avoided here. Commit your KiCad project files to a branch dedicated to hardware work (example: `hw/edge/alpha-pcb`).
- When the schematic is ready, export the netlist and PCB footprint list for layout.
