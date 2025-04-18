import time
from dataclasses import dataclass
import bme680

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('Initial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)


@dataclass
class Measurement:
    temperature: float
    pressure: float
    humidity: float
    gas_resistance: float
    timestamp: float

    @staticmethod
    def from_sensor():
        if sensor.get_sensor_data() and sensor.data.heat_stable:
            return Measurement(
                temperature=sensor.data.temperature,
                pressure=sensor.data.pressure,
                humidity=sensor.data.humidity,
                gas_resistance=sensor.data.gas_resistance,
                timestamp=time.time()
            )
