# Firmware — Device Watchdog

**Target MCU:** Raspberry Pi Pico (RP2040) or ATtiny85  
**Language:** MicroPython (RP2040) / C (ATtiny85)  
**Version:** 0.1.0 (stub — implementation in progress)

This module supervises the Aku Edge Hub SBC (Raspberry Pi 4B or Jetson Orin Nano).
If the SBC fails to send a heartbeat over USB serial or GPIO within a configurable
timeout window, the watchdog cuts power to the SBC via a relay and restores it
after a configurable reset delay, performing a hard reboot.

---

## Design

```
SBC → heartbeat (USB serial "PING\n" every 30 s)
        │
    Watchdog MCU (Pico / ATtiny85)
        │  timeout > 90 s?
        ▼
    Relay cuts 5 V supply to SBC → waits 5 s → restores power
```

---

## Watchdog Parameters (configurable)

| Parameter | Default | Notes |
|-----------|---------|-------|
| Heartbeat interval (expected) | 30 s | SBC sends "PING\n" every 30 s |
| Watchdog timeout | 90 s | 3 × heartbeat interval |
| Reset hold-off (power cut) | 5 s | Duration SBC power is cut |
| Max resets before alert | 3 | After 3 resets, blink error LED |

---

## Hardware Connections (RP2040 variant)

| Pico Pin | Signal | Purpose |
|----------|--------|---------|
| GP0 (UART0 TX) | Serial to SBC | (optional: receive heartbeat) |
| GP1 (UART0 RX) | Serial from SBC | Receive "PING\n" heartbeat |
| GP15 | Relay control | HIGH = SBC powered, LOW = cut |
| GP16 | Error LED | Blinks on repeated resets |
| USB | Serial to host | Debug / config |

---

## Status

- [ ] RP2040 MicroPython implementation (in progress)
- [ ] ATtiny85 C implementation (planned)
- [ ] Integration test with Edge Hub SBC
- [ ] Hardware relay board design

---

## Related

- [Energy Monitor firmware](../energy-monitor/README.md)
- [Firmware README](../README.md)
