# Aku Platform Sensor Code

import board
import busio
import adafruit_ina219
import adafruit_ds18x20
import adafruit_onewire.bus
import requests

# Optional wind sensor import
try:
    import adafruit_anemometer
except ImportError:
    adafruit_anemometer = None

# Modular sensor reading functions
def read_voltage_current():
    i2c = busio.I2C(board.SCL, board.SDA)
    ina219 = adafruit_ina219.INA219(i2c)
    return ina219.bus_voltage, ina219.current

def read_temperature():
    onewire_bus = adafruit_onewire.bus.OneWireBus(board.D2)
    ds18 = adafruit_ds18x20.DS18X20(onewire_bus, onewire_bus.scan()[0])
    return ds18.temperature

def read_wind_speed():
    if adafruit_anemometer:
        wind_sensor = adafruit_anemometer.Anemometer(board.D3)
        return wind_sensor.wind_speed
    return None

# Main function for multi-product support
def collect_sensor_data(product_type="hub"):
    voltage, current = read_voltage_current()
    temperature = read_temperature()
    wind_speed = read_wind_speed()
    data = {
        'product_type': product_type,
        'voltage': voltage,
        'current': current,
        'temperature': temperature,
        'wind_speed': wind_speed
    }
    return data

if __name__ == "__main__":
    # Example: set product_type to 'projector', 'smart_board', etc.
    product_type = "hub"
    sensor_data = collect_sensor_data(product_type)
    print("Sensor Data:", sensor_data)
    try:
        r = requests.post('http://localhost:8000/sensor/data', json=sensor_data)
        print('POST result:', r.json())
    except Exception as e:
        print('POST failed:', e)
