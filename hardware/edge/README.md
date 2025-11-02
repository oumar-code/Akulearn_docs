# Edge Hub Hardware Overview (Edge Alpha)

This document is the hub for Edge alpha artifacts: block diagrams, PMU guidance, BOMs, and procurement notes.

Artifacts in this folder:
- `diagrams/` — Mermaid sources for block diagrams (edge_system_block.mmd, pmu_block.mmd, network_block.mmd). The repo CI renders these to SVG/PNG.
- `pmu/pmu_schematic_guidance.md` — step-by-step KiCad-friendly guidance to implement `pmu.sch`.
- `kicad/` — KiCad scaffold and placeholders; create your `edge-alpha.kicad_pro` project here locally.
- `procurement/README.md` — procurement & supplier outreach guidance referencing `hardware/boms/edge_alpha_bom.csv`.

Rendered diagrams (CI)
- After pushing `.mmd` files, the render workflow in `.github/workflows/render-mermaid.yml` will create SVG/PNG assets under the docs output folder; check the generated PR for images to include in docs.

Quick start
1. Review `pmu/pmu_schematic_guidance.md` and the block diagrams in `diagrams/`.
2. Start a KiCad project (`edge-alpha`) in `kicad/` and create `pmu.sch` and `compute_carrier.sch` sheets.
3. Use `hardware/boms/edge_alpha_bom.csv` to order a Jetson dev kit, LoRa dev module, sensors and a battery for bench testing.

Contact
- Add procurement updates and supplier quotes as comments in the BOM CSV or create a PR with updated pricing and lead times.
