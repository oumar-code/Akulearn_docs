# Example Python driver for smart BMS (Battery Management System)
import serial

class BatteryMonitor:
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)

    def read_soc(self):
        self.ser.write(b'READ_SOC\n')
        return float(self.ser.readline().decode().strip())

    def read_voltage(self):
        self.ser.write(b'READ_VOLTAGE\n')
        return float(self.ser.readline().decode().strip())
