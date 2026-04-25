# Battery Storage Subsystem

---

## Battery Specification

| Parameter | Prototype |
|-----------|-----------|
| Chemistry | LiFePO4 (Lithium Iron Phosphate) |
| Nominal voltage | 24 V (8S configuration) |
| Capacity | 50 Ah (1.2 kWh nominal, ~1 kWh usable) |
| Max depth of discharge (DoD) | 80 % |
| Usable capacity | 1.2 kWh × 80 % = **960 Wh usable** |
| Cycle life | > 2000 cycles to 80 % capacity |
| BMS | Active balancing, OVP / UVP / OTP protection |
| Cell arrangement | 8S2P (8 cells in series × 2 in parallel) |
| Cell format | 100 Ah prismatic cells (e.g., CALB CA100 or EVE LF105) |

---

## Autonomy Calculation

| Load | Power | Daily Hours | Daily Energy |
|------|-------|-------------|--------------|
| SBC + Wi-Fi + Storage | 25 W | 24 h | 600 Wh |
| Projector | 60 W | 3 h | 180 Wh |
| **Total** | | | **780 Wh/day** |

```
Autonomy = Usable capacity / Daily load
         = 960 Wh / 780 Wh per day
         ≈ 1.23 days (prototype: 50 Ah @ 24 V)

With 200 Wp solar (4.5 PSH × 0.85 derating = 765 Wh/day harvest):
  Net daily surplus = 765 Wh - 780 Wh ≈ -15 Wh (near break-even — add wind turbine)
  With wind turbine (300 W rated, 2 effective hours = 600 Wh):
  Net daily surplus = 1365 Wh - 780 Wh = +585 Wh → full recharge each day
```

**Design target:** 2 days of autonomy → upgrade to 100 Ah battery (2 kWh usable).

---

## Battery Management System (BMS)

| Function | Setpoint |
|----------|----------|
| Overvoltage protection (OVP) | 29.2 V (3.65 V/cell) |
| Undervoltage protection (UVP) | 20.0 V (2.5 V/cell) |
| Over-temperature protection (OTP) | 60 °C |
| Low-temperature charge cutoff | 0 °C |
| Max continuous discharge current | 100 A |
| Max continuous charge current | 50 A |
| Balancing | Active (cell-to-cell) |

---

## Wiring & Safety

| Item | Specification |
|------|--------------|
| Battery cable (+ and -) | 4 AWG, 600 V rated, < 0.5 m |
| Battery fuse | 125 A mega fuse, within 150 mm of positive terminal |
| Disconnect switch | 150 A battery isolator switch (accessible from outside enclosure) |
| Terminal torque | M8 bolt: 8 N·m; M6 bolt: 5 N·m |

> ⚠️ **LiFePO4 batteries are thermally stable but still store significant energy.
> Always use insulated tools. Never short the battery terminals. Wear eye protection.**

---

## Maintenance Schedule

| Interval | Task |
|----------|------|
| Monthly | Check terminal torque; inspect for corrosion |
| Quarterly | Record cell voltages under load via BMS display |
| Annually | Full capacity test: discharge at 0.2C, record capacity in Ah |
| At replacement | When capacity falls below 70 % rated (< 700 Wh usable) |

---

## Prototype Readiness

- [x] LiFePO4 battery bank assembled and BMS configured
- [x] Capacity and cycle testing initiated
- [ ] 100 Ah upgrade for 2-day autonomy target
- [ ] Environmental enclosure (ventilated, >IP44)
