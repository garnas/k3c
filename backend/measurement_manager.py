from dotenv import dotenv_values

from sqlalchemy import create_engine

from backend.sqlc.gen.models import Measurement
from backend.sqlc.gen.query import Querier

import dataclasses
import decimal
import datetime


class _MeasurementManager:
    def __init__(self):
        config = dotenv_values(".env")
        DB_NAME = config.get("db_name")
        DB_USER = config.get("db_user")
        DB_PASSWORD = config.get("db_password")
        DB_HOST = config.get("db_host")
        DB_PORT = config.get("db_port")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL, echo=False)
        self.querier = Querier(conn=engine.connect())

    querier: Querier

    @staticmethod
    def serialize_measurement(measurement: Measurement) -> dict:
        return {
            "measurements_id": measurement.measurements_id,
            "temperature": float(measurement.temperature) if measurement.temperature is not None else None,
            "humidity": float(measurement.humidity) if measurement.humidity is not None else None,
            "pressure": float(measurement.pressure) if measurement.pressure is not None else None,
            "gas_resistance": float(measurement.gas_resistance) if measurement.gas_resistance is not None else None,
            "timestamp": measurement.timestamp.timestamp() if measurement.timestamp is not None else None,
        }

measurement_manager = _MeasurementManager()
