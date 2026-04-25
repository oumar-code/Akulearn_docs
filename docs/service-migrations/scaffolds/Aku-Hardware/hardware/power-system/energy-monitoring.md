# Energy Monitoring — INA3221 Integration

The Aku Edge Hub uses the **Texas Instruments INA3221** triple-channel shunt and
bus voltage monitor (I²C) to measure power flows from solar, wind, and total load.
Metrics are exposed via a Prometheus `/metrics` endpoint in the
[Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) software stack.

---

## INA3221 Overview

| Parameter | Value |
|-----------|-------|
| Interface | I²C, 400 kHz (fast mode) |
| Address | 0x40 (A0, A1 both GND) |
| Channels | 3 independent shunt + bus voltage |
| Shunt voltage range | ±163.84 mV (full-scale), ±40.96 mV (typical) |
| Bus voltage range | 0–26 V |
| Shunt resistance | 0.1 Ω per channel (100 mΩ, 1 % tolerance) |
| Resolution | 40 µV (shunt), 8 mV (bus) |
| Datasheet | TI SBOS498 |

---

## Channel Assignment

| Channel | Measurement Point | Metric Name |
|---------|------------------|-------------|
| CH1 | Solar PV DC input wire | `edge_solar_voltage_volts`, `edge_solar_current_amps` |
| CH2 | Wind turbine rectified DC wire | `edge_wind_voltage_volts`, `edge_wind_current_amps` |
| CH3 | Total load (24 V → converters) | `edge_load_voltage_volts`, `edge_load_current_amps` |

---

## Derived Metrics

The Aku-EdgeHub firmware computes and exposes:

| Metric | Formula | Unit |
|--------|---------|------|
| `edge_solar_power_watts` | V_CH1 × I_CH1 | W |
| `edge_wind_power_watts` | V_CH2 × I_CH2 | W |
| `edge_load_power_watts` | V_CH3 × I_CH3 | W |
| `edge_battery_soc_percent` | Derived from battery voltage + coulomb counting | % |
| `edge_batt_voltage_volts` | Battery bus voltage (from CH3 bus reading) | V |

---

## Full Prometheus Metrics Inventory

| Metric | Description |
|--------|-------------|
| `edge_uptime_percent{site}` | Hub availability over rolling 24 h |
| `edge_batt_voltage_volts{site}` | Battery bus voltage |
| `edge_battery_soc_percent{site}` | State of Charge (from BMS coulomb counter) |
| `edge_solar_voltage_volts{site}` | Solar PV input voltage |
| `edge_solar_current_amps{site}` | Solar PV input current |
| `edge_solar_power_watts{site}` | Solar PV input power |
| `edge_wind_voltage_volts{site}` | Wind turbine rectified DC voltage |
| `edge_wind_current_amps{site}` | Wind turbine DC current |
| `edge_wind_power_watts{site}` | Wind turbine DC power |
| `edge_load_current_amps{site}` | Total load current |
| `edge_load_power_watts{site}` | Total load power |
| `edge_cpu_temp_celsius{site}` | SBC CPU temperature |
| `edge_enclosure_temp_celsius{site}` | Enclosure internal temperature (DS18B20) |
| `aku_cache_hit_ratio{site}` | Local content cache efficiency |

All metrics are scraped by the Aku Super Hub Prometheus instance at 60-second intervals.

---

## Wiring

See [hardware/edge-hub/wiring.md — INA3221](../edge-hub/wiring.md) for the full I²C
pin assignments and shunt placement diagram.

---

## Firmware

The INA3221 MicroPython driver lives in
[`firmware/energy-monitor/main.py`](../../firmware/energy-monitor/main.py).

For the production Python library used by the FastAPI app on the RPi, see the
[Aku-EdgeHub](https://github.com/oumar-code/Aku-EdgeHub) software repo:
`app/services/energy_monitor.py`.

---

## Prototype Readiness

- [x] INA3221 sensor integration with Edge Hub firmware
- [x] Prometheus metrics endpoint live at `/metrics`
- [ ] Grafana dashboard template published (see `monitoring/kpi_dashboard_spec.md` in Akulearn_docs)
