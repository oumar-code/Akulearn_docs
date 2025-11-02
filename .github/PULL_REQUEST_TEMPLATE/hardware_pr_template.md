<!--
  Hardware PR template
  Use this template for any PR that modifies hardware designs, BOMs, schematics, or procurement artifacts.
-->

# Summary
Provide a short summary of the hardware change and purpose.

Related Issue: # (if applicable)

## What changed
- List files added/modified (schematics, BOMs, KiCad project files, diagrams).

## Motivation
- Why is this change needed? (bugfix, prototype iteration, component substitution)

## Checklist (required)
- [ ] PR includes updated BOM (CSV) or a note explaining why BOM not changed
- [ ] Schematic files updated (or `pmu_schematic_template.kicad_sch` updated) and ERC run locally
- [ ] Diagrams updated and `.mmd` sources included where relevant
- [ ] Test points and debug headers noted in schematic
- [ ] Procurement impact assessed (lead times, alternates) and RFQ updated
- [ ] Reviewer: hardware engineer assigned

## QA / Validation Plan
- How will this change be validated (bench tests, power-up checks, thermal runs)? Include steps and pass criteria.

## Risks and Mitigations
- List known risks and mitigations (e.g., part lead time, thermal concerns, RF matching needs)

## Attachments
- Attach PDFs or rendered diagrams if available. Prefer linking CI-generated SVG/PNG assets.
