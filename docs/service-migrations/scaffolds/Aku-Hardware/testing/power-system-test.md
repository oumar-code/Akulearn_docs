# Power System Acceptance Test

**Unit serial:** _______________  
**Test date:** _______________  
**Tested by:** _______________  
**Witnessed by:** _______________

---

## Pre-Test Checklist

- [ ] All solar panel connections made and MC4 connectors seated
- [ ] Battery fully charged (≥ 27.0 V for 24 V LiFePO4)
- [ ] All wiring per [`hardware/power-system/`](../hardware/power-system/) verified
- [ ] Dump-load resistor mounted and connected
- [ ] INA3221 sensor installed and I²C connections verified

---

## Test 1 — Solar Open-Circuit Voltage

**Pass criteria:** Voc ≥ 20.5 V (100 Wp mono panel in full sun or equivalent bench light)

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| Solar panel Voc (no load) | 20.5–22.5 V | | |
| Polarity correct (+ to PV+, − to PV−) | Yes | | |

---

## Test 2 — Charge Controller Operation

**Pass criteria:** Charge controller powers on; battery charging current > 0 A

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| Controller display — battery voltage | ≥ 24.0 V | | |
| Controller display — charge current | > 0.5 A (with solar input) | | |
| CH1 INA3221 solar current (via firmware) | > 0.5 A | | |
| Controller LOAD output voltage | 24.0 ± 0.5 V | | |

---

## Test 3 — Battery Bank

**Pass criteria:** Battery voltage under load remains ≥ 23.0 V; BMS does not trip

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| Open-circuit battery voltage | 25.6–29.2 V (LiFePO4) | | |
| Battery voltage under 20 A load (10 min) | ≥ 23.0 V | | |
| BMS temperature reading | < 45 °C | | |
| BMS balance LEDs (all cells balanced) | All green | | |

---

## Test 4 — DC-DC Converters

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| U7 output voltage (no load) | 5.0–5.1 V | | |
| U7 output voltage (3 A load) | 4.9–5.1 V | | |
| U8 output voltage (no load) | 12.0–12.3 V | | |
| U8 output voltage (2 A load) | 11.8–12.3 V | | |
| U7 heat (30 min at 3 A) | < 70 °C (case) | | |

---

## Test 5 — Inverter (230 V AC Output)

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| AC output voltage (no load) | 220–235 V AC | | |
| AC output voltage (projector 60 W load) | 215–235 V AC | | |
| Projector powers on and displays image | Yes | | |
| Inverter heat (30 min) | < 60 °C (case) | | |

---

## Test 6 — Dump-Load Controller

**Requires:** Battery fully charged (29.0 V), continuous solar/wind input

| Measurement | Expected | Actual | Pass/Fail |
|-------------|----------|--------|-----------|
| Dump-load activates when battery > 28.8 V | Yes | | |
| Dump-load resistor temperature (steady state) | < 100 °C | | |
| Battery voltage stays ≤ 29.2 V | Yes | | |

---

## Test 7 — 72-Hour Burn-In

**Pass criteria:** No faults or thermal anomalies over 72 continuous hours

| Check | Expected | Observed | Pass/Fail |
|-------|----------|----------|-----------|
| Enclosure temperature at 24 h | < 55 °C | | |
| Enclosure temperature at 72 h | < 55 °C | | |
| Battery voltage drift (start vs. end) | < ±0.5 V | | |
| No BMS protection events | 0 events | | |
| No dump-load fault events | 0 events | | |

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test engineer | | | |
| Witness / approver | | | |

**Overall result:** ☐ PASS   ☐ FAIL

**Notes:**
