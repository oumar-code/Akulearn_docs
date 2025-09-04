# Solar Power System Wiring Diagram for Akulearn Projector Hub

```
[SOLAR PANEL]---(DC)---[CHARGE CONTROLLER]---(DC)---[DEEP-CYCLE BATTERY]---(DC)---[INVERTER]---(AC)---[SMART BOARD/TV + PROJECTOR HUB]

# Monitoring Connections:
- Charge Controller: Serial/USB/I2C to Linux device
- Battery: Smart BMS (UART/I2C/RS485) to Linux device
- Inverter: RS232/RS485/Ethernet to Linux device

# Example Physical Connections:
- Solar Panel (+/-) to Charge Controller PV input
- Charge Controller Battery output (+/-) to Battery terminals
- Battery output (+/-) to Inverter DC input
- Inverter AC output to Smart Board/TV/Hub
- Charge Controller/Smart BMS/ Inverter communication ports to Linux device (USB/Serial/I2C)
```

## Notes
- Use appropriate fuses and breakers for safety.
- All communication cables (serial, I2C, RS485) should be shielded and kept short.
- Enclosure should be ventilated and secure.
