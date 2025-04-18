from dataclasses import dataclass


@dataclass
class Measurement:
    temperature: float
    pressure: float
    humidity: float
    gas_resistance: float
    timestamp: float

    @staticmethod
    def from_sensor():
        return Measurement(
            temperature=3,
            pressure=4,
            humidity=6,
            gas_resistance=7,
            timestamp=8
        )
