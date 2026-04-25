# Solar Subsystem

---

## Panel Specification

| Parameter | Prototype | Production Target |
|-----------|-----------|-------------------|
| Panel type | Monocrystalline silicon | Monocrystalline high-efficiency |
| Peak power | 100–200 Wp | 200–400 Wp (site-dependent) |
| Open-circuit voltage (Voc) | ~22 V (12 V nominal) | 24 V or 48 V string |
| Short-circuit current (Isc) | ~5.5 A | ~11 A per 200 Wp panel |
| Mounting | Fixed tilt, south-facing | Adjustable tilt bracket |
| Charge controller | PWM (prototype) → MPPT upgrade | Dual-input MPPT |

---

## Solar Irradiance Assumptions (Zamfara State)

| Season | Daily Peak Sun Hours (PSH) |
|--------|---------------------------|
| Dry season (Oct–Mar) | 5.5–6.0 PSH |
| Rainy season (Apr–Sep) | 4.0–5.0 PSH |
| Harmattan (design worst-case) | 4.5 PSH |

Panel derating: **15 %** (temperature coefficient × ambient temp, dust on glass, wiring losses).

---

## MPPT Charge Controller

| Parameter | Prototype | Production |
|-----------|-----------|------------|
| Model | Epever Tracer-AN 20A | Victron SmartSolar MPPT 100/20 |
| Max solar input | 260 Wp (12 V) | 290 Wp |
| Battery voltage | 12 V / 24 V auto | 12 V / 24 V / 48 V selectable |
| Max charge current | 20 A | 20 A |
| Communication | RS485 (Modbus) | Bluetooth + VE.Direct |
| Wind input | No (separate dump-load controller) | Yes (dual-input models) |

> **Prototype note:** The prototype uses a PWM controller that will be replaced by
> an MPPT unit for the pilot deployment. MPPT increases harvest efficiency by 10–30 %.

---

## Wiring

| Wire | Gauge | Length | Notes |
|------|-------|--------|-------|
| Panel (+) to charge controller PV+ | 10 AWG | ≤ 5 m | MC4 connector at panel end |
| Panel (-) to charge controller PV- | 10 AWG | ≤ 5 m | MC4 connector at panel end |
| Controller BAT+ to battery+ | 8 AWG | ≤ 1 m | Include 30 A fuse within 150 mm of battery |
| Controller BAT- to battery- | 8 AWG | ≤ 1 m | |
| Controller LOAD+ to DC bus+ | 10 AWG | ≤ 1 m | 20 A fuse inline |
| Controller LOAD- to DC bus- | 10 AWG | ≤ 1 m | |

---

## Grounding

- Panel frame → 6 AWG to earth stake (≤ 10 Ω ground impedance).
- Charge controller chassis → 6 AWG to earth stake.
- Battery negative → single ground reference (do not double-ground).

---

## Prototype Readiness

- [x] Solar panel and MPPT controller procured and bench-tested
- [x] 100 Wp panel installed on fixed south-facing tilt bracket
- [ ] 200 Wp panel upgrade (production pilot)
- [ ] Adjustable tilt bracket for seasonal optimisation
