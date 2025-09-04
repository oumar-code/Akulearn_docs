# Example Python driver for inverter (RS232/RS485)
import serial

class Inverter:
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=9600, timeout=1)

    def read_status(self):
        self.ser.write(b'STATUS\n')
        return self.ser.readline().decode().strip()

    def shutdown(self):
        self.ser.write(b'SHUTDOWN\n')
