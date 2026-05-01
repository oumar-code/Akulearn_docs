# Firmware — Device Watchdog

**Target MCU:** Raspberry Pi Pico (RP2040)  
**Language:** MicroPython  
**Version:** 1.0.0  

This module supervises the Aku Edge Hub SBC (Raspberry Pi 4B or Jetson Orin Nano).
If the SBC fails to send a heartbeat over UART within a configurable timeout window,
the watchdog cuts power to the SBC via a relay and restores it after a configurable
reset delay, performing a hard reboot.

---

## Design

```
SBC → heartbeat ("PING\n" over UART every 30 s)
        │
    Watchdog MCU (Pico RP2040)
        │  timeout > 90 s?
        ▼
    Relay opens → 5 V supply to SBC cut → waits 5 s → relay closes → power restored
```

---

## Watchdog Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Heartbeat interval (expected) | 30 s | SBC sends "PING\n" every 30 s |
| Watchdog timeout | 90 s | 3 × heartbeat interval |
| Reset hold-off (power cut) | 5 s | Duration SBC power is cut |
| Max resets before alert | 3 | After 3 resets, blink error LED and halt |

---

## Hardware Connections

| Pico Pin | Signal | Purpose |
|----------|--------|---------|
| GP0 (UART0 TX) | (optional) | Send commands to SBC |
| GP1 (UART0 RX) | UART from SBC | Receive "PING\n" heartbeat |
| GP15 | Relay control | HIGH = SBC powered, LOW = power cut |
| GP16 | Error LED | Blinks on repeated resets |
| VBUS (pin 40) | Relay VCC | 5 V for relay coil |
| GND (pin 38) | Relay GND | Common ground |

**Relay wiring:**

| Relay terminal | Connection |
|----------------|-----------|
| COM | 5 V supply to SBC |
| NO (normally open) | SBC 5 V input → normally closed (relay coil energised) |
| NC | Unconnected |

---

## Flash Instructions

```bash
# Prerequisites: Python 3.11+, mpremote
pip install mpremote

# Connect the Raspberry Pi Pico via USB
# Flash MicroPython once (if not already) from micropython.org/download/rp2-pico/

# Copy watchdog firmware to the Pico
mpremote connect auto cp firmware/device-watchdog/main.py :main.py

# The watchdog starts automatically on next power cycle
```

---

## SBC Heartbeat Integration

The Aku-EdgeHub software must send `PING\n` over the UART connected to the Pico
at regular intervals. Add the following systemd timer or background task:

```python
# In Aku-EdgeHub app startup (app/main.py)
import asyncio
import serial  # pyserial

async def heartbeat_task(port: str = "/dev/ttyACM0", interval: int = 30) -> None:
    """Send PING\n to the hardware watchdog at regular intervals."""
    ser = serial.Serial(port, 115200, timeout=1)
    while True:
        ser.write(b"PING\n")
        await asyncio.sleep(interval)
```

> **Note:** The Pico appears as `/dev/ttyACM0` or `/dev/ttyUSB0` depending on the
> USB driver. Verify with `ls /dev/tty*` after plugging in.

---

## Status

- [x] RP2040 MicroPython implementation complete (`main.py`)
- [x] UART heartbeat parsing implemented
- [x] Relay power-cut and restore logic implemented
- [x] Error LED blink and max-reset halt implemented
- [ ] Integration test with Edge Hub SBC
- [ ] Hardware relay board design (PCB — see `hardware/edge-hub/pcb/`)
- [ ] Flash and validate on physical Pico + relay hardware

---

## Related

- [Energy Monitor firmware](../energy-monitor/README.md)
- [Firmware README](../README.md)
- [Edge Hub Integration Test](../../testing/edge-hub-integration-test.md)

