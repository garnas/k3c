import os
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from backend.sqlc.gen.query import Querier, CreateMeasurementParams

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
DB_NAME = os.getenv("db_name")
DB_USER = os.getenv("db_user")
DB_PASSWORD = os.getenv("db_password")
DB_HOST = os.getenv("db_host")
DB_PORT = os.getenv("db_port")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False)

with engine.connect() as conn:
    q = Querier(conn=conn)
    params = CreateMeasurementParams(
        timestamp=datetime.now(),
        humidity=Decimal(12),
        temperature=Decimal(22),
        pressure=Decimal(32),
        gas_resistance=Decimal(52),
    )
    q.create_measurement(
        arg=params
    )
    t = q.list_measurements()
    for m in t:
        print(m)
    conn.commit()

exit()
# Check if essential variables are loaded
if not all([DB_NAME, DB_USER, DB_PASSWORD]):
    print("Error: Database credentials (DB_NAME, DB_USER, DB_PASSWORD) not found in .env file.")
    exit(1)

# Construct the database URL (DSN) for SQLAlchemy
# Using 'psycopg' driver which works with the modern 'psycopg' library (or 'psycopg2')

print(f"Attempting to connect to: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # Create an engine instance (SQLAlchemy 2.0 style)
    # echo=True will log all SQL generated, remove for production
    engine = create_engine(DATABASE_URL, echo=False)

    # Connect to the database and test the connection
    with engine.connect() as connection:
        # Execute a simple query to verify connection
        result = connection.execute(text("SELECT 1"))
        print(f"Successfully connected to database '{DB_NAME}'!")
        print(f"Test query result (SELECT 1): {result.scalar_one()}")

    # The connection is automatically closed when exiting the 'with' block

except OperationalError as e:
    print(f"Error connecting to the database: {e}")
    print("Please check:")
    print("1. Is the PostgreSQL server running (e.g., via Docker)?")
    print("2. Are the credentials in the .env file correct?")
    print(f"3. Is the host '{DB_HOST}' and port '{DB_PORT}' accessible?")
except Exception as e:
    print(f"An unexpected error occurred: {e}")