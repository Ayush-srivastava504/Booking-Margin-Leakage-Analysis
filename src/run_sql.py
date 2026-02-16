from pathlib import Path
from sqlalchemy import text
from db import get_db_engine, ensure_database

ensure_database()
engine = get_db_engine()

base_path = Path("sql")
layers = ["staging", "intermediate", "marts"]

for layer in layers:
    layer_path = base_path / layer
    if not layer_path.exists():
        continue

    for sql_file in sorted(layer_path.glob("*.sql")):
        query = sql_file.read_text(encoding="utf-8")

        with engine.begin() as conn:
            conn.execute(text(query))
