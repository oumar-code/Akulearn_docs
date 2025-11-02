EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:conn
LIBS:regul
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "PMU - Edge Alpha"
Date ""
Rev "alpha"
Comp ""
Comment1 "PMU schematic scaffold: replace placeholders with actual footprints in KiCad"
$EndDescr

$Sheet 1 1
pmu 0 0
$EndSheet

# Nets (define as named nets in KiCad when creating the schematic):
# SOLAR_PLUS, SOLAR_MINUS, BATT_PLUS, BATT_MINUS, 12V, GND, V5V, V3V3, V1V8,
# BMS_SDA, BMS_SCL, PWR_OK, RESET_N, SENSE_PLUS, SENSE_MINUS

# Input Protection block
Text Notes 100 100 2 ~ 0
Input Protection:
# - Reverse polarity protection (P-channel MOSFET or ideal diode)
# - TVS diode footprint
# - Fuse footprint (F1)

# MPPT Interface block
Text Notes 100 220 2 ~ 0
MPPT Interface:
# - If external MPPT: connector J1 with SOLAR_PLUS/SOLAR_MINUS and BATT outputs
# - If on-board: place controller U_MPPT with switching components

# Battery pack and BMS
Text Notes 100 340 2 ~ 0
Battery/BMS:
# - Connector J_BATT: BATT_PLUS, BATT_MINUS, BMS_SDA, BMS_SCL
# - Shunt resistor footprint R_SENSE between SENSE_PLUS and SENSE_MINUS

# DC-DC regulators and power rails
Text Notes 100 460 2 ~ 0
DC-DC Regulators:
# - U1: BUCK_5V -> V5V
# - U2: BUCK_3V3 -> V3V3
# - U3: LDO_1V8 -> V1V8
# - Place bulk caps C_bulk_12V near DC-DC input

# Monitoring and telemetry
Text Notes 100 580 2 ~ 0
Telemetry:
# - U_ISENSE: INA219/INA226 measured across R_SENSE
# - TEMP_SENSE: NTC or digital temp sensor footprint
# - Expose BMS_SDA/BMS_SCL to compute module via level shifter if needed

# Debug header and programming
Text Notes 100 700 2 ~ 0
Debug Header:
# - JTAG header footprint
# - UART header (3.3V TTL)

# Test Points (add TP footprints): TP_BATT+, TP_BATT-, TP_12V, TP_5V, TP_3V3, TP_1V8, TP_SENSE+, TP_SENSE-, TP_RESET

End
