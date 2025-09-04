# Akulearn Hardware Ordering Guide

## PCB Fabrication
- Use `akulearn_sensor_pcb.kicad_pcb` and `akulearn_sensor_pcb.sch` files.
- Recommended manufacturers: JLCPCB, PCBWay, OSH Park.
- Upload files, select quantity, thickness (1.6mm), and finish (HASL or ENIG).

## Enclosure
- Use `akulearn_enclosure_cad.step` for 3D printing or CNC machining.
- Material: Polycarbonate or aluminum for durability.
- Provide STEP file to local or online fabrication service.

## Components
- Solar panel: 2x 200W, monocrystalline, MC4 connectors.
- Battery: 2x 12V 100Ah lithium or AGM.
- Charge controller: 40A MPPT, Modbus RTU support.
- Inverter: 300W pure sine wave, RS232/RS485 interface.
- Sensors: INA219 (I2C), DS18B20 (1-Wire), relays, connectors.

## Assembly
- Follow wiring diagrams and block diagrams in project docs.
- Use maintenance checklist for ongoing reliability.

---

Order all parts from reputable suppliers and verify compatibility before assembly.
