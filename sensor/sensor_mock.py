from dataclasses import dataclass
import random
import time

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
            temperature=random.randint(-1000, 1000) / 100,
            pressure=random.randint(1000, 1002),
            humidity=random.randint(4000, 6500) / 100,
            gas_resistance=random.randint(40000, 50000),
            timestamp=time.time()
        )
