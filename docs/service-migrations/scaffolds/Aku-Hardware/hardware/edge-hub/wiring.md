# Aku Edge Hub — Wiring & Connector Guide

**Revision:** A (Prototype)

This document covers all power and signal connections inside the Aku Edge Hub
enclosure. Follow all wiring exactly as described; incorrect wiring can damage
components or create a fire hazard.

---

## Safety Precautions

> ⚠️ **Always disconnect the battery and solar input before opening the enclosure.**
> The 24 V DC bus can deliver dangerous current even when the solar panel is covered.

- Use appropriate wire gauges (see table below).
- Protect all 24 V inputs with an in-line fuse.
- Secure all cables with cable ties to prevent chafing.
- Label all terminal blocks before first power-on.

---

## Wire Gauge Reference

| Circuit | Current | Recommended AWG |
|---------|---------|-----------------|
| 24 V input (from charge controller) | 5 A max | 18 AWG |
| 24 V → 5 V buck (RPi supply) | 3 A max | 20 AWG |
| 24 V → 12 V buck (AP supply) | 2 A max | 22 AWG |
| I²C bus (SDA/SCL) | < 50 mA | 26 AWG / ribbon |
| 1-Wire (DS18B20) | < 10 mA | 26 AWG |
| GPIO (LEDs, PIR) | < 50 mA | 26 AWG |

---

## Power Rail Wiring

```
External 24 V DC input
        │
    [5 A fuse]
        │
   Terminal Block TB1
        ├── TB1-1 → U7 (24 V → 5 V/5 A buck) → USB-C → RPi 4B (U1)
        ├── TB1-2 → U8 (24 V → 12 V/3 A buck) → 12 V terminal → Wi-Fi AP (U4)
        └── TB1-3 → INA3221 CH3 shunt + → Load bus
                                         └── Combined load
```

---

## I²C Bus (GPIO Pins — Raspberry Pi 40-pin Header)

| Signal | RPi GPIO (BCM) | Physical Pin | INA3221 Pin |
|--------|---------------|--------------|-------------|
| SDA | GPIO 2 | Pin 3 | SDA |
| SCL | GPIO 3 | Pin 5 | SCL |
| VCC (3.3 V) | 3.3 V | Pin 1 | VCC |
| GND | GND | Pin 6 | GND |

**I²C address:** `0x40` (A0 and A1 pins both tied to GND on Adafruit 4162 breakout)

**Pull-up resistors:** 4.7 kΩ to 3.3 V on SDA and SCL (included on Adafruit 4162 breakout — do not add external resistors).

---

## INA3221 Channel Assignment

| Channel | Shunt Location | Measurement | Shunt Resistance |
|---------|---------------|-------------|-----------------|
| CH1 (IN1+/IN1-) | Solar PV input wire | Solar current & voltage | 0.1 Ω / 3 W |
| CH2 (IN2+/IN2-) | Wind turbine DC wire | Wind current & voltage | 0.1 Ω / 3 W |
| CH3 (IN3+/IN3-) | Load (24 V → converters) | Total load current | 0.1 Ω / 3 W |

---

## 1-Wire Bus (DS18B20 Temperature Sensors)

| Signal | RPi GPIO (BCM) | Physical Pin |
|--------|---------------|--------------|
| Data | GPIO 4 | Pin 7 |
| VCC (3.3 V) | 3.3 V | Pin 1 |
| GND | GND | Pin 9 |

**Pull-up:** 4.7 kΩ from Data to VCC (required — add externally if not on breakout).

**Sensor 1 address:** Ambient temperature sensor (outside enclosure).  
**Sensor 2 address:** Enclosure internal temperature (cable-tie to SBC heatsink).

---

## GPIO Assignments (Status LEDs & PIR)

| Function | RPi GPIO (BCM) | Physical Pin | Notes |
|----------|---------------|--------------|-------|
| Power LED (green) | GPIO 22 | Pin 15 | 330 Ω to 3.3 V |
| Wi-Fi LED (blue) | GPIO 23 | Pin 16 | 330 Ω to 3.3 V |
| Sync LED (amber) | GPIO 24 | Pin 18 | 330 Ω to 3.3 V |
| PIR signal | GPIO 17 | Pin 11 | HC-SR501 OUT pin |
| PIR VCC | 5 V | Pin 2 | HC-SR501 VCC |
| PIR GND | GND | Pin 14 | HC-SR501 GND |

---

## HDMI Connections

| Port | Use | Cable |
|------|-----|-------|
| RPi HDMI0 (micro-HDMI) | Projector module | Micro-HDMI to HDMI, 2 m |
| RPi HDMI1 (micro-HDMI) | Facilitator display (optional) | Micro-HDMI to HDMI, 1 m |
