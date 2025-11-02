# Hardware PR / QA Checklist

This checklist should be used by authors and reviewers for any hardware-related pull request.

Pre-merge checks (author)
- [ ] BOM CSV updated with any new parts and alternates
- [ ] Supplier/lead-time notes added to RFQ spreadsheet
- [ ] KiCad schematic sheets committed or schematic templates updated
- [ ] ERC and DRC run locally and major warnings addressed
- [ ] Test points and debug headers present and documented
- [ ] Thermal and power estimates documented (expected idle/peak wattage)

Review checks (reviewer)
- [ ] Verify BOM lines for correctness and alternates
- [ ] Confirm footprints and suggested footprints are appropriate
- [ ] Check that RF sections have notes about antenna matching and test plan
- [ ] Ensure procurement notes include at least two suppliers for long-lead items
- [ ] Confirm QA/test plan is adequate for initial bench/alpha prototype

Post-merge / Release checks
- [ ] Netlist exported and linked to PCB layout branch
- [ ] BOM locked for prototype order and vendor quotes collected
- [ ] Test fixture plan created (bench setup, power meter hookup, RF test distances)

Notes
- For RF module/antenna changes, include an RF test plan and indicate if external tuning will be required (SMA/antenna connector vs integrated PCB antenna).
- For battery changes, require datasheets and UN38.3 compliance docs from supplier prior to assembly.
