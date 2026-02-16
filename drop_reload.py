#!/usr/bin/env python3

# This script handles full database reload for the Booking Margin Leakage project.
# It is intentionally kept separate from the core data generation logic.
#
# The previous data_generator.py was producing less realistic data and was tightly
# coupled to generation logic only. This workflow script exists to:
# - Drop existing MySQL tables
# - Reload fresh CSV data
# - Re-run the SQL transformation pipeline
# - Quickly verify KPIs after reload
#
# It does not change business logic or transformation rules.
# It exists purely for maintenance, testing, and clean re-runs during development.


import os
import time
import traceback
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv

from config import RAW_DATA_DIR, SQL_DIR

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_engine():
    url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    return create_engine(url)


def drop_all_tables():
    print("\nSTEP 1: Dropping tables\n")

    engine = get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        print("No tables found")
        return

    with engine.begin() as conn:
        for table in tables:
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Failed to drop {table}: {str(e)[:80]}")


def load_csv_data():
    print("\nSTEP 2: Loading CSV data\n")

    engine = get_engine()

    tables = [
        ("hosts.csv", "hosts"),
        ("listings.csv", "listings"),
        ("guests.csv", "guests"),
        ("bookings.csv", "bookings"),
        ("booking_fees.csv", "booking_fees"),
        ("host_costs.csv", "host_costs"),
    ]

    for filename, table_name in tables:
        path = RAW_DATA_DIR / filename

        if not path.exists():
            print(f"{filename} not found")
            continue

        try:
            df = pd.read_csv(path)

            date_cols = [c for c in df.columns if "date" in c.lower()]
            for col in date_cols:
                df[col] = pd.to_datetime(df[col], errors="coerce")

            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"{table_name} loaded ({len(df):,} rows)")

        except Exception as e:
            print(f"Error loading {filename}: {str(e)[:100]}")


def run_sql_pipeline():
    print("\nSTEP 3: Running SQL pipeline\n")

    engine = get_engine()
    layers = ["staging", "intermediate", "marts"]

    for layer in layers:
        layer_path = SQL_DIR / layer
        if not layer_path.exists():
            continue

        for sql_file in sorted(layer_path.glob("*.sql")):
            query = sql_file.read_text(encoding="utf-8")

            try:
                with engine.begin() as conn:
                    conn.execute(text(query))
                print(f"Executed {sql_file.name}")
            except Exception as e:
                print(f"Error in {sql_file.name}: {str(e)[:100]}")


def verify_data():
    print("\nSTEP 4: Verifying\n")

    engine = get_engine()

    try:
        df = pd.read_sql("SELECT * FROM kpi_profitability_distribution", engine)
        print(df)

        df2 = pd.read_sql("SELECT * FROM kpi_revenue_overview", engine)
        print(df2)

    except Exception as e:
        print(f"Verification failed: {str(e)[:100]}")


def main():
    print("\nBooking Margin Leakage - Full Reload\n")

    try:
        drop_all_tables()
        time.sleep(1)

        load_csv_data()
        time.sleep(1)

        run_sql_pipeline()
        time.sleep(1)

        verify_data()

        print("\nWorkflow finished\n")

    except Exception as e:
        print(f"\nFatal error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
