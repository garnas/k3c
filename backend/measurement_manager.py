from dotenv import dotenv_values

from sqlalchemy import create_engine

from backend.sqlc.gen.query import Querier


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

measurement_manager = _MeasurementManager()
