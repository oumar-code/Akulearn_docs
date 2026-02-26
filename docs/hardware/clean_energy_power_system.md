# Clean Energy Power System

This document describes the solar and wind hybrid power system used in the **Aku
Edge Hub** clean energy prototype. It covers component selection rationale,
system architecture, turbine blade aerodynamics, and prototype readiness.

---

## 1. System Overview

The Edge Hub is designed to operate reliably in off-grid and weak-grid
environments (e.g., rural Zamfara state). Power is supplied by a **solar PV +
small wind turbine** hybrid system feeding a LiFePO4 battery bank, with an MPPT
charge controller managing both sources.

```
Solar Panel(s) ──►┐
                  │  Hybrid MPPT Charge Controller
Wind Turbine  ──►─┤  + Dump-Load Controller
                  │
                  ▼
           LiFePO4 Battery Bank (BMS)
                  │
                  ▼
        DC-UPS / Inverter-Charger
        ├── 12 V / 19 V DC → SBC, Wi-Fi, Storage
        └── 230 V AC        → Projector Module
```

---

## 2. Solar Subsystem

| Parameter | Prototype Value | Production Target |
|---|---|---|
| Panel type | Monocrystalline silicon | Monocrystalline (high-efficiency) |
| Peak power | 100–200 Wp | 200–400 Wp (site-dependent) |
| Voc | ~22 V (12 V nominal) | 24 V or 48 V string |
| Mounting | Fixed tilt, south-facing | Adjustable tilt bracket |
| Charge controller | PWM → MPPT upgrade | Dual-input MPPT |

### 2.1 Solar Irradiance Assumptions (Zamfara)

- Average daily solar irradiance: **5.5–6.0 peak sun hours (PSH)**
- Design worst-case: **4.5 PSH** (harmattan season)
- Panel derating: 15 % (temperature, dust, cable losses)

---

## 3. Wind Subsystem

| Parameter | Prototype Value | Production Target |
|---|---|---|
| Turbine type | Horizontal-axis (HAWT), 3-blade | HAWT, site-optimised |
| Rated power | 300–500 W | 500 W–1 kW |
| Cut-in wind speed | 2.5 m/s | ≤ 2.5 m/s |
| Rated wind speed | 11–12 m/s | 10–12 m/s |
| Cut-out wind speed | 15 m/s (furling) | 15–20 m/s |
| Hub height | 6 m (prototype mast) | 9–12 m |
| Output | 3-phase AC → rectifier → DC bus | Same |
| Dump-load controller | Resistive dump load (48 V rated) | Same |

### 3.1 Turbine Blade Aerodynamics

Turbine blade aerodynamics are a critical factor in prototype performance and are
fully included in the clean energy design. The following principles and parameters
govern blade selection and geometry for the Aku Edge Hub wind subsystem.

#### 3.1.1 Blade Design Principles

- **Aerofoil profile** — Blades use a **NACA 4412** (or equivalent) low-Reynolds-
  number aerofoil, optimised for the low-to-moderate wind speeds typical of rural
  northern Nigeria (3–10 m/s annual mean at hub height).
- **Tip Speed Ratio (TSR)** — Target TSR of **6–7** at rated wind speed, balancing
  power extraction efficiency against acoustic noise and mechanical stress.
- **Blade count** — Three blades provide optimal balance of aerodynamic efficiency,
  structural fatigue life, and gyroscopic stability. Two-blade designs were
  rejected due to higher vibration loads at low TSR.
- **Chord and twist distribution** — Blade chord tapers linearly from root
  (~120 mm) to tip (~40 mm); twist decreases from ~14° at root to ~2° at tip,
  following Betz-optimal distribution for the target TSR and site wind profile.
- **Swept area** — Prototype rotor diameter: **1.2–1.5 m** (swept area ≈ 1.1–
  1.8 m²). Production blades will be sized to swept area required by the 500 W
  rated power target at rated wind speed.

#### 3.1.2 Aerodynamic Performance Parameters

| Parameter | Value |
|---|---|
| Design Cp (power coefficient) | 0.38–0.42 (prototype target) |
| Betz limit | 0.593 (theoretical maximum) |
| Efficiency vs. Betz | ~65–70 % |
| Stall type | Passive stall (fixed pitch) |
| Reynolds number at tip (rated) | ~2 × 10⁵ |
| Lift/drag ratio (design point) | ~40–50 |

#### 3.1.3 Blade Materials

- **Prototype** — Glass-fibre reinforced polymer (GFRP) hand-layup, or carved
  high-density polyethylene (HDPE) for rapid-iteration testing.
- **Production** — Pultruded GFRP or injection-moulded reinforced nylon for cost
  and consistency.

#### 3.1.4 Blade Testing & Validation

1. **CFD simulation** — OpenFOAM steady-state RANS (k-ω SST) for lift/drag polar
   at operating Reynolds numbers before physical fabrication.
2. **Wind-tunnel testing** — Scale model validation at local university partner
   facilities (target: University of Sokoto / ABU Zaria).
3. **Field spin-up** — Blade set mounted on prototype mast; power curve measured
   against anemometer data and compared to BEM (Blade Element Momentum) model.
4. **Fatigue check** — 10⁷ cycle equivalent loading estimate; materials safety
   factor ≥ 3 for prototype, ≥ 5 for production.

#### 3.1.5 Noise & Safety

- Target A-weighted sound level: **< 45 dB(A)** at 30 m (school/community
  setting).
- Tip speed limited to **≤ 60 m/s** to stay within passive-stall / furling
  operational envelope and reduce tip-vortex noise.
- Physical blade guard / exclusion zone: 1.5 × rotor diameter radius from mast
  base, clearly marked on site.

---

## 4. Energy Storage

| Parameter | Prototype Value |
|---|---|
| Chemistry | LiFePO4 (Lithium Iron Phosphate) |
| Capacity | 50 Ah @ 24 V (1.2 kWh usable) |
| Max depth of discharge | 80 % |
| BMS | Active balancing, over-voltage / under-voltage / over-temp protection |
| Cycle life | > 2000 cycles to 80 % capacity |

### 4.1 Autonomy Calculation

- Edge Hub load: ~25 W average (SBC + Wi-Fi + storage)
- Projector load: ~60 W (3 h/day teaching sessions)
- Daily energy: 25 W × 24 h + 60 W × 3 h = **780 Wh/day**
- Usable capacity: 1 200 Wh
- **Autonomy without generation: ~1.5 days** (design target: 2 days with 200 Wp solar)

---

## 5. Charge Controller & Dump-Load

- **Hybrid MPPT controller** — accepts both solar PV (up to 400 Wp) and rectified
  wind DC input; tracks maximum power point for each source independently.
- **Dump-load controller** — diverts excess wind energy to a resistive heating
  element when battery is full, preventing over-voltage damage. Sized for peak
  turbine output × 1.25 safety margin.

---

## 6. Energy Monitoring

The INA3221 three-channel current/voltage sensor on the Edge Hub provides:

| Channel | Measurement |
|---|---|
| CH1 | Solar PV current & voltage |
| CH2 | Wind turbine DC current & voltage |
| CH3 | Total load current & voltage |

Metrics are exposed via the `/metrics` Prometheus endpoint. See
[`monitoring/kpi_dashboard_spec.md`](../monitoring/kpi_dashboard_spec.md) for
full KPI definitions.

---

## 7. Prototype Readiness Checklist

- [x] Solar panel and MPPT controller procured and bench-tested
- [x] LiFePO4 battery bank assembled and BMS configured
- [x] INA3221 sensor integration with Edge Hub firmware
- [x] Turbine blade aerodynamic design (CFD simulation complete — NACA 4412)
- [ ] Physical blade fabrication (GFRP hand-layup) — **in progress**
- [ ] Wind-tunnel validation at partner institution
- [ ] Field mast installation and power-curve measurement
- [ ] Dump-load controller integration and over-voltage testing
- [ ] Full hybrid system 72-hour burn-in test

---

## 8. References

- Betz, A. (1926). *Wind-Energie und ihre Ausnutzung durch Windmühlen.*
- Manwell, J. F., McGowan, J. G., & Rogers, A. L. (2009). *Wind Energy Explained:
  Theory, Design and Application* (2nd ed.). Wiley.
- NACA Technical Report NACA-TM-1148 (aerofoil data).
- INA3221 datasheet — Texas Instruments SBOS498.
- OpenFOAM v10 documentation — [openfoam.org](https://openfoam.org).
