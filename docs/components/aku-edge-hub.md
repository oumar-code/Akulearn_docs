<!--
COPILOT_PROMPT:
Refine the Aku Edge Hub doc. State Tier 1 role: local compute, IoT gateway, caching, ruggedized solar+wind hybrid power, and metrics endpoints.
Include 2D conceptual drawing description and hardware specs summary.
-->
# Aku Edge Hub (Tier 1)

## Role

The Aku Edge Hub is the Tier 1 node of the Aku Platform. Deployed at schools,
clinics, and community centres, it provides:

- **Local compute** — runs the Akulearn PWA, AI inference (Gemma), and local
  content cache without internet connectivity
- **IoT gateway** — collects sensor telemetry and exposes a `/metrics` endpoint
  (Prometheus-compatible) for scraping by the Aku Super Hub
- **Resilient power** — operates from a solar/wind hybrid power system with a
  LiFePO4 battery bank; continues operating through nights and overcast periods

## Hardware Summary

| Subsystem | Prototype Component | Production Target |
|---|---|---|
| SBC | Raspberry Pi 4 Model B (4 GB) | Jetson Orin Nano / Rockchip RK3588 |
| Storage | 256 GB NVMe SSD | Industrial-grade eMMC + NVMe |
| Wi-Fi | AP mode, Wi-Fi 5 | Wi-Fi 6, dual-band |
| Power input | 24 V DC from hybrid charge controller | 24 V / 48 V DC bus |
| Battery | LiFePO4, 50 Ah @ 24 V (1.2 kWh usable) | Expandable to 2.4 kWh |
| Solar | 100–200 Wp monocrystalline panel | Overspecced for Zamfara conditions |
| Wind | 300–500 W small turbine (prototype evaluation) | Site-specific |
| Energy controller | Hybrid MPPT (solar + wind) + dump-load | Same |
| Energy monitoring | INA3221 multi-channel current/voltage | Same |

## Power Architecture

See [`docs/hardware/clean_energy_power_system.md`](../hardware/clean_energy_power_system.md)
for the full solar and wind system design, component selection rationale, and
prototype readiness checklist.

### Block Diagram (Conceptual)

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

## Metrics Endpoints

The Edge Hub exposes the following key Prometheus metrics (scraped by the Super
Hub monitoring stack):

| Metric | Description |
|---|---|
| `edge_uptime_percent{site}` | Hub availability over rolling 24 h |
| `edge_batt_voltage_volts{site}` | Battery bus voltage |
| `edge_battery_soc_percent{site}` | State of Charge (from BMS) |
| `edge_solar_voltage_volts{site}` | Solar PV input voltage |
| `edge_wind_voltage_volts{site}` | Wind turbine rectified DC voltage |
| `edge_load_current_amps{site}` | Total load current drawn by hub |
| `edge_cpu_temp_celsius{site}` | SBC CPU temperature |
| `aku_cache_hit_ratio{site}` | Local content cache efficiency |

For full KPI definitions see `monitoring/kpi_dashboard_spec.md`.
