# FreeCAD 0.21 — Enclosure Modeling Guide

**Target file:** `enclosure-body.FCStd`  
**FreeCAD version:** 0.21.x (stable)  
**Export targets:** DXF R12 (flat patterns), STEP AP214 (assembly)

This guide walks a mechanical engineer through building the parametric sheet-metal
enclosure model from scratch in FreeCAD 0.21. Follow the steps in order; do not
skip the parametric sketch step or dimensions will be hard-coded and difficult to
update.

---

## Prerequisites

### Required Workbenches

FreeCAD 0.21 ships with these workbenches — enable them in View → Workbenches:

| Workbench | Use |
|-----------|-----|
| **Part Design** | Create the 3D solid body |
| **Sheet Metal** | Unfold the body into a flat pattern for DXF export |
| **Sketcher** | Define 2D profiles and hole patterns |
| **TechDraw** | (Optional) Generate 2D drawing sheet for the fabrication drawing |

Install the Sheet Metal workbench via `Tools → Addon Manager → SheetMetal` if not
already present.

---

## Step 1 — Create a New FreeCAD Document

1. `File → New`
2. `File → Save As` → name it `enclosure-body.FCStd` in this directory.
3. In the Model tree, right-click → `Create body` → name it `EnclosureBody`.

---

## Step 2 — Define Global Parameters (Spreadsheet)

Using a Spreadsheet to hold all dimensions makes the model fully parametric.

1. Go to **Spreadsheet workbench** (View → Workbenches → Spreadsheet).
2. `Spreadsheet → Create spreadsheet` → name it `Params`.
3. Enter the following cells:

| Cell | Name (Alias) | Value | Unit |
|------|-------------|-------|------|
| A1 | `W` | 300 | mm — enclosure width |
| A2 | `H` | 200 | mm — enclosure height |
| A3 | `D` | 120 | mm — enclosure depth |
| A4 | `T` | 1.5 | mm — wall thickness |
| A5 | `R_ext` | 3 | mm — external corner radius |
| A6 | `KO1_X` | 50 | mm — KO1 X position |
| A7 | `KO2_X` | 120 | mm |
| A8 | `KO3_X` | 190 | mm |
| A9 | `KO4_X` | 250 | mm |
| A10 | `KO_Y` | 60 | mm — all KO Y (depth centre) |

To set an alias: right-click a cell → Properties → set Alias to the name in the
table above (no spaces).

Reference cells in sketches with `Spreadsheet.W`, `Spreadsheet.T`, etc.

---

## Step 3 — Model the Enclosure Body (Part Design)

### 3a. Base sketch (body footprint)

1. Switch to **Part Design** workbench.
2. Select the `EnclosureBody`, click `New Sketch` on the XY plane.
3. Draw a rectangle: width = `Spreadsheet.W`, height = `Spreadsheet.D`.
4. Apply fillet at all four corners: radius = `Spreadsheet.R_ext`.
5. Close sketch.
6. **Pad** (extrude) the sketch: length = `Spreadsheet.H`.
7. Rename the feature `Body_Solid`.

### 3b. Shell the body (hollow it out)

1. Select the top face of `Body_Solid`.
2. **Part Design → Thickness** (shell): thickness = `Spreadsheet.T`, select the top
   face as the face to remove (this becomes the lid opening).
3. Rename the feature `Body_Shell`.

### 3c. Cut cable gland knockouts (bottom face)

For each knockout KO1–KO4:

1. Select the bottom face → `New Sketch`.
2. Draw a circle at the KO position (use `Spreadsheet.KO1_X`, `Spreadsheet.KO_Y`).
3. Set diameter per the hole summary in [`mechanical-drawing.md`](mechanical-drawing.md).
4. Close sketch → **Pocket** (cut through) the circle.
5. Repeat for KO2, KO3, KO4.

### 3d. Cut lid screw holes (top rim)

1. Select the top rim face → `New Sketch`.
2. Draw four circles at the M4 screw positions (10,10), (290,10), (10,190), (290,190).
3. Diameter: 4.5 mm.
4. Pocket (cut through wall thickness).

### 3e. Cut wall-mount keyholes (rear face)

1. Select the rear face → `New Sketch`.
2. At (60, 100) draw: a circle Ø8 mm (head) and below it a rectangle 5.5 mm wide × 12 mm
   tall (slot). Use the Part Design `Pocket` → cut through.
3. Repeat at (240, 100).

---

## Step 4 — Model the Lid (separate body)

1. Right-click in Model tree → `Create body` → name it `LidBody`.
2. Sketch on XY plane: rectangle = `Spreadsheet.W` × `Spreadsheet.D`, same corner radius.
3. Pad to `Spreadsheet.T` (1.5 mm).
4. Cut LED holes (×3, Ø5 mm) and PIR aperture (Ø8 mm) — positions per
   [`mechanical-drawing.md`](mechanical-drawing.md) §2.
5. Add a 10 mm × 1 mm lip sketch on the underside perimeter — pad 10 mm inward to
   create the lid-to-body seal channel.

---

## Step 5 — Unfold with Sheet Metal Workbench

> The Sheet Metal workbench works best when the model is built as bent sheet
> rather than a shelled solid. For DXF export from a shelled solid, use the
> approach below.

1. Switch to **Sheet Metal** workbench.
2. Select the `Body_Shell` → `Sheet Metal → Add base flange` — this converts the
   solid to a sheet-metal object FreeCAD can unfold.
3. Set material thickness = 1.5 mm (should match Pad thickness).
4. `Sheet Metal → Unfold` → accept defaults.
5. A flat "Unfold" object appears in the tree. Select it.

### Export DXF flat pattern

1. Select the `Unfold` object → `File → Export` → choose format **DXF R12**.
2. Save as `enclosure-body.dxf`.
3. Repeat for lid: `enclosure-lid.dxf`.

---

## Step 6 — Create Drill Template DXF

The drill template is a 2D drawing of just the hole positions — no outline needed.

1. Switch to **TechDraw** workbench.
2. `TechDraw → Insert Page (use template)` → choose A3 landscape.
3. `TechDraw → Insert View` → select top face of `Body_Shell`.
4. Add all hole centre marks using `TechDraw → Insert Annotation`.
5. Export: `File → Export` → DXF → save as `enclosure-drill-template.dxf`.

---

## Step 7 — Export STEP Assembly

1. In the Model tree, select both `EnclosureBody` and `LidBody`.
2. `File → Export` → choose **STEP AP214**.
3. Save as `enclosure-assembly.step`.
4. Open in a STEP viewer (FreeCAD itself, or FreeCAD's built-in viewer) and check
   clearances against the PCB placement in [`pcb-mounting.md`](pcb-mounting.md).

---

## Step 8 — Validation Checklist

- [ ] `Spreadsheet.W/H/D` = 300/200/120 mm (verify in spreadsheet)
- [ ] Wall thickness on all faces = 1.5 mm (measure with Part Design → Measure)
- [ ] All 4 KO knockouts present, correct diameter, correct X position
- [ ] Lid screw holes (×4) present, 4.5 mm Ø, correct corner positions
- [ ] Wall-mount keyholes (×2) present, rear face
- [ ] LED holes (×3, 5 mm) and PIR aperture (8 mm) in lid
- [ ] Flat patterns exported to DXF, opened in LibreCAD / QCad — outline is continuous
- [ ] STEP assembly opens in FreeCAD without errors
- [ ] PCB (100×60 mm) fits inside with clearance ≥ 5 mm on all sides (check in STEP)

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Sheet Metal → Unfold fails | Rebuild model using Sheet Metal Bend workbench from scratch (preferred for unfoldable geometry) |
| DXF export shows curved lines as polylines | In Export dialog, set arc resolution to 1° for clean arcs |
| STEP file too large | Suppress the insect mesh louvre detail before STEP export |
| Spreadsheet alias not found | Aliases are case-sensitive; check exact spelling in the sketch constraint formula |
