# Example Python driver for solar charge controller (Modbus RTU)
import serial
import minimalmodbus

class ChargeController:
    def __init__(self, port, slave_address=1):
        self.instrument = minimalmodbus.Instrument(port, slave_address)
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.timeout = 1

    def read_battery_voltage(self):
        # Register address may vary by model
        return self.instrument.read_register(0x3100, 2)

    def read_panel_output(self):
        return self.instrument.read_register(0x3101, 2)

    def set_low_power_mode(self, enable):
        # Write to control register
        self.instrument.write_register(0x3300, int(enable))
