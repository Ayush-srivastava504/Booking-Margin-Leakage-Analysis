import pandas as pd
from pathlib import Path
from db import get_db_engine, ensure_database

ensure_database()
engine = get_db_engine()

raw_dir = Path("data/raw")

tables = {
    "bookings.csv": "bookings",
    "booking_fees.csv": "booking_fees",
    "host_costs.csv": "host_costs",
}

for filename, table in tables.items():
    path = raw_dir / filename
    if not path.exists():
        continue

    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists="replace", index=False)
