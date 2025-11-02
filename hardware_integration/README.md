# hardware_integration/

Purpose
-------
This folder contains integration-level code, scripts, and documentation for connecting Aku Platform hardware to higher-level services (for example, drivers, integration tests, and example code used by the `hardware/` designs).

When to use this folder
-----------------------
- If you are integrating a device's firmware or device-side software with cloud APIs or the IG‑Hub control panel, put example scripts and integration tests here.
- If you are creating driver wrappers or reference firmware that are not board-level EDA files, this is a good place.

Why it's separate from `hardware/`
---------------------------------
`hardware/` focuses on mechanical/electrical design artifacts: schematics, PCB layouts, BOMs, enclosure CAD, and procurement materials. `hardware_integration/` focuses on software/firmware integration, sample clients, and test rigs.

Consolidation note
------------------
There is intentional separation, but if your change spans both hardware and integration code (for example, adding a new connector pinout and the corresponding driver), create a PR that touches both folders and reference this README and the `hardware/` README. If you'd prefer consolidation, propose a migration plan in an issue and we can merge the two areas into one top-level `hardware/` area with `design/` and `integration/` subfolders.
