from dotenv import load_dotenv
import os
from mysql.connector import pooling
import sqlite3
from pathlib import Path

# Load .env variables
load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE")
}

# Init db (lazy)
pool = None

def _create_pool_if_needed():
    global pool
    if pool is not None:
        return

    # Only attempt to create a pool when all config values are present
    if not all(DB_CONFIG.values()):
        return

    pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=5, **DB_CONFIG)


def get_conn():
    _create_pool_if_needed()
    if pool is None:
        # Fallback: use SQLite for local development
        db_path = Path(__file__).parent / "dev.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        _ensure_sqlite_schema(conn)
        return conn
    return pool.get_connection()


def _ensure_sqlite_schema(conn):
    # Create tables compatible with TODOS.sql if they don't exist
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT,
            due TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()

# DB-Helper
def db_read(sql, params=None, single=False):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())

        if single:
            # liefert EIN Dict oder None
            row = cur.fetchone()
            print("db_read(single=True) ->", row)   # DEBUG
            return row
        else:
            # liefert Liste von Dicts (evtl. [])
            rows = cur.fetchall()
            print("db_read(single=False) ->", rows)  # DEBUG
            return rows

    finally:
        try:
            cur.close()
        except:
            pass
        conn.close()


def db_write(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        print("db_write OK:", sql, params)  # DEBUG
    finally:
        try:
            cur.close()
        except:
            pass
        conn.close()