# Aku Edge Hub — Hybrid Power System

The Aku Edge Hub operates reliably in off-grid and weak-grid environments
(e.g., rural Zamfara state). Power is supplied by a **solar PV + small wind
turbine** hybrid system feeding a LiFePO4 battery bank, with an MPPT charge
controller managing both sources.

---

## System Block Diagram

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

## Load Profile

| Load | Average Power | Daily Hours | Daily Energy |
|------|--------------|-------------|--------------|
| SBC + Wi-Fi + Storage | 25 W | 24 h | 600 Wh |
| Projector | 60 W | 3 h | 180 Wh |
| **Total** | | | **780 Wh/day** |

---

## Energy Budget (Zamfara Site)

| Parameter | Value |
|-----------|-------|
| Daily load | 780 Wh |
| Solar irradiance (average) | 5.5–6.0 peak sun hours (PSH) |
| Solar irradiance (worst-case — harmattan) | 4.5 PSH |
| Panel derating (temp + dust + wiring) | 15 % |
| Solar harvest (200 Wp, 4.5 PSH × 0.85) | ~765 Wh/day |
| Wind harvest (300 W avg, 2 h effective) | ~600 Wh/day |
| Net surplus | ~585 Wh/day |
| Battery autonomy without generation | ~1.5 days |
| Design target autonomy | 2 days (200 Wp solar) |

---

## Documents in this Directory

| File | Contents |
|------|----------|
| [`solar-subsystem.md`](solar-subsystem.md) | Solar panel selection, charge controller, wiring |
| [`wind-turbine.md`](wind-turbine.md) | Wind turbine spec, blade aerodynamics, installation |
| [`battery-storage.md`](battery-storage.md) | LiFePO4 battery bank, BMS, autonomy calculation |
| [`energy-monitoring.md`](energy-monitoring.md) | INA3221 integration, Prometheus metrics |

---

## Related

- [Firmware — Energy Monitor](../../firmware/energy-monitor/README.md) — INA3221 firmware
- [Hardware — Edge Hub](../edge-hub/README.md) — how power connects to the SBC
