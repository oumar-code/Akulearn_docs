# Example sensor code for temperature, voltage, current, wind speed

import board
import busio
import adafruit_ina219
import adafruit_ds18x20
import adafruit_onewire.bus
import requests
# Example wind sensor import (replace with actual library if needed)
try:
    import adafruit_anemometer
except ImportError:
    adafruit_anemometer = None

i2c = busio.I2C(board.SCL, board.SDA)
ina219 = adafruit_ina219.INA219(i2c)
voltage = ina219.bus_voltage
current = ina219.current
onewire_bus = adafruit_onewire.bus.OneWireBus(board.D2)
ds18 = adafruit_ds18x20.DS18X20(onewire_bus, onewire_bus.scan()[0])
temperature = ds18.temperature

# Wind sensor example (replace pin and logic as needed)
wind_speed = None
if adafruit_anemometer:
    wind_sensor = adafruit_anemometer.Anemometer(board.D3)
    wind_speed = wind_sensor.wind_speed

print('Bus Voltage:', voltage)
print('Current:', current)
print('Temperature:', temperature)
if wind_speed is not None:
    print('Wind Speed:', wind_speed)

# Post sensor data to backend
data = {
    'voltage': voltage,
    'current': current,
    'temperature': temperature,
    'wind_speed': wind_speed
}
try:
    r = requests.post('http://localhost:8000/sensor/data', json=data)
    print('POST result:', r.json())
except Exception as e:
    print('POST failed:', e)
