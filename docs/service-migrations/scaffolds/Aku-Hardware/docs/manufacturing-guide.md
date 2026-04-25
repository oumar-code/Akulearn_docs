# Manufacturing Guide

This guide describes the production manufacturing process for the Aku Edge Hub
(Gen 1 Prototype). It covers sourcing, assembly workflow, quality control, and
packaging.

---

## Production Workflow

```
Sourcing → Incoming QC → Sub-assembly → Final Assembly → Testing → Packaging → Deployment
```

---

## 1. Sourcing

### Approved Suppliers

| Component | Primary Supplier | Backup Supplier |
|-----------|-----------------|-----------------|
| Raspberry Pi 4B | Approved RPi distributors (RS/Farnell) | OKdo, PiShop |
| INA3221 breakout | Adafruit (US) | Pimoroni (UK) |
| NVMe SSD | Western Digital / Samsung (authorised) | Kingston |
| LiFePO4 cells | CALB / EVE (authorised distributor) | Lishen |
| Steel enclosure | Local fabricator (Kano) | Spelsberg (import) |
| Wi-Fi AP | TP-Link (authorised) | Ubiquiti |

### Lead Times (prototype volumes < 50 units)

| Component | Lead Time |
|-----------|-----------|
| RPi 4B | 2–4 weeks (allocation-dependent) |
| LiFePO4 battery pack | 3–6 weeks |
| Custom enclosure | 1–2 weeks (local fabrication) |
| Electronics (MOQ) | 1–2 weeks |

---

## 2. Incoming Quality Control (IQC)

Each incoming batch must be inspected before use:

| Item | IQC Check |
|------|----------|
| RPi 4B | Boot test, USB, HDMI, Ethernet functional |
| INA3221 | I²C device scan confirms address 0x40 |
| NVMe SSD | SMART status = PASS; read/write speed test |
| LiFePO4 cells | OCV ≥ 3.2 V per cell; IR < 1 mΩ |
| Enclosure | No cracks, cable gland threads intact, IP seal present |
| Cables & connectors | Visual inspection; continuity test |

**Reject rate target:** < 1 % for electronic components, < 3 % for mechanical.

---

## 3. Sub-Assembly Steps

### 3a. Battery Pack Assembly

1. Sort cells by capacity (within 2 % of rated Ah).
2. Spot-weld nickel strips in 8S2P configuration.
3. Attach BMS to cell pack; connect balance leads in order.
4. Apply heat-shrink wrap.
5. Label with cell lot number, date, and capacity (measured at 0.5C discharge).

### 3b. Enclosure Preparation

1. Fabricate from DXF template (see `/enclosure/` CAD files when available).
2. Powder-coat in RAL 7035 light grey.
3. Install cable glands, DIN rail, and lid fasteners.
4. Apply exterior label with serial number, voltage, and warning markings.

### 3c. Electronics Pre-Test

1. Flash Raspberry Pi OS Lite to SD card using Raspberry Pi Imager.
2. Install Aku-EdgeHub software per [Aku-EdgeHub README](https://github.com/oumar-code/Aku-EdgeHub).
3. Flash INA3221 firmware to Pico (see `firmware/energy-monitor/README.md`).
4. Verify I²C communication on bench.

---

## 4. Final Assembly

Follow the step-by-step procedure in
[`hardware/edge-hub/assembly.md`](../hardware/edge-hub/assembly.md).

---

## 5. Quality Control (QC) Testing

Each completed unit must pass:

1. [Power System Acceptance Test](../testing/power-system-test.md)
2. [Edge Hub Integration Test](../testing/edge-hub-integration-test.md)

Both test sheets must be completed, signed, and filed with the unit's serial
number record before the unit is released for deployment.

---

## 6. Packaging

| Item | Packaging |
|------|----------|
| Edge Hub unit | Cardboard box (foam-lined), 350 × 250 × 180 mm |
| Accessories (cables, mounting kit) | Zip-lock bag inside box |
| Quick-start card | Laminated A5, inside box lid |
| Serial number | Sticker on outside of box |

---

## 7. Serial Number Format

`AEH-YYYYMM-NNN`

- `AEH` — Aku Edge Hub
- `YYYYMM` — year and month of manufacture
- `NNN` — sequential unit number (001–999)

Example: `AEH-202506-001`
