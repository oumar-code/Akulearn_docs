# Firmware

This directory contains embedded firmware for the microcontrollers and sensors
used in the Aku Edge Hub hardware stack.

---

## Modules

| Directory | Target MCU | Language | Purpose |
|-----------|-----------|---------|---------|
| [`energy-monitor/`](energy-monitor/) | RP2040 (Raspberry Pi Pico) | MicroPython | INA3221 3-channel energy monitoring; streams JSON to Edge Hub SBC |
| [`device-watchdog/`](device-watchdog/) | RP2040 / ATtiny85 | MicroPython / C | Hardware watchdog — resets SBC if heartbeat is lost |

---

## Toolchain Setup

### MicroPython (energy-monitor, device-watchdog on RP2040)

```bash
# Prerequisites
pip install mpremote

# Download MicroPython for RP2040 from: https://micropython.org/download/rp2-pico/
# Flash MicroPython once (hold BOOTSEL, plug in USB, release BOOTSEL — appears as USB drive):
cp rp2-pico-*.uf2 /media/$USER/RPI-RP2/

# After reboot, verify connection:
mpremote connect auto repl

# Upload firmware module:
mpremote connect auto fs cp firmware/energy-monitor/main.py :main.py

# Run immediately without saving:
mpremote connect auto run firmware/energy-monitor/main.py
```

### C / Arduino (device-watchdog on ATtiny85)

```bash
# Install avr-gcc toolchain:
sudo apt-get install gcc-avr avr-libc avrdude

# Build:
cd firmware/device-watchdog
make

# Flash via USBasp programmer:
make flash
```

---

## Testing Firmware

```bash
# Install test dependencies:
pip install pytest

# Run unit tests (host-side, mocked hardware):
pytest firmware/
```

---

## Versioning

Firmware versions follow [SemVer](https://semver.org/):

- Tag format: `fw-<module>-v<MAJOR>.<MINOR>.<PATCH>` (e.g., `fw-energy-monitor-v1.0.0`)
- Changelog entries in the module `README.md`.

---

## CI

The `firmware-ci.yml` workflow runs `pylint` on all `*.py` firmware files and
`pytest` on any available unit tests on every pull request.
