# Wind Turbine Subsystem

---

## Turbine Specification

| Parameter | Prototype | Production Target |
|-----------|-----------|-------------------|
| Turbine type | Horizontal-axis (HAWT), 3-blade | HAWT, site-optimised |
| Rated power | 300–500 W | 500 W–1 kW |
| Cut-in wind speed | 2.5 m/s | ≤ 2.5 m/s |
| Rated wind speed | 11–12 m/s | 10–12 m/s |
| Cut-out wind speed | 15 m/s (furling) | 15–20 m/s |
| Hub height | 6 m (prototype mast) | 9–12 m |
| Output | 3-phase AC → rectifier → DC bus | Same |
| Dump-load controller | Resistive dump load (24/48 V rated) | Same |

---

## Blade Aerodynamics

### Design Principles

- **Aerofoil profile** — NACA 4412 (or equivalent) low-Reynolds-number aerofoil,
  optimised for the low-to-moderate wind speeds typical of rural northern Nigeria
  (3–10 m/s annual mean at hub height).
- **Tip Speed Ratio (TSR)** — Target TSR of **6–7** at rated wind speed, balancing
  power extraction efficiency against acoustic noise and mechanical stress.
- **Blade count** — Three blades provide optimal balance of aerodynamic efficiency,
  structural fatigue life, and gyroscopic stability.
- **Chord and twist distribution** — Blade chord tapers linearly from root (~120 mm)
  to tip (~40 mm); twist decreases from ~14° at root to ~2° at tip, following
  Betz-optimal distribution for the target TSR and site wind profile.
- **Swept area** — Prototype rotor diameter: 1.2–1.5 m (swept area ≈ 1.1–1.8 m²).
  Production blades sized for swept area required by 500 W rated power at rated wind speed.

### Aerodynamic Performance Parameters

| Parameter | Value |
|-----------|-------|
| Design Cp (power coefficient) | 0.38–0.42 (prototype target) |
| Betz limit (theoretical max) | 0.593 |
| Efficiency vs. Betz | ~65–70 % |
| Stall type | Passive stall (fixed pitch) |
| Reynolds number at tip (rated) | ~2 × 10⁵ |
| Lift/drag ratio (design point) | ~40–50 |

### Blade Materials

| Tier | Material |
|------|----------|
| Prototype | Glass-fibre reinforced polymer (GFRP) hand-layup, or HDPE carved |
| Production | Pultruded GFRP or injection-moulded reinforced nylon |

### Blade Testing & Validation

1. **CFD simulation** — OpenFOAM steady-state RANS (k-ω SST) for lift/drag polar
   at operating Reynolds numbers before physical fabrication.
2. **Wind-tunnel testing** — Scale model validation at local university partner
   facilities (target: University of Sokoto / ABU Zaria).
3. **Field spin-up** — Blade set mounted on prototype mast; power curve measured
   against anemometer data and compared to BEM (Blade Element Momentum) model.
4. **Fatigue check** — 10⁷ cycle equivalent loading; materials safety factor ≥ 3
   for prototype, ≥ 5 for production.

### Noise & Safety

- Target A-weighted sound level: **< 45 dB(A)** at 30 m (school/community setting).
- Tip speed limited to **≤ 60 m/s** (passive stall / furling envelope).
- Physical blade guard / exclusion zone: 1.5 × rotor diameter radius from mast base,
  clearly marked on site.

---

## Rectifier & Dump-Load Controller

| Component | Description |
|-----------|-------------|
| Rectifier | 3-phase full-wave bridge rectifier, 50 A, 100 V (e.g., KBPC5010) |
| Dump-load controller | Morningstar TS-45 or equivalent; sized for peak turbine output × 1.25 |
| Dump-load resistor | 48 V / 500 W stainless steel water heater element (passive heat dissipation) |

The dump-load controller diverts excess wind energy to the resistive element when
the battery is full, preventing over-voltage damage to the battery and rectifier.

---

## Installation

1. Erect the mast at a minimum hub height of 6 m, clear of buildings and trees
   by at least 2 × hub height on the prevailing-wind side.
2. Lay 3-core cable (10 AWG, rated 600 V) from turbine to rectifier enclosure
   using buried conduit (min 600 mm depth).
3. Connect rectifier output to dump-load controller, then to the hybrid MPPT
   charge controller or battery bus.
4. Commission dump-load controller per manufacturer instructions — set the voltage
   setpoint to match battery bank full-charge voltage.

---

## Prototype Readiness

- [x] Turbine blade aerodynamic design complete (CFD simulation — NACA 4412)
- [x] Rectifier sourced and bench-tested
- [ ] Physical blade fabrication (GFRP hand-layup) — **in progress**
- [ ] Wind-tunnel validation at partner institution (University of Sokoto)
- [ ] Field mast installation and power-curve measurement
- [ ] Dump-load controller integration and over-voltage testing

---

## References

- Betz, A. (1926). *Wind-Energie und ihre Ausnutzung durch Windmühlen.*
- Manwell, J. F., McGowan, J. G., & Rogers, A. L. (2009). *Wind Energy Explained:
  Theory, Design and Application* (2nd ed.). Wiley.
- NACA Technical Report NACA-TM-1148 (aerofoil data).
- OpenFOAM v10 documentation — [openfoam.org](https://openfoam.org).
