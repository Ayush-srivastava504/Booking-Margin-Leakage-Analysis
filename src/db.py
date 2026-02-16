from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_server_engine():
    url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    return create_engine(url)


def get_db_engine():
    url = URL.create(
        "mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
    return create_engine(url)


def ensure_database():
    engine = get_server_engine()
    with engine.begin() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
