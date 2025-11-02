# Edge Hub - Detailed Requirements

This file captures the initial requirements for the Aku Edge Hub (Tier 1). Use this as the canonical source when designing schematics, picking SKUs, and creating the PCB.

## Functional Requirements
- Local AI inference (vision models, lightweight transformer encoders) at near-real-time latencies.
- Local data collection from sensors and cameras; batching and resilient store-and-forward to upstream.
- Support for remote management (OTA firmware updates, metrics & logging).

## Compute
- Primary target: NVIDIA Jetson Orin Nano (16GB) or Jetson Orin NX for higher throughput.
- Low-cost variant: Raspberry Pi Compute Module 4 (CM4) with external NPU (e.g., Google Coral) if budget constrained.
- Storage: 64–256 GB eMMC or NVMe module (M.2) depending on SKU.

## Power
- Solar input: nominal 12–24V (50W panel recommended at 18V Vmp), MPPT charge controller supporting LiFePO4.
- Battery: LiFePO4, 12V nominal, 20Ah (~240Wh) as baseline; select BMS with cell balancing and SMBus/I2C telemetry.
- Peak power budget: 20–50W depending on compute module; idle budget: <5W with aggressive power gating.

## Connectivity
- LoRa/SX126x module with external SMA antenna connector.
- Dual-band Wi-Fi 6 module (external antenna connectors) and optional onboard BLE.
- Cellular modem with eSIM capability (optional) supporting 4G/5G bands common in ECOWAS markets.
- Ethernet: single GbE with PoE-in option for deployments where solar isn't used.

## Sensors & Peripherals
- Cameras: MIPI CSI-2 (1–2 lanes) with IMX or similar sensor modules.
- Environmental: I2C sensors (temperature, humidity, pressure).
- Vibration: accelerometer connected via I2C or SPI; optional ADC for higher-resolution sensors.
- GNSS: UART or SPI interface.

## Environmental
- Target ingress: IP65–IP67 enclosure for outdoor deployments.
- Operating temperature: -20°C to +60°C (select industrial temperature components where necessary).
- UV-stable enclosure materials and corrosion-resistant hardware.

## Mechanical
- Target dimensions: 25 x 25 x 15 cm (including mounting brackets).
- Wall and pole mounting options with stainless steel hardware.

## Security & Maintainability
- TPM for hardware root of trust and secure boot.
- Tamper detection switches and sealed screws for tamper evidence.
- Debug headers: JTAG, UART pins accessible via sealed panel.

## Test & Measurement Requirements
- Test points for key rails, inrush current measurement port, thermal sensors for CPU region, and RF test ports.

## Regulatory
- Design to meet CE/FCC where applicable and plan for local certification; cellular modules should be carrier-certified for target markets.
