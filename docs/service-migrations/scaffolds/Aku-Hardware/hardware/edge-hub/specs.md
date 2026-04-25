# Aku Edge Hub — Full Hardware Specification

**Revision:** A (Prototype)  
**Date:** 2025-Q2  
**Status:** Active — prototype deployment in Zamfara state pilot

---

## 1. Single-Board Computer (SBC)

| Parameter | Prototype (Gen 1) | Production Target (Gen 2) |
|-----------|-------------------|---------------------------|
| Model | Raspberry Pi 4 Model B | NVIDIA Jetson Orin Nano 8 GB |
| CPU | Broadcom BCM2711, Quad-core Cortex-A72, 1.8 GHz | 6-core Arm Cortex-A78AE |
| RAM | 4 GB LPDDR4-3200 | 8 GB LPDDR5 |
| GPU / NPU | VideoCore VI (no NPU) | 1024-core Ampere GPU + DLA |
| OS | Raspberry Pi OS Lite 64-bit (Bookworm) | JetPack 6 (Ubuntu 22.04) |
| AI inference | CPU-only Gemma 2B int8 | GPU-accelerated Gemma 7B |

## 2. Storage

| Parameter | Prototype | Production |
|-----------|-----------|------------|
| Primary | 256 GB PCIe NVMe SSD (M.2 2280 via USB 3.0 HAT) | 256 GB industrial eMMC on SOM |
| Expansion | USB 3.0 external SSD (optional) | M.2 2280 NVMe slot |
| SD Card | 32 GB (OS only) | Not used (eMMC boot) |
| Endurance | Consumer-grade | Industrial temp (-40 °C to +85 °C), SLC cache |

## 3. Networking

| Parameter | Prototype | Production |
|-----------|-----------|------------|
| Wi-Fi AP | TP-Link EAP225 (Wi-Fi 5, AC1350, dual-band) via USB | Wi-Fi 6 AP module (dual-band) |
| AP mode | `hostapd` on 2.4 GHz (range) + 5 GHz (throughput) | Same |
| Max clients | 50 concurrent devices | 100 concurrent devices |
| Ethernet | GbE RJ45 (uplink to ISP / satellite modem) | Same |
| Backhaul | 4G LTE USB dongle (optional fallback) | Integrated LTE CAT-6 module |

## 4. Power

| Parameter | Prototype | Production |
|-----------|-----------|------------|
| Input voltage | 24 V DC (from MPPT charge controller) | 24 V or 48 V DC |
| SBC supply | 5 V / 3 A via USB-C PD buck converter | Same |
| Wi-Fi AP supply | 12 V / 1.5 A DC-DC | Same |
| Idle power | ~15 W (SBC + Wi-Fi, no inference) | ~20 W |
| Peak power | ~25 W (SBC under load) | ~35 W (GPU inference) |
| Projector supply | 230 V AC via inverter (separate circuit) | Same |

## 5. Sensors & I/O

| Component | Interface | Purpose |
|-----------|-----------|---------|
| INA3221 | I²C (address 0x40) | 3-channel current/voltage monitoring |
| DS18B20 (×2) | 1-Wire (GPIO 4) | Ambient + enclosure temperature |
| PIR sensor | GPIO (GPIO 17) | Motion-activated display wake |
| Status LEDs (×3) | GPIO (GPIO 22, 23, 24) | Power, Wi-Fi, sync status |
| USB-A (×4) | USB 3.0 / 2.0 | Peripheral expansion |
| HDMI (×2) | HDMI 2.0 | Projector output + facilitator display |
| 3.5 mm audio | PWM audio | Speaker for audio content |

## 6. Enclosure

| Parameter | Value |
|-----------|-------|
| Material | Powder-coated mild steel (IP54 rated) |
| Dimensions (W×H×D) | 300 × 200 × 120 mm |
| Mounting | Wall bracket or surface-mount |
| Operating temperature | 0 °C to +55 °C ambient |
| Storage temperature | -20 °C to +70 °C |
| Humidity | 5 %–95 % non-condensing |
| Protection | IP54 (dust-protected, splash-resistant) |

## 7. Certifications (Target)

| Certification | Requirement |
|---------------|-------------|
| NCC (Nigeria) | Type approval for Wi-Fi equipment |
| CE (export) | EMC Directive 2014/30/EU |
| RoHS | Directive 2011/65/EU |
| ECOWAS | Regional type approval |
