# Edge Hub Integration Test

**Unit serial:** _______________  
**Software version:** _______________  
**Test date:** _______________  
**Tested by:** _______________

---

## Prerequisites

- [ ] Power system acceptance test PASSED (see [`power-system-test.md`](power-system-test.md))
- [ ] Raspberry Pi 4B flashed with latest Raspberry Pi OS Lite 64-bit
- [ ] Aku-EdgeHub software installed per [Aku-EdgeHub README](https://github.com/oumar-code/Aku-EdgeHub)
- [ ] INA3221 firmware flashed to Pico (see [`../firmware/energy-monitor/`](../firmware/energy-monitor/))
- [ ] Wi-Fi AP configured (SSID: `Akulearn_Hub_<serial>`, WPA2 passphrase set)

---

## Test 1 — Boot & Connectivity

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| RPi boots within 60 s of power-on | Yes | | |
| SSH accessible on LAN IP | Yes | | |
| Aku-EdgeHub service running (`systemctl status aku-edgehub`) | `active (running)` | | |
| `/api/v1/health/offline` returns 200 OK | Yes | | |
| `uptime` shows no unexpected reboots | Yes (0 reboots) | | |

---

## Test 2 — INA3221 Energy Monitor

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| `/dev/ttyACM0` present (Pico firmware running) | Yes | | |
| JSON output readable: `cat /dev/ttyACM0` | Valid JSON, 1 Hz | | |
| Solar voltage CH1 (bench supply 24 V) | 23.5–24.5 V | | |
| Load current CH3 (RPi + AP powered) | 1.5–2.5 A | | |
| `/metrics` endpoint returns `edge_solar_voltage_volts` | Yes | | |
| `/metrics` endpoint returns `edge_load_current_amps` | Yes | | |

---

## Test 3 — Storage

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| NVMe SSD detected (`lsblk`) | `/dev/nvme0n1` or `/dev/sda` | | |
| Content directory mounted (`/data`) | Yes | | |
| Write speed (dd test) | ≥ 200 MB/s | | |
| Read speed (dd test) | ≥ 400 MB/s | | |
| SQLite DB accessible | Yes (Aku-EdgeHub creates it on first run) | | |

---

## Test 4 — Wi-Fi Hotspot

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| SSID `Akulearn_Hub_<serial>` visible on test device | Yes | | |
| WPA2 authentication succeeds | Yes | | |
| Test device receives DHCP lease | Yes (192.168.4.x) | | |
| HTTP access to Edge Hub API from Wi-Fi device | Yes (via LAN IP) | | |
| 5 simultaneous devices connected | Yes (no drops) | | |
| 2.4 GHz channel (coverage test, 30 m) | Signal ≥ −75 dBm | | |

---

## Test 5 — Content Sync

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| `/api/v1/sync/trigger` POST returns 202 | Yes | | |
| Sync job visible in logs (`journalctl -u aku-edgehub`) | Yes | | |
| Content served from local cache after sync | Yes | | |
| Cache hit ratio metric `aku_cache_hit_ratio` > 0 | Yes (after content load) | | |

---

## Test 6 — AI Inference (Local Gemma)

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| `/api/v1/ai/infer` POST returns 200 with model output | Yes | | |
| Inference time (Gemma 2B int8, RPi 4B) | < 30 s per request | | |
| CPU temperature during inference | < 80 °C | | |

---

## Test 7 — Projector Output

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| Projector powers on from 230 V AC inverter | Yes | | |
| HDMI signal detected by projector | Yes | | |
| Video content plays without artefacts | Yes | | |
| Audio output from projector speaker | Yes | | |

---

## Test 8 — 24-Hour Soak

Run the unit under full load (SBC + Wi-Fi + 3 h projector) for 24 hours.

| Check | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| No unplanned reboots (check `last reboot`) | 0 reboots | | |
| No service crashes (`journalctl -p err`) | 0 errors | | |
| Max SBC CPU temperature | < 80 °C | | |
| Max enclosure temperature | < 55 °C | | |
| Battery SoC at end of 24 h (with solar) | ≥ 80 % | | |

---

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test engineer | | | |
| Hardware lead | | | |

**Overall result:** ☐ PASS   ☐ FAIL

**Notes:**
