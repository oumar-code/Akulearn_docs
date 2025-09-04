# Example sensor code for temperature, voltage, current

import board
import busio
import adafruit_ina219
import adafruit_ds18x20
import adafruit_onewire.bus
import requests

i2c = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c)
voltage = ina219.bus_voltage
current = ina219.current
onewire_bus = adafruit_onewire.bus.OneWireBus(board.D2)
ds18 = adafruit_ds18x20.DS18X20(onewire_bus, onewire_bus.scan()[0])
temperature = ds18.temperature

print('Bus Voltage:', voltage)
print('Current:', current)
print('Temperature:', temperature)

# Post sensor data to backend
data = {
	'voltage': voltage,
	'current': current,
	'temperature': temperature
}
try:
	r = requests.post('http://localhost:8000/sensor/data', json=data)
	print('POST result:', r.json())
except Exception as e:
	print('POST failed:', e)
