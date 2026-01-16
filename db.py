from dotenv import load_dotenv
import os
import sqlite3
from pathlib import Path

# MySQL ist optional - Fallback zu SQLite
try:
    from mysql.connector import pooling
except ImportError:
    pooling = None

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

    # MySQL nur nutzen wenn Paket verfügbar ist
    if pooling is None:
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
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_points (
            user_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )
    conn.commit()

# DB-Helper
def db_write(sql, params=None):
    """Schreibe/Update in die Datenbank"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        if isinstance(conn, sqlite3.Connection):
            # Konvertiere %s zu ? für SQLite
            sql = sql.replace('%s', '?')
        cur.execute(sql, params or ())
        conn.commit()
        print("db_write OK:", sql, params)  # DEBUG
    finally:
        try:
            cur.close()
        except:
            pass
        conn.close()

def db_read(sql, params=None, single=False):
    conn = get_conn()
    try:
        # SQLite und MySQL kompatibel
        if isinstance(conn, sqlite3.Connection):
            cur = conn.cursor()
            # Konvertiere %s zu ? für SQLite
            sql = sql.replace('%s', '?')
        else:
            cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())

        if single:
            # liefert EIN Dict oder None
            row = cur.fetchone()
            # SQLite Row zu Dict konvertieren
            if row and isinstance(conn, sqlite3.Connection):
                row = dict(row)
            print("db_read(single=True) ->", row)   # DEBUG
            return row
        else:
            # liefert Liste von Dicts (evtl. [])
            rows = cur.fetchall()
            # SQLite Rows zu Dicts konvertieren
            if rows and isinstance(conn, sqlite3.Connection):
                rows = [dict(r) for r in rows]
            print("db_read(single=False) ->", rows)  # DEBUG
            return rows

    finally:
        try:
            cur.close()
        except:
            pass
        conn.close()


def db_upsert(user_id, points):
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()

        cur.execute("SELECT user_id FROM user_points WHERE user_id = ?", (user_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute(
                "UPDATE user_points SET points = ? WHERE user_id = ?",
                (points, user_id),
            )
        else:
            cur.execute(
                "INSERT INTO user_points (user_id, points) VALUES (?, ?)",
                (user_id, points),
            )

        conn.commit()
    finally:
        conn.close()


def ensure_pluspoints_column():
    conn = sqlite3.connect("app.db")
    try:
        conn.execute("ALTER TABLE users ADD COLUMN pluspoints INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        # Spalte existiert bereits -> ignorieren
        pass
    finally:
        conn.close()

