# Firmware — Energy Monitor (INA3221)

**Target MCU:** Raspberry Pi Pico (RP2040)  
**Language:** MicroPython  
**Version:** 1.0.0

This module runs on a Raspberry Pi Pico attached to the Aku Edge Hub SBC via
USB serial. It reads all three INA3221 channels (solar, wind, load) at 1 Hz and
streams JSON-formatted readings to the SBC, which ingests them into the
Prometheus metrics endpoint.

---

## Hardware Connections

| Pico Pin | Signal | INA3221 Pin |
|----------|--------|-------------|
| GP4 (I2C0 SDA) | SDA | SDA |
| GP5 (I2C0 SCL) | SCL | SCL |
| 3V3 (physical pin 36) | VCC | VCC |
| GND (physical pin 38) | GND | GND |

**I²C address:** `0x40` (A0, A1 both tied to GND)

---

## Output Format

The firmware prints one JSON object per second to USB serial (115200 baud):

```json
{
  "ts": 1716800400,
  "solar_v": 24.12,
  "solar_a": 3.45,
  "wind_v":  23.98,
  "wind_a":  1.20,
  "load_v":  24.05,
  "load_a":  1.80
}
```

The Aku-EdgeHub Python service reads this stream from `/dev/ttyACM0` and
converts it to Prometheus gauge metrics.

---

## Quick Start

```bash
# 1. Flash MicroPython to the Pico (one-time)
# Download from https://micropython.org/download/rp2-pico/ and copy .uf2 in BOOTSEL mode.

# 2. Upload the firmware
pip install mpremote
mpremote connect auto fs cp firmware/energy-monitor/main.py :main.py

# 3. Verify output
mpremote connect auto repl
# Press Ctrl+D to soft-reset — JSON lines should appear on the REPL
```

---

## Changelog

### v1.0.0
- Initial release: INA3221 3-channel read at 1 Hz, JSON serial output
