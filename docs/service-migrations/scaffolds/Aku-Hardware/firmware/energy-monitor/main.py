"""
Aku Edge Hub — INA3221 Energy Monitor Firmware
Target: Raspberry Pi Pico (RP2040) running MicroPython
Version: 1.0.0

Reads solar (CH1), wind (CH2), and load (CH3) current and voltage from the
INA3221 at 1 Hz and prints a JSON line to USB serial for ingestion by the
Aku-EdgeHub software stack.

Wiring:
  Pico GP4 (I2C0 SDA) → INA3221 SDA
  Pico GP5 (I2C0 SCL) → INA3221 SCL
  Pico 3V3 (pin 36)   → INA3221 VCC
  Pico GND (pin 38)   → INA3221 GND
  INA3221 A0, A1      → GND  (I2C address 0x40)
"""

import json
import time

from machine import I2C, Pin  # type: ignore[import]  # MicroPython built-in

# ── INA3221 register map ──────────────────────────────────────────────────────
_INA3221_ADDR = 0x40

_REG_CONFIG = 0x00
_REG_CH1_SHUNT = 0x01  # CH1 shunt voltage
_REG_CH1_BUS = 0x02    # CH1 bus voltage
_REG_CH2_SHUNT = 0x03  # CH2 shunt voltage
_REG_CH2_BUS = 0x04    # CH2 bus voltage
_REG_CH3_SHUNT = 0x05  # CH3 shunt voltage
_REG_CH3_BUS = 0x06    # CH3 bus voltage

# Default config: all 3 channels enabled, 1.1 ms conversion time, 128 averages
_CONFIG_DEFAULT = 0x7127

# Shunt resistance in Ohms (0.1 Ω on Adafruit INA3221 breakout board)
_SHUNT_OHMS = 0.1


def _read_register(i2c: I2C, reg: int) -> int:
    """Read a 16-bit big-endian register from the INA3221."""
    data = i2c.readfrom_mem(_INA3221_ADDR, reg, 2)
    return (data[0] << 8) | data[1]


def _signed16(value: int) -> int:
    """Convert unsigned 16-bit to signed (two's complement)."""
    if value >= 0x8000:
        return value - 0x10000
    return value


def read_channel(i2c: I2C, shunt_reg: int, bus_reg: int) -> tuple[float, float]:
    """
    Read one INA3221 channel.

    Returns:
        (bus_voltage_V, current_A)
    """
    # Shunt voltage LSB = 40 µV (per INA3221 datasheet)
    raw_shunt = _signed16(_read_register(i2c, shunt_reg))
    shunt_mv = raw_shunt * 40e-6  # V

    # Bus voltage LSB = 8 mV
    raw_bus = _read_register(i2c, bus_reg)
    bus_v = (raw_bus >> 3) * 8e-3  # V (bits [15:3], shift right 3)

    current_a = shunt_mv / _SHUNT_OHMS

    return round(bus_v, 3), round(current_a, 3)


def main() -> None:
    """Main loop: read INA3221 at 1 Hz, emit JSON to serial."""
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400_000)

    # Verify device present
    devices = i2c.scan()
    if _INA3221_ADDR not in devices:
        print(json.dumps({"error": "INA3221 not found", "scanned": devices}))
        return

    # Write config register (enable all channels, continuous mode)
    i2c.writeto_mem(
        _INA3221_ADDR,
        _REG_CONFIG,
        bytearray([(_CONFIG_DEFAULT >> 8) & 0xFF, _CONFIG_DEFAULT & 0xFF]),
    )

    while True:
        solar_v, solar_a = read_channel(i2c, _REG_CH1_SHUNT, _REG_CH1_BUS)
        wind_v, wind_a = read_channel(i2c, _REG_CH2_SHUNT, _REG_CH2_BUS)
        load_v, load_a = read_channel(i2c, _REG_CH3_SHUNT, _REG_CH3_BUS)

        payload = {
            "ts": time.time(),
            "solar_v": solar_v,
            "solar_a": solar_a,
            "wind_v": wind_v,
            "wind_a": wind_a,
            "load_v": load_v,
            "load_a": load_a,
        }
        print(json.dumps(payload))
        time.sleep(1)


main()
