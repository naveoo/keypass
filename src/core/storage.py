import sqlite3
from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from re import match

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "database.db"
PASSWORD_TABLE_NAME = getenv("PASSWORD_TABLE_NAME")
if not match(r"^\w+$", PASSWORD_TABLE_NAME):
    raise ValueError("Invalid table name")

def init_cursor():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def init_database():
    conn, cursor = init_cursor()
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {PASSWORD_TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application TEXT NOT NULL,
                userid TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
    finally:
        conn.close()

def insert(values:tuple):
    assert len(values) == 3
    for value in values:
        assert value != ""
    
    conn, cursor = init_cursor()
    try:
        cursor.execute(f"""
            INSERT INTO {PASSWORD_TABLE_NAME} (application, userid, password)
            VALUES (?, ?, ?)
        """, values)
        conn.commit()
    finally:
        conn.close()

def get_applications():
    conn, cursor = init_cursor()
    try:
        cursor.execute(f"SELECT application FROM {PASSWORD_TABLE_NAME}")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

def get_info(application:str):
    conn, cursor = init_cursor()
    try:
        cursor.execute(f"""
            SELECT userid, password FROM {PASSWORD_TABLE_NAME}
            WHERE application = ?
        """, (application,))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()