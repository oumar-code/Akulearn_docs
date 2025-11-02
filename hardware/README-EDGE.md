# Aku Edge Hub - Getting Started

This document explains the immediate steps to begin Edge Hub hardware design and prototyping.

1. Review `hardware/edge/requirements.md` and `component-selection.md`.
2. Pick the compute SKU for the alpha prototype (recommendation: Jetson Orin Nano 16GB).
3. Start a KiCad project under `hardware/edge/kicad/` and create a PMU (power) schematic.
4. Build a small test harness using a Jetson dev kit, a LoRa dev module, and the DaaS/IG-Hub software stack for integration testing.
5. Document test results and iterate on the PMU and thermal design before PCB layout.
