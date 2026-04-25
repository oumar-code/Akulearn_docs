# Aku Edge Hub — Bill of Materials

**Revision:** A (Prototype)  
**Date:** 2025-Q2  
Prices are indicative retail (USD). Production pricing subject to volume negotiation.

---

## Prototype BOM (Gen 1 — Raspberry Pi 4B)

| # | Ref | Description | MPN / Model | Qty | Unit Cost (USD) | Supplier |
|---|-----|-------------|-------------|-----|-----------------|---------|
| 1 | U1 | Raspberry Pi 4 Model B, 4 GB | SC0195 | 1 | 55.00 | Raspberry Pi |
| 2 | U2 | INA3221 3-channel current/voltage sensor breakout | Adafruit 4162 | 1 | 9.95 | Adafruit |
| 3 | U3 | DS18B20 waterproof temperature sensor (×2) | DS18B20-PAR | 2 | 4.50 | Adafruit |
| 4 | U4 | TP-Link EAP225 Wi-Fi 5 access point | EAP225 | 1 | 59.99 | TP-Link |
| 5 | U5 | WD Blue SN570 NVMe SSD, 500 GB M.2 2280 | WDS500G3B0C | 1 | 45.00 | Western Digital |
| 6 | U6 | Argon ONE M.2 NVMe HAT for RPi 4 | ARG-RPiCASE-M.2 | 1 | 35.00 | Argon40 |
| 7 | U7 | USB-C PD buck converter 24 V→5 V/5 A | — | 1 | 8.00 | Generic |
| 8 | U8 | DC-DC buck converter 24 V→12 V/3 A | LM2596S module | 1 | 3.50 | Generic |
| 9 | U9 | MicroSD card 32 GB (OS) | SanDisk SDSQUAR | 1 | 9.00 | SanDisk |
| 10 | J1 | GbE RJ45 patch cord, 1 m | — | 1 | 2.00 | Generic |
| 11 | J2 | HDMI cable, 2 m (projector) | — | 1 | 5.00 | Generic |
| 12 | J3 | USB-C power cable, 0.3 m | — | 1 | 3.00 | Generic |
| 13 | SW1 | Status LED board (3× LED + 330 Ω resistors) | — | 1 | 1.50 | Generic |
| 14 | SW2 | PIR motion sensor (HC-SR501) | HC-SR501 | 1 | 2.00 | Generic |
| 15 | E1 | IP54 steel enclosure, 300×200×120 mm | — | 1 | 28.00 | Generic |
| 16 | M1 | DIN rail + standoffs + cable ties | — | 1 | 4.00 | Generic |
| — | — | **Prototype BOM Total (approx.)** | | | **~275 USD** | |

---

## Production BOM Delta (Gen 2 — Jetson Orin Nano)

Changes from prototype BOM (all other items remain similar):

| # | Ref | Description | MPN | Qty | Unit Cost (USD) | Notes |
|---|-----|-------------|-----|-----|-----------------|-------|
| 1 | U1 | NVIDIA Jetson Orin Nano 8 GB Module | 900-13767-0030-000 | 1 | 199.00 | Replaces RPi 4B |
| 2 | U1a | Jetson Orin Nano Developer Kit Carrier Board | — | 1 | 149.00 | Or custom carrier |
| 3 | U4 | Wi-Fi 6 AP module (dual-band, PoE) | UAP-AC-LITE / similar | 1 | 99.00 | Replaces EAP225 |
| 4 | U5 | Industrial NVMe SSD 256 GB, -40–85 °C | Innodisk DDEM4 | 1 | 120.00 | Replaces WD Blue |
| — | — | **Additional cost vs prototype** | | | **~+313 USD** | |

---

## Consumables & Spares

| Item | Qty per unit | Purpose |
|------|-------------|---------|
| Cable ties, nylon 200 mm | 20 | Cable management |
| M3 standoffs × 15 mm (×4) | 4 | PCB mounting |
| Thermal paste (Noctua NT-H1) | 1 g | SBC heatsink |
| Fuse, 5 A automotive blade | 2 | Power rail protection |
| Fuse holder, in-line | 1 | 24 V input protection |
