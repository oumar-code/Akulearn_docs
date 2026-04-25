# Maintenance Guide

This guide covers preventive and corrective maintenance for deployed Aku Edge Hubs.

---

## Maintenance Schedule

### Monthly (Facilitator)

| Task | How |
|------|-----|
| Clean solar panel glass | Damp cloth (morning, no direct sun) |
| Check Edge Hub status LEDs | All three should be on; red = fault |
| Verify Wi-Fi hotspot active | Connect a device; confirm internet-less content loads |
| Check battery indicator on charge controller | Should show "Float" or "Full" |
| Report any unusual noises from wind turbine (if installed) | Log in support portal |

### Quarterly (Field Engineer)

| Task | How |
|------|-----|
| Inspect all cable connections | Check for corrosion, loose terminals; re-torque if needed |
| Check battery terminal voltage under load | Multimeter: should be ≥ 23 V |
| Read BMS balance status | All cells within ±0.05 V |
| Check INA3221 readings | Via `/metrics` endpoint or SSH |
| Inspect enclosure gasket | Replace if cracked or compressed |
| Update Aku-EdgeHub software | `sudo apt update && sudo systemctl restart aku-edgehub` |
| Check NVMe SSD SMART status | `smartctl -a /dev/nvme0n1` — reallocated sectors should be 0 |
| Blow out dust from enclosure louvres | Compressed air or soft brush |
| Check Wi-Fi AP — connected client count | Via EAP225 controller or `iw dev wlan0 station dump` |

### Annually (Hardware Engineer)

| Task | How |
|------|-----|
| Full battery capacity test | Discharge at 0.2C; record Ah; replace if < 70 % rated |
| Re-grease all M-thread cable glands | Cable gland compound |
| Check mast / panel tilt bracket for corrosion | Re-paint any bare metal; re-tighten bolts |
| Wind turbine blade inspection (if installed) | Look for surface cracks or delamination; re-coat if needed |
| Verify all grounding connections (earth stake) | Measure impedance ≤ 10 Ω |
| Replace enclosure door gasket (IP seal) | Standard PVC foam cord gasket |
| Firmware version check and update | Flash latest `fw-energy-monitor-vX.Y.Z` to Pico |

---

## Fault Diagnosis

### No Power / Edge Hub not booting

1. Check battery voltage at Terminal Block TB1 — should be 22–29 V.
2. Check 5 A input fuse — replace if blown.
3. Check U7 buck converter output — should be 5.0–5.1 V.
4. If U7 output OK but RPi does not boot — check microSD card and USB-C cable.

### Wi-Fi LED off / No SSID

1. SSH in; check `systemctl status hostapd` or EAP225 management interface.
2. Restart Wi-Fi service: `sudo systemctl restart hostapd` (or EAP225 reboot).
3. Check Ethernet uplink (WAN LED on EAP225).

### Sync LED flashing (sync fail)

1. Check internet connectivity: `ping 8.8.8.8`.
2. Check Aku-EdgeHub service: `journalctl -u aku-edgehub -n 50`.
3. Check Super Hub endpoint reachability.

### Battery voltage declining over days

1. Check solar panel output: INA3221 CH1 current should be > 0 A in daylight.
2. Inspect solar panel glass for shading or dirt.
3. Check MPPT controller fault LED.
4. Check dump-load controller — if stuck open, it may be discharging battery.

### Wind turbine not spinning (if installed)

1. Check wind speed with anemometer — must be > 2.5 m/s for cut-in.
2. Check cable continuity from turbine to rectifier.
3. Inspect blades for damage or ice (harmattan dust build-up).

---

## Spare Parts Inventory (per 10 units deployed)

| Part | Quantity |
|------|----------|
| 5 A blade fuse | 20 |
| MicroSD card 32 GB | 2 |
| USB-C PD buck module (U7) | 2 |
| INA3221 breakout | 1 |
| Enclosure gasket (600 mm cord) | 2 m |
| Raspberry Pi Pico (watchdog/energy-monitor) | 2 |
| Thermal paste 4 g | 1 syringe |
| Cable ties 200 mm (bag of 100) | 1 bag |
