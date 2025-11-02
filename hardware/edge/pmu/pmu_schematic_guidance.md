# PMU Schematic Guidance — Edge Alpha

This document provides a KiCad-friendly, component-level guidance for the Power Management Unit (PMU) schematic for the Edge Hub alpha.

Purpose
- Provide a clear set of recommended components, net names, connector pinouts, test points, and layout notes so a schematic author can create `pmu.sch` in KiCad.

High-level block diagram
- Solar panel -> MPPT charge controller -> Battery (LiFePO4) + BMS -> Main 12V rail -> DC-DC regulators -> SoC rails (5V, 3.3V, 1.8V)

Recommended reference components and footprints
- MPPT Charge Controller (external or module)
  - Example: Victron SmartSolar (commercial) or TI reference design using BQ24650 family for custom PCB.
  - If using an external module, treat as a black box with inputs: SOLAR+, SOLAR-, output: BATT+, BATT-, telemetry/comm: BMS_SMBUS (I2C-like) or UART.

- Battery Pack and BMS
  - Cells: LiFePO4 4S nominal 12.8V pack (e.g., 12.8V, 20Ah)
  - BMS: vendor-specific pack with cell balancing, charge/discharge MOSFETs, and SMBus or UART telemetry.
  - Connector: waterproof 2-3 pin power connector (e.g., M12 2-pin or Amphenol IP67) plus SMBus/JTAG header for telemetry.

- Protection
  - Input reverse-polarity protection (P-channel MOSFET or ideal diode IC)
  - TVS diodes on solar and external power lines
  - Slow-blow fuse on battery output (select rating >= expected inrush but protect against short)

- DC-DC regulators (recommend high-efficiency synchronous buck)
  - 12V main rail: direct from BMS output.
  - 5V BUCK: supplies USB, PoE frontend, peripherals. Example: Murata OKI-78SR-like module or TI TPS5430 footprint.
  - 3.3V BUCK: sensors, RF modules. Example: TI TPS62840 or similar.
  - 1.8V (if required): SoC IO or DDR rails depending on compute module.

- SoC/Compute power sequencing
  - Provide PWR_OK net from 12V rail through enable signals to DC-DC regulators.
  - Reset circuit: generate a RESET_N net to the compute module using supervisor IC (e.g., TPS3700) monitoring core rails.

- Decoupling and PI filtering
  - Place bulk electrolytic (or polymer) caps on 12V rail near the DC-DC inputs.
  - Place ceramic decoupling caps (0.1uF, 1uF) near regulator outputs and SoC power pins per vendor recommendations.

- Telemetry and monitoring
  - BMS telemetry: expose SMBUS/I2C net to the compute module via a level shifter if required.
  - Current sensing: optional shunt + amplifier (provide SENSE+ and SENSE- nets) for power profiling.
  - Temperature sensors: place thermal diode or NTC near CPU region and route to ADC channel.

- Test points and debug
  - Add labeled test points for: BATT+, BATT-, 12V, 5V, 3V3, 1V8, RESET_N, BMS_SDA, BMS_SCL, SENSE+, SENSE-, GND.
  - Add a discrete header for JTAG and UART (3.3V) accessible via a sealed debug port.

Connector pinouts (suggested)
- POWER_IN (solar panel): SOLAR+, SOLAR-, GND
- BATTERY: BATT+, BATT-, BMS_COMM (SMBus), BMS_GND
- OUT_12V: 12V, GND
- OUT_5V: 5V, GND
- OUT_3V3: 3.3V, GND
- DEBUG: UART_TX, UART_RX, JTAG_TCK, JTAG_TMS, JTAG_TDI, JTAG_TDO, GND

Footprints and symbol notes for KiCad
- Use standard footprints for through-hole or SMD inductors and capacitors depending on chosen DC-DC modules.
- Create a hierarchical sheet `pmu.sch` with sub-blocks for: Input Protection, MPPT Interface, Battery/BMS, DC-DC Regs, Monitoring & Test Points.

Layout and thermal notes
- Keep power traces wide; define 2oz copper pour for power plane if possible.
- Place thermal vias under any heat dissipating regulators.
- Keep analog sense traces (current shunt) away from high-current switch nodes; use Kelvin sensing if possible.

DFM and manufacturing notes
- Add accessible test points and a programming header for bootloader and firmware flash.
- Provide silk-screen reference for polarity and connector orientation to assist assembly.

References
- TI BQ24650 datasheet and MPPT reference designs
- Example PMIC application notes from vendors

Next steps
1. Author `pmu.sch` in KiCad using the above nets and component references.
2. Review with electrical engineer and run ERC in KiCad.
3. Export netlist and create PCB footprint list for layout.
