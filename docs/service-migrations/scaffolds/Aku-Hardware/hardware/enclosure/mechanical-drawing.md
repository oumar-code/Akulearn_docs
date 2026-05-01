# Aku Edge Hub — Fabrication Drawing

**Drawing number:** AKU-EH-ENC-001  
**Revision:** A  
**Material:** DC01 cold-rolled mild steel (CRCA) 1.5 mm, powder-coat RAL 7035 light grey  
**Scale:** Not to scale — all dimensions in millimetres  
**Tolerance (unless stated):** Linear ±0.5 mm, angular ±1°, holes ±0.2 mm

This document is the fabrication reference for the custom sheet-metal enclosure.
Hand this to the sheet-metal shop together with the DXF files when available.
Until DXF files are ready, this drawing is the sole dimensional reference.

---

## 1. Overall Dimensions

```
                 300 mm (Width)
    ┌────────────────────────────────────────────┐  ─┐
    │                                            │   │
    │                                            │   │ 200 mm
    │                                            │   │ (Height)
    │                                            │   │
    └────────────────────────────────────────────┘  ─┘
    │◄──────────────── 300 mm ──────────────────►│
    Depth (front-to-back): 120 mm
    Wall thickness: 1.5 mm (all faces)
```

| Dimension | Value |
|-----------|-------|
| Width (W) | 300 mm |
| Height (H) | 200 mm |
| Depth (D) | 120 mm |
| Wall thickness | 1.5 mm |
| Corner radii (external) | R3 mm (all external corners) |

---

## 2. Front View (with lid fitted)

```
     0mm                  300mm
  Y  ┌──┬─────────────────────┬──┐
200  │●  │                     │  ●│  ← M4 captive screws (×4, quarter-turn)
     ├──┘                     └──┤
     │                           │
     │   (Lid face — blank)      │
     │                           │
     │  ○  ○  ○   ◉              │  ← 5 mm LED holes (×3) + 8 mm PIR aperture
     │  130 150 170  250         │    at Y=30 from bottom of lid
     │                           │  
     ├──┐                     ┌──┤
  0  │●  │                     │  ●│
     └──┴─────────────────────┴──┘
```

**Lid cutouts (positions on lid face, from bottom-left of lid):**

| Feature | X (mm) | Y (mm) | Diameter |
|---------|--------|--------|----------|
| LED1 (green — Power) | 130 | 30 | 5 mm |
| LED2 (blue — Wi-Fi) | 150 | 30 | 5 mm |
| LED3 (amber — Sync) | 170 | 30 | 5 mm |
| PIR aperture | 250 | 30 | 8 mm |

**Lid corner screws (M4 captive):**

| Position | X (mm) | Y (mm) |
|----------|--------|--------|
| Bottom-left | 10 | 10 |
| Bottom-right | 290 | 10 |
| Top-left | 10 | 190 |
| Top-right | 290 | 190 |

---

## 3. Rear View (wall-mount face)

```
     0mm                  300mm
  Y  ┌─────────────────────────────┐
200  │                             │
     │   ┌──────────────────────┐  │
     │   │  Ventilation louvres  │  │  (passive, with insect mesh)
     │   │  (top half of rear)   │  │
     │   └──────────────────────┘  │
100  │         ⊕           ⊕       │  ← M5 keyhole wall-mount slots
     │        60mm        240mm    │
     │                             │
  0  └─────────────────────────────┘
```

**Keyhole wall-mount slots:**

| Slot | Centre X (mm) | Centre Y (mm) | Head Ø | Slot width |
|------|--------------|--------------|--------|-----------|
| KH1 | 60 | 100 | 8 mm | 5.5 mm × 12 mm (slot upward) |
| KH2 | 240 | 100 | 8 mm | 5.5 mm × 12 mm (slot upward) |

**Louvres:**
- Pattern: 10 horizontal louvres, 20 mm wide × 2 mm pitch, across full width
- Position: rear face, Y = 100 mm to 190 mm
- Insect mesh: 1 mm mesh spot-welded behind louvres

---

## 4. Bottom View (cable gland face)

```
     0mm                  300mm
  D  ┌──────────────────────────────────────────┐
120  │                                          │
     │   ○        ○        ○        ○           │
     │  KO1      KO2      KO3      KO4          │
     │  50mm    120mm    190mm    250mm         │
  0  └──────────────────────────────────────────┘
```

**Cable gland knockouts (bottom face):**

| Knock-out | X (mm from left) | Thread | Cut Ø | Purpose |
|-----------|-----------------|--------|--------|---------|
| KO1 | 50 | PG16 | 22 mm | 24 V DC input (18 AWG 2-core) |
| KO2 | 120 | PG13.5 | 20 mm | HDMI cable (projector) |
| KO3 | 190 | PG11 | 16 mm | Cat5e Ethernet (uplink) |
| KO4 | 250 | PG11 | 16 mm | USB 3.0 (optional SSD) |

All knockouts centred at Y = 60 mm (mid-depth of bottom face).  
Tolerance on gland holes: ±0.3 mm.

---

## 5. Side View (left, showing depth)

```
 Front         Rear
    ┌────────────┐
    │            │  ← 1.5 mm walls
    │  120 mm D  │
    └────────────┘
```

---

## 6. Section View A–A (vertical, through centre at X = 150 mm)

```
        Lid (1.5 mm)
 ┌─────────────────────┐
 │   [Internal volume] │
 │   W_internal = 297  │
 │   H_internal = 197  │
 │   D_internal = 117  │
 │                     │
 └─────────────────────┘
        Body base (1.5 mm)
```

Internal clearance dimensions (nominal):

| Dimension | Value |
|-----------|-------|
| Internal width | 297 mm |
| Internal height | 197 mm |
| Internal depth | 117 mm |

---

## 7. DIN Rail Mounting (internal)

- One 35 mm symmetrical DIN rail (EN 60715) mounted horizontally inside.
- Rail fixed with 4 × M4 countersunk screws through base plate.
- Rail position: Y = 30 mm from enclosure bottom (base plate), centred at X = 150 mm.
- Rail length: 260 mm (leaving 20 mm clearance each side).

---

## 8. Material & Finish Specification

| Item | Specification |
|------|--------------|
| Material | Cold-rolled mild steel (CRCA), 1.5 mm, DC01 or equivalent |
| Surface prep | Phosphate wash + primer (before powder coat) |
| Powder coat | RAL 7035 (light grey), 60–80 µm thickness, gloss level 30–40 |
| Internal finish | Light grey powder coat (same batch) |
| Hardware | M4 captive screws: zinc-plated steel, quarter-turn (Dzus or equivalent) |
| Gasket | EPDM foam gasket, 10 mm × 3 mm, self-adhesive, full lid perimeter |
| DIN rail | Zinc-plated steel, 35 mm (EN 60715), 260 mm length |

---

## 9. IP54 Compliance Notes

- EPDM gasket must be continuous around lid with no joints at corners.
- All cable gland knockouts must be fitted with rated PG glands when installed.
- Louvre insect mesh must have no gaps larger than 1 mm.
- After assembly, validate with IEC 60529 §14.2.4 (dust) and §14.2.5 (water spray).

---

## 10. Hole Summary Table

| Feature | X (mm) | Y (mm) | Face | Ø (mm) | Notes |
|---------|--------|--------|------|--------|-------|
| KO1 cable gland | 50 | 60 | Bottom | 22 | PG16 |
| KO2 cable gland | 120 | 60 | Bottom | 20 | PG13.5 |
| KO3 cable gland | 190 | 60 | Bottom | 16 | PG11 |
| KO4 cable gland | 250 | 60 | Bottom | 16 | PG11 |
| M4 lid screw BL | 10 | 10 | Lid | 4.5 | Quarter-turn captive |
| M4 lid screw BR | 290 | 10 | Lid | 4.5 | Quarter-turn captive |
| M4 lid screw TL | 10 | 190 | Lid | 4.5 | Quarter-turn captive |
| M4 lid screw TR | 290 | 190 | Lid | 4.5 | Quarter-turn captive |
| M5 keyhole KH1 | 60 | 100 | Rear | 8/5.5 | Wall mount |
| M5 keyhole KH2 | 240 | 100 | Rear | 8/5.5 | Wall mount |
| LED1 hole | 130 | 30 | Lid | 5 | Green LED |
| LED2 hole | 150 | 30 | Lid | 5 | Blue LED |
| LED3 hole | 170 | 30 | Lid | 5 | Amber LED |
| PIR aperture | 250 | 30 | Lid | 8 | HC-SR501 |
| DIN M4 screws (×4) | 20,80,160,240 | 30 | Base | 4.5 | DIN rail fix |

All coordinates in mm from bottom-left corner of the respective face.
