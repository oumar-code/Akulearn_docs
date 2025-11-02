# Edge Hub - Component Selection (Initial Shortlist)

This document lists candidate components, SKUs, and rationales for the Edge Hub prototype.

## Compute Modules
- NVIDIA Jetson Orin Nano 16GB (orderable SKU: `JNX-ONX-16GB` or vendor SKU) — Good balance of performance and power for vision/edge ML.
- NVIDIA Jetson Orin NX (for higher throughput) — consider 8GB/16GB variants depending on models.
- Raspberry Pi Compute Module 4 (CM4) — for low-cost variants; pair with Google Coral USB/NPU for ML acceleration.

## Power & BMS
- MPPT Charge Controller: Victron SmartSolar MPPT 75/15 or equivalent; for custom boards consider TI MPPT reference designs (e.g., BQ24650 family)
- DC-DC Converters: 12V -> 5V (for USB/C devices) and 3.3V/1.8V rails for sensors and SoC power islands — use high-efficiency synchronous buck converters (e.g., TI LMR33630 or Murata converters).
- Battery: LiFePO4 12V, 20Ah baseline (EVE or Winston cells) with a BMS supporting SMBus telemetry.

## RF Modules
- LoRa: Semtech SX1262 module or Murata CMWX1ZZABZ-078 — industrial modules with good regional support.
- Wi-Fi/BLE: Industrial M.2 or mini-PCIe Wi-Fi module supporting 2.4/5GHz (e.g., Intel AX200 family or Qualcomm modules) with external antenna connectors.
- Cellular: Quectel EG25-G (4G) or RM series for 5G — ensure regional band support and MFF2/eSIM variants as needed.

## Sensors & Peripherals
- Camera modules: Raspberry Pi High Quality (HQ) camera or Sony IMX series MIPI modules.
- Environmental sensors: Sensirion SHT4x (I2C), Bosch BME688 (I2C), ST accelerometers (I2C/SPI).
- GNSS: u-blox NEO-M8 series (UART) for accurate location and timing.

## Connectors & Enclosure
- Waterproof connectors: M12 Ethernet, waterproof USB A/C options, gland seals for external cables.
- Enclosure: Off-the-shelf IP67 enclosure with custom CNC/moulded lid for antenna and connector placements; consider injection molding for production.

## Notes
- Confirm SKU availability and lead times; maintain alternate suppliers for critical parts.
- Where possible, choose module footprints that minimize RF certification burden (pre-certified modules simplify device certification).
