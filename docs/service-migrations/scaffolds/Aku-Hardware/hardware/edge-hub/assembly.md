# Aku Edge Hub — Assembly Procedure

**Revision:** A (Prototype)  
**Estimated assembly time:** 90 minutes (first unit), 45 minutes (subsequent units)

---

## Prerequisites

### Tools Required

- Phillips screwdriver (#1, #2)
- Flat-blade screwdriver (terminal blocks)
- Wire stripper / crimper
- Digital multimeter
- Label printer or permanent marker
- Cable ties
- Anti-static wrist strap

### Materials Required

All items per [`bom.md`](bom.md). Verify quantities before starting.

---

## Step 1 — Prepare the Enclosure

1. Remove the lid of the IP54 enclosure.
2. Mark and drill (or punch) the following cable entry holes on the bottom face:
   - **KO1** 25 mm — 24 V DC input cable gland (PG16)
   - **KO2** 20 mm — HDMI cable gland (PG13.5)
   - **KO3** 16 mm — Ethernet cable gland (PG11)
3. Install cable glands (hand-tight + 1/4 turn with wrench).
4. Mount the DIN rail inside the enclosure base with M4 screws × 4.

## Step 2 — Mount the SBC

1. Attach the Argon ONE M.2 HAT to the Raspberry Pi 4B:
   a. Seat the NVMe SSD in the M.2 2280 slot and tighten the retention screw.
   b. Align the HAT with the RPi GPIO header and press firmly until fully seated.
   c. Secure the HAT-RPi stack with the four standoffs provided.
2. Apply a thin bead of thermal paste to the RPi CPU.
3. Attach the HAT's aluminium heatsink case — it acts as both heatsink and enclosure.
4. Mount the assembled RPi + HAT on the enclosure base plate using M3 standoffs (15 mm × 4).

## Step 3 — Mount the Power Converters

1. Mount **U7** (24 V → 5 V buck) on the DIN rail using the snap-on bracket.
2. Mount **U8** (24 V → 12 V buck) beside it.
3. Mount **TB1** (5-pole terminal block) at the 24 V input entry.
4. Thread the 24 V input cable through KO1; strip 8 mm of insulation.
5. Insert the fuse holder in-line on the positive (red) 24 V wire; install a 5 A fuse.
6. Terminate: positive → TB1-1, negative (black) → TB1-GND.

## Step 4 — Wire Power Rails

Follow the wiring diagram in [`wiring.md`](wiring.md).

1. Run 18 AWG wire from TB1-1 (+24 V) to U7 input+.
2. Run 18 AWG wire from TB1-GND (-24 V) to U7 input-.
3. Run 20 AWG wire from U7 output (5 V) to the USB-C PD connector for the RPi.
4. Run 22 AWG wire from TB1-1 (+24 V) to U8 input+.
5. Run 22 AWG wire from TB1-GND to U8 input-.
6. Run 22 AWG wire from U8 output (12 V) to the Wi-Fi AP power barrel jack.

> **Before continuing:** Measure TB1-1 with a multimeter to confirm 24 V, then measure
> U7 output (target 5.0–5.1 V) and U8 output (target 12.0–12.3 V) without load.

## Step 5 — Install the INA3221 Sensor (U2)

1. Mount the Adafruit INA3221 breakout on the enclosure base with M2 standoffs.
2. Connect I²C signals per [`wiring.md → I²C Bus`](wiring.md) using 26 AWG ribbon cable.
3. Insert 0.1 Ω current-sense shunts on CH1 (solar), CH2 (wind), CH3 (load) wires.
   Each shunt is a series resistor in the positive rail; maintain correct polarity (IN+ faces source).

## Step 6 — Install Temperature Sensors (U3)

1. Thread DS18B20 sensor 1 cable through a small grommet hole; route outside for ambient.
2. Cable-tie DS18B20 sensor 2 to the RPi heatsink for enclosure/SBC temperature.
3. Connect both sensor data wires (yellow) to GPIO 4 (physical pin 7) with a 4.7 kΩ pull-up to 3.3 V.
4. Connect VCC (red) to pin 1 (3.3 V), GND (black) to pin 9.

## Step 7 — Install Status LEDs & PIR

1. Mount the 3-LED status board in the enclosure lid cutout (drill 3 × 5 mm holes).
2. Connect GPIO 22, 23, 24 per [`wiring.md → GPIO Assignments`](wiring.md).
3. Mount the PIR sensor (HC-SR501) on the inside of the lid; connect GPIO 17, 5 V, GND.

## Step 8 — Install the Wi-Fi AP

1. Mount the TP-Link EAP225 on the side of the enclosure or on an external bracket.
2. Route Ethernet from EAP225 LAN port to RPi GbE port through KO3.
3. Power the EAP225 from U8 output (12 V).
4. Mount the EAP225 antennas through the enclosure lid (drill 2 × SMA holes or use external bracket).

## Step 9 — Cable Dress & Labelling

1. Bundle all cables with cable ties every 100 mm.
2. Label every terminal with a printed or hand-written label.
3. Label each wire at both ends: `24V+`, `24V-`, `5V`, `12V`, `I2C-SDA`, `I2C-SCL`, `1W`, `GND`.

## Step 10 — Functional Test

1. Re-check all connections against [`wiring.md`](wiring.md) and the checklist in
   [`../../testing/edge-hub-integration-test.md`](../../testing/edge-hub-integration-test.md).
2. Connect 24 V DC supply (or battery) — the RPi should boot within 60 seconds.
3. Verify all three status LEDs illuminate during boot sequence.
4. SSH into the RPi; run the software stack per the
   [Aku-EdgeHub README](https://github.com/oumar-code/Aku-EdgeHub#quick-start).
5. Confirm INA3221 readings at `/metrics` endpoint.
6. Confirm Wi-Fi SSID "Akulearn_Hub" appears on a test device.

## Step 11 — Seal and Label the Enclosure

1. Close the lid; tighten all lid screws.
2. Affix the serial number label (format: `AEH-YYYYMM-NNN`) to the front of the enclosure.
3. Affix the safety label: "24 V DC — Disconnect before opening."
