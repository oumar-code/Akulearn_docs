# Aku Platform Hardware Strategy

This document outlines the phased, tiered strategy for hardware and schematic design across the Aku Platform: Edge Hubs (Tier 1), Super Hubs (Tier 2), and IG-Hub (Tier 3). It focuses on ruggedness, solar integration, modularity, and AI/ML capability.

## Overarching Principles
- Requirements-driven design: trace decisions to measurable requirements (compute, power, environmental, cost).
- Modular components with standard interfaces (PCIe, USB, Ethernet, MIPI, GPIO) for upgradeability and repair.
- Power efficiency: MPPT charge controllers, LiFePO4 batteries, multiple power rails and careful power sequencing.
- Environmental resilience: IP-rated enclosures, conformal coating, dust filters, and extended temperature components.
- Thermal management: passive + active cooling options depending on compute load.
- Hardware security: TPM, secure boot, tamper detection, and firmware signing.

## Phased Approach
1. Requirements capture and component shortlist.
2. Block diagrams and schematic fragments for PMU, compute module carrier, RF front-end, and sensor interfaces.
3. Rapid prototyping with dev-kits; measure power and RF performance.
4. Alpha PCB + enclosure fit-checks.
5. Environmental and performance validation. Iterate.
6. Pilot builds and scaling to production BOM.

## Edge Hub (Tier 1) - Summary
- Goal: Rugged, solar-powered edge node for local inference and data collection.
- Candidate compute modules: NVIDIA Jetson Orin Nano (16GB), Jetson Orin NX, Raspberry Pi Compute Module 4 (for lower-cost variants).
- Power: Design for 50W solar panels, LiFePO4 battery (12V/20Ah+ depending on load), MPPT controller with LiFePO4 profile.
- Connectivity: LoRa/SX126x, Wi-Fi 6 module, optional 4G/5G eSIM-capable modem.
- Sensors: Camera (MIPI CSI), environmental sensors (I2C), vibration (ADC), GNSS (UART/SPI).

## Super Hub (Tier 2) - Summary
- Goal: Rack-mounted data center node for aggregation, regional ML processing and storage.
- Use COTS server platforms (Supermicro/Dell/HP) with optional GPU accelerators (NVIDIA H100/A100) or Jetson AGX Orin modules for constrained deployments.
- Networking: 10GbE or 25/40GbE depending on regional backbone.

## IG-Hub (Tier 3) - Summary
- Goal: High-availability logical gateway (cloud-native + co-location) and minimal physical footprint at IXPs.
- Prefer managed cloud deployments (GCP) with co-location for low-latency peering and HSMs for key management where required.

## Deliverables
- Hardware folder skeleton (this repo)
- Edge Hub block diagrams & KiCad schematic template
- Super Hub procurement checklist and rack diagrams
- IG-Hub network and co-location diagrams
- BOM templates and supplier recommendations

## Next Steps
1. Formalize Edge Hub SKU selection and capture precise power budgets.
2. Start KiCad project under `hardware/edge/` and create initial PMU schematic.
3. Create BOM template and begin supplier outreach for long-lead items.
