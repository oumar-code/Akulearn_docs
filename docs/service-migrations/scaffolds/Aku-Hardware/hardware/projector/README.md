# Aku Projector Module — Overview

The Aku Projector is the classroom display device that pairs with the Aku Edge Hub
to deliver facilitator-led group learning sessions to communities without reliable
electricity or internet. It is powered from the Edge Hub's 230 V AC inverter output.

---

## Key Requirements

| Requirement | Value |
|-------------|-------|
| Minimum brightness | 2000 ANSI lumens (indoor daylight) |
| Native resolution | 1280 × 800 (WXGA) or higher |
| Input | HDMI 1.4 |
| Power supply | 90–240 V AC, 50/60 Hz |
| Power consumption | ≤ 80 W (LED lamp) |
| Lamp life | ≥ 30 000 hours (LED) |
| Operating temperature | 0 °C to +45 °C |
| Connectivity | HDMI input + USB-A (media player) |
| Audio | Built-in 10 W speaker |

---

## Recommended Models

| Tier | Model | ANSI Lumens | Lamp | Price (USD) |
|------|-------|-------------|------|-------------|
| Prototype | ViewSonic PA503W | 3600 | DLP LED | ~299 |
| Prototype alt | Optoma ML1080 | 1200 | LED | ~449 |
| Production | Anker Nebula Solar Portable | 400 | LED | ~600 |
| Production HD | BenQ MX532 | 3300 | DLP LED | ~499 |

> **Note:** For outdoor / high-ambient-light deployments, target ≥ 3000 ANSI lumens.
> For night-time indoor classes, 1200 ANSI lumens is acceptable.

---

## Mounting Options

1. **Ceiling mount** — fixed installation in a permanent classroom (bracket included with most projectors).
2. **Tripod mount** — portable deployment to community spaces; use a 1/4"-20 tripod adapter.
3. **Wall shelf** — low-cost fixed install; 300 × 150 mm powder-coated bracket.

---

## Documents in this Directory

| File | Contents |
|------|----------|
| [`specs.md`](specs.md) | Full projector specification and selection criteria |
| [`bom.md`](bom.md) | Bill of Materials — projector kit |

---

## Integration with Edge Hub

The projector connects to the Aku Edge Hub via:

- **HDMI** (video + audio) from RPi HDMI0 port
- **Power** from the Edge Hub's DC-UPS / inverter 230 V AC output

The Aku-SmartBoard software (oumar-code/Aku-SmartBoard) manages display output,
content playback, and facilitator controls via the Compose Desktop UI on the RPi.
